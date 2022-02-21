# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : CertServer.cert_generator & Last Modded : 2022.02.21. ###
Coded with Python 3.10 Grammar by purplepig4657
Description : This is a generator script to generate a CertSercer-signed certificate.
Reference : [CA certificate] https://www.openssl.org/docs/manmaster/man5/x509v3_config.html
            [add subject, authority key] https://stackoverflow.com/questions/14972345/creating-self-signed-certificate-using-pyopenssl
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from os import path
import sys
from getpass import getpass
from geocoder import ipinfo

from settings import *


# [import root CA certificate.]
# check if root CA certificate is exist.
if not path.isfile(f"{CERT_DIR}/{CERT_FILE}"):
    print(f"Certificate files not found. You must init(generate a certificate) first.")
    sys.exit(1)

# ***** An error may occur in later times. *****
# get a passphrase and key by an expedient way; waitress checks only part of the argv.
try:
    __PASSPHRASE__ = sys.argv[[i for i, arg in enumerate(sys.argv) if '--po=' in arg][0]]\
        .replace('--po=', '').replace('\n', '').replace('\r', '')
except IndexError:
    if OS == "Windows" and path.isfile(f"{CERT_DIR}/{PASS_FILE}"):
        with open(f"{CERT_DIR}/{PASS_FILE}", 'r') as pass_file:
            __PASSPHRASE__ = pass_file.read().replace('\n', '').replace('\r', '')
    else:
        __PASSPHRASE__ = getpass("Enter passphrase: ")
try:
    __KEY_FILE__ = sys.argv[[i for i, arg in enumerate(sys.argv) if '--ho=' in arg][0]].replace('--ho=', '')
except IndexError:
    if OS == "Windows" and path.isfile(f"{CERT_DIR}/{KEY_FILE}"):
        with open(f"{CERT_DIR}/{KEY_FILE}", 'r') as ca_key_file:
            __KEY_FILE__ = ca_key_file.read()
    else:
        __KEY_FILE__ = getpass("Enter certificate key: ")

with open(path.join(CERT_DIR, CERT_FILE), 'r') as ca_crt_file:
    __CA_CRT__ = crypto.load_certificate(FILETYPE_PEM, ca_crt_file.read().encode('utf-8'))
__CA_KEY__ = crypto.load_privatekey(FILETYPE_PEM, __KEY_FILE__, passphrase=__PASSPHRASE__.encode('utf-8'))


def generate_key() -> crypto.PKey:
    """ Generate a key pair with a 4096 bit RSA key.
        This key is going to be send to the client.
    """
    keypair = crypto.PKey()
    keypair.generate_key(TYPE_RSA, 4096)

    return keypair


def make_certificate_signing_request(
        client_keypair: crypto.PKey, client_public_ip: str, client_private_ip: str) -> crypto.X509Req:
    """ Make a certificate signing request, that is originally used to request for signing to the CA(CS) by the client.
        But, in this case, the client does not send the CSR to the CA, instead, the CA make CSR and do the signing.
    """
    # get public(external) ip address information from ipinfo.io api.
    _, city, region, country, *_ = ipinfo(client_public_ip).json['raw'].values()

    # create a subject object
    request = crypto.X509Req()
    subject = request.get_subject()
    subject.CN = client_private_ip  # internal ip
    subject.C = country
    subject.ST = region
    subject.L = city
    subject.O = "UntactOrder"
    subject.OU = "A PosServer Instance"
    request.set_pubkey(client_keypair)
    request.sign(client_keypair, 'SHA256')  # sign the request(csr) with the CA(CS) private key.

    return request


def create_certificate(csr: crypto.X509Req, client_private_ip: str) -> bytes:
    """ Create a certificate from the CSR.
        The certificate is signed by the CA(CS)."""
    crt = crypto.X509()  # create a certificate object
    crt.set_version(2)
    crt.set_serial_number(1)  # serial number must be unique, but we don't care. ^^

    crt.gmtime_adj_notBefore(0)  # start time from now
    crt.gmtime_adj_notAfter(ONE_YEAR * HOW_MANY_YEARS)  # end time
    crt.set_issuer(__CA_CRT__.get_subject())  # set root CA information.
    crt.set_subject(csr.get_subject())  # set client information from the CSR.
    crt.add_extensions([  # add extensions; crt does not ues domain name, so we need to add subject alternative name.
        crypto.X509Extension(b"subjectAltName", False, f"IP:{client_private_ip}".encode('utf-8'))
    ])  # if the client's ip is not exists at crt ip list, the certificate will be disabled.
    crt.set_pubkey(csr.get_pubkey())  # set client public key from the CSR to the crt.
    crt.sign(__CA_KEY__, 'SHA256')  # sign the crt with the CA(CS) private key.

    return crypto.dump_certificate(FILETYPE_PEM, crt)  # dump the certificate to bytes.


def proceed_certificate_generation(client_public_ip: str, client_private_ip: str) -> (bytes, bytes):
    """ Proceed the certificate generation.
    """
    # generate a key pair.
    client_keypair = generate_key()
    key_dump = crypto.dump_privatekey(FILETYPE_PEM, client_keypair)

    # make a certificate signing request.
    csr = make_certificate_signing_request(client_keypair, client_public_ip, client_private_ip)

    # create a certificate dump.
    crt_dump = create_certificate(csr, client_private_ip)

    return crt_dump, key_dump
