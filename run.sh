#!/usr/bin/env bash
sudo -i -u root bash << EOF
echo -n "INFO:get passphrase and certificate key with permission of "
whoami
passphrase=$(</etc/certserver/ssl.pass)
key=$(</etc/certserver/rootCA.key)
EOF

echo -n "INFO:server open with permission of "
whoami
cd ./src/main
waitress-serve --po=$passphrase --ho=$key --host=127.0.0.1 --port=5000 --url-scheme=https --call app:create_app | tee -a waitress-serve.log
