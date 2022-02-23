#!/usr/bin/env bash
echo -n "INFO:get passphrase and certificate key with permission of "
whoami
passphrase="$(</etc/certserver/ssl.pass)"
key="$(cat /etc/certserver/rootCA.key)"

date_year=`date | cut -d ' ' -f7`
date_month=`date | cut -d ' ' -f2`
date_day=`date | cut -d ' ' -f4`
full_date="$date_year"_"$date_month"_"$date_day"

sudo -u ubuntu bash << EOF
echo -n "INFO:server open with permission of "
whoami

cd src/main
echo -e "$passphrase\n$key\n" | waitress-serve --po=on --host=127.0.0.1 --port=5000 --url-scheme=https --call app:create_app | tee -a ../../log/"$full_date".waitress-serve.log
EOF
