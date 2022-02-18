cd src/main
waitress-serve --host=127.0.0.1 --port=5000 --url-scheme=https --call app:create_app
:waitress-serve --po='YourCertPassWord' --host=127.0.0.1 --port=5000 --url-scheme=https --call app:create_app
