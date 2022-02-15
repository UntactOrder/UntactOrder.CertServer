# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : CertServer.app & Last Modded : 2022.02.16. ###
Coded with Python 3.10 Grammar by purplepig4657
Description : ?
Reference : ?
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from flask import Flask, request, jsonify, make_response
from waitress import serve

from cert_generator import proceed_certificate_generation


app = Flask(__name__)


@app.route('/')
def index():
    """ To check if the server is running """
    return "Hello, World!"


@app.route('/cert_request', methods=['POST'])
def cert_request() -> jsonify:
    """ Process the certificate request. """
    client_public_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)  # get external IP
    personal_json = request.get_json()
    if not personal_json or len(personal_json) > 1:  # if not '0 < len(json) < 2', then it's bad request.
        return make_response("Json Parse Error", 400)
    client_private_ip = next(iter(personal_json.values()))  # get internal IP
    crt_dump, key_dump = proceed_certificate_generation(client_public_ip, client_private_ip)  # generate certificate
    respond = {'crt': crt_dump.decode(), 'key': key_dump.decode()}  # create respond object
    return jsonify(respond)


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000, url_scheme='https')
