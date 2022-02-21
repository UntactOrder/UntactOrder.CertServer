#!/usr/bin/env bash
# https://growingsaja.tistory.com/330
sudo -i -u root bash << EOF
echo -n "INFO:get passphrase and certificate key with permission of "
whoami
passphrase=value=$(</etc/certserver/ssl.pass)
key=value=$(</etc/certserver/rootCA.key)
EOF

echo -n "INFO:server open with permission of "
whoami

date_year=`date | cut -d ' ' -f7`
date_month=`date | cut -d ' ' -f2`
date_day=`date | cut -d ' ' -f4`
full_date="$date_year"_"$date_month"_"$date_day"

tee -a waitress-serve.log | nohup waitress-serve --po=$passphrase --ho=$key --host=127.0.0.1 --port=5000 --url-scheme=https --call app:create_app >> ./log/"$full_date".log &
