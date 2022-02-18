#!/usr/bin/env bash
# https://growingsaja.tistory.com/330

date_year=`date |cut -d ' ' -f7`
date_month=`date |cut -d ' ' -f2`
date_day=`date |cut -d ' ' -f4`
full_date="$date_year"_"$date_month"_"$date_day"

nohup ./run.sh >> /log/"$full_date".log &
