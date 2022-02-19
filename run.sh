#!/usr/bin/env bash
cd ./src/main
sudo waitress-serve --host=127.0.0.1 --port=5000 --url-scheme=https --call app:create_app | tee -a waitress-serve.log
