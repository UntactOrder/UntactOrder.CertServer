# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : CertServer.cert_generator & Last Modded : 2022.02.16. ###
Coded with Python 3.10 Grammar by purplepig4657
Description : This is a generator script to generate a CertSercer-signed certificate.
Reference : [CA certificate] https://www.openssl.org/docs/manmaster/man5/x509v3_config.html
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from os import path, mkdir
from getpass import getpass
import requests
from OpenSSL import crypto
from geocoder import ipinfo


IP_API_URL = "https://api.ipify.org"

TYPE_RSA = crypto.TYPE_RSA
FILETYPE_PEM = crypto.FILETYPE_PEM
ONE_YEAR = 365 * 24 * 60 * 60
HOW_MANY_YEARS = 65

CERT_DIR = "cert"
CERT_FILE = "rootCA.crt"
KEY_FILE = "rootCA.key"
PASS_FILE = "ssl.pass"

# import root CA certificate.
if not path.isdir(CERT_DIR):
    mkdir(CERT_DIR)

if path.isfile(f"{CERT_DIR}/{PASS_FILE}"):
    with open(f"{CERT_DIR}/{PASS_FILE}", 'r') as pass_file:
        __PASSPHRASE__ = pass_file.read().replace('\n', '').replace('\r', '')
else:
    __PASSPHRASE__ = getpass("Enter passphrase: ")

if not path.isfile(f"{CERT_DIR}/{CERT_FILE}") or not path.isfile(f"{CERT_DIR}/{KEY_FILE}"):
    print(f"\nCertificate files not found. Create a directory called '{CERT_DIR}' automatically "
          f"in the same directory as this python file and generate '{CERT_FILE}' and '{KEY_FILE}' files.")

    def proceed_certificate_authority_generation():
        """ Generate CertServer crt file and key file with a 4096 bit RSA key.
        """
        keypair = crypto.PKey()
        keypair.generate_key(TYPE_RSA, 4096)

        public_ip = requests.get(IP_API_URL).content.decode()
        country = input("Enter your Country Name: ")
        region = input("Enter your State: ")
        city = input("Enter your Location(City): ")

        crt = crypto.X509()
        crt.set_version(2)
        crt.set_serial_number(1)  # serial number must be unique, but we don't care. ^^
        crt.gmtime_adj_notBefore(0)  # start time from now
        crt.gmtime_adj_notAfter(ONE_YEAR * HOW_MANY_YEARS)  # end time

        subject = crt.get_subject()
        subject.CN = public_ip  # external ip
        subject.C = country
        subject.ST = region
        subject.L = city
        subject.O = "UntactOrder"
        subject.OU = "A CertServer Instance"
        crt.add_extensions([  # add extensions; crt does not ues domain name, so need to add subject alternative name.
            # [set this certificate belongs to Certificate Authority(CA)]

            # This is a multi-valued extension which indicates whether a certificate is a CA certificate.
            # The first value is CA followed by TRUE or FALSE. If CA is TRUE then an optional pathlen name followed
            # by a nonnegative value can be included.
            crypto.X509Extension(b'basicConstraints', True, b'CA:TRUE'),
            # The SKID extension specification has a value with three choices. If the value is the word none then
            # no SKID extension will be included. If the value is the word hash, or by default for the x509, req,
            # and ca apps, the process specified in RFC 5280 section 4.2.1.2. (1) is followed: The keyIdentifier is
            # composed of the 160-bit SHA-1 hash of the value of the BIT STRING subjectPublicKey (excluding the tag,
            # length, and number of unused bits).
            crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash", subject=crt),
            crypto.X509Extension(b"subjectAltName", False, f"IP:{public_ip}".encode('utf-8'))
        ])  # if the client's ip is not exists at crt ip list, the certificate will be disabled.
        crt.add_extensions([
            # The AKID extension specification may have the value none indicating that no AKID shall be included.
            # Otherwise it may have the value keyid or issuer or both of them, separated by ,. Either or both can have
            # the option always, indicated by putting a colon : between the value and this option. For self-signed
            # certificates the AKID is suppressed unless always is present. By default the x509, req, and ca apps
            # behave as if none was given for self-signed certificates and keyid, issuer otherwise.
            crypto.X509Extension(b"authorityKeyIdentifier", False, b"keyid:always", issuer=crt)
        ])
        crt.set_subject(crt.get_subject())
        crt.set_issuer(crt.get_subject())
        crt.set_pubkey(keypair)
        crt.sign(keypair, 'SHA256')  # sign with the CA(CS) private key.

        with open(path.join(CERT_DIR, KEY_FILE), 'w+') as ca_key_file, \
                open(path.join(CERT_DIR, CERT_FILE), 'w+') as ca_crt_file:
            ca_key_file.write(crypto.dump_privatekey(
                FILETYPE_PEM, keypair, cipher='AES256', passphrase=__PASSPHRASE__.encode('utf-8')).decode())
            ca_crt_file.write(crypto.dump_certificate(FILETYPE_PEM, crt).decode())
            print("Certificate Authority generated successfully.\n")

    proceed_certificate_authority_generation()

with open(path.join(CERT_DIR, CERT_FILE), 'r') as ca_crt_file, open(path.join(CERT_DIR, KEY_FILE), 'r') as ca_key_file:
    __CA_CRT__ = crypto.load_certificate(FILETYPE_PEM, ca_crt_file.read().encode('utf-8'))
    __CA_KEY__ = crypto.load_privatekey(FILETYPE_PEM, ca_key_file.read(), passphrase=__PASSPHRASE__.encode('utf-8'))


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
    crt.sign(__CA_KEY__, "SHA256")  # sign the crt with the CA(CS) private key.

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
