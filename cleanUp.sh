#!/bin/bash

# remove credHelpers
isConfFileExist=$(ls /root/.docker | grep "config.json")
if [[ ! -z "$isConfFileExist" ]]; then
    sudo rm /root/.docker/config.json
fi


docker-compose down -v