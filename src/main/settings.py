# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : CertServer.settings & Last Modded : 2022.02.21. ###
Coded with Python 3.10 Grammar by purplepig4657
Description : CertServer Settings
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import platform
from OpenSSL import crypto


IP_API_URL = "https://api.ipify.org"

TYPE_RSA = crypto.TYPE_RSA
FILETYPE_PEM = crypto.FILETYPE_PEM
ONE_YEAR = 365 * 24 * 60 * 60
HOW_MANY_YEARS = 65

OS = platform.system()

CERT_DIR = "cert" if OS == "Windows" else "/etc/certserver"
CERT_FILE = "rootCA.crt"
KEY_FILE = "rootCA.key"
PASS_FILE = "ssl.pass"
