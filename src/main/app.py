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


@app.route('/cert_request', methods=['POST'])
def cert_request() -> jsonify:
    client_public_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    personal_json = request.get_json()
    if not personal_json or len(personal_json) > 1:
        return make_response("Json Parse Error", 400)
    client_private_ip = next(iter(personal_json.values()))
    crt_dump, key_dump = proceed_certificate_generation(client_public_ip, client_private_ip)
    respond = {'crt': crt_dump.decode(), 'key': key_dump.decode()}
    return jsonify(respond)


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000, url_scheme='https')
