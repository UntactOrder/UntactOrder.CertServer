#!/usr/bin/env bash
passphrase=value=$(</etc/certserver/ssl.pass)
key=value=$(</etc/certserver/rootCA.key)

cd ./src/main
waitress-serve --po=passphrase --ho=key --host=127.0.0.1 --port=5000 --url-scheme=https --call app:create_app | tee -a waitress-serve.log
