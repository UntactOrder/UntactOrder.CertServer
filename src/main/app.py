# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
### Alias : CertServer.app & Last Modded : 2022.02.26. ###
Coded with Python 3.10 Grammar by purplepig4657
Description : CertServer is a simple web server for managing SSL certificates.
              waitress process http/https requests and flask make respond data.
Reference : [create_app] https://stackoverflow.com/questions/57600034/waitress-command-line-returning-malformed-application-when-deploying-flask-web
            [Logging] https://stackoverflow.com/questions/52372187/logging-with-command-line-waitress-serve
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from datetime import datetime, time

from flask import Flask, request, jsonify, make_response
from waitress import serve

from cert_generator import proceed_certificate_generation, UnitType


def create_app():
    app = Flask(__name__)

    service_denial_msg = "From 3:00 to 3:30, it is server inspection time. Sorry for the inconvenience. " \
                         "We would appreciate it if you could try again after the inspection."
    service_denial_start = time(3, 0, 0, 0)
    service_denial_end = time(3, 30, 0, 0)

    def server_inspection_time_noticer(func):
        def notice_service_denial(*args, **kwargs):
            if service_denial_start <= datetime.now().time() <= service_denial_end:
                print("Server Inspection Time")
                return make_response(service_denial_msg, 503)
            else:
                return func(*args, **kwargs)
        notice_service_denial.__name__ = func.__name__  # rename function name
        return notice_service_denial

    @app.route('/')
    @server_inspection_time_noticer
    def index():
        """ To check if the server is running """
        #return f"Hello, {request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}!"
        return "Hello, World!"

    @app.route('/cert_request/<unit_type>', methods=['POST'])
    @server_inspection_time_noticer
    def cert_request(unit_type) -> jsonify:
        """
        Process the certificate request - POST method
        :param unit_type: Can be "bridge" or "pos"
        """
        unit_type = UnitType.BRIDGE if unit_type == "bridge" else UnitType.POS

        # get private/public ip address from request
        if unit_type == UnitType.POS:  # if PosServer unit
            # if not '0 < len(json) < 2' or if private_ip from json is not ipv4/ipv6 shape, then it's bad request.
            personal_json = request.get_json()
            if not personal_json or len(personal_json) > 1 or True not \
                    in [personal_json[list(personal_json)[-1]].count(i[0]) == i[1] for i in (('.', 3), (':', 7))]:
                return make_response("Json Parse Error", 411)
            client_private_ip = next(iter(personal_json.values()))  # get internal IP
        else:  # if BridgeServer unit, then private_ip is not required.
            client_private_ip = ""
        client_public_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)  # get external IP

        # generate certificate and return response
        crt_dump, key_dump = proceed_certificate_generation(unit_type, client_public_ip, client_private_ip)
        respond = {'crt': crt_dump.decode(), 'key': key_dump.decode()}  # create respond object
        return jsonify(respond)

    return app


if __name__ == '__main__':
    wsgiapp = create_app()
    serve(wsgiapp, host='0.0.0.0', port=5000, url_scheme='https')
