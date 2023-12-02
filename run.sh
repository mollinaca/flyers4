#!/bin/bash

if [ ! -e $(pwd)/app/data/last.json ]; then
    cp $(pwd)/app/data/last-init.json $(pwd)/app/data/last.json
fi

PATH=$PATH:/usr/bin/:/usr/local/bin
# docker-compose up
docker-compose run flyers4 python main.py
