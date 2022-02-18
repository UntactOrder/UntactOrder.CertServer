#!/usr/bin/env bash
# https://growingsaja.tistory.com/330

date_year=`date |cut -d ' ' -f7`
date_month=`date |cut -d ' ' -f2`
date_day=`date |cut -d ' ' -f4`
full_date="$date_year"_"$date_month"_"$date_day"

nohup waitress-serve --host=127.0.0.1 --port=5000 --url-scheme=https --call app:create_app >> ./log/"$full_date".log & tee -a waitress-serve.log
