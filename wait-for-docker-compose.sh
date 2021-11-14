#!/usr/bin/env bash

is_healthy() {

    mongo_health_status="$(docker inspect -f "{{.State.Status}}" mongodb)"
    flask_health_status="$(docker inspect -f "{{.State.Status}}" flask)"

    if [ "$mongo_health_status" = "running" ] && [ "$flask_health_status" = "running" ]; then
        return 0
    else
        return 1
    fi
}

timer=0
while ! is_healthy; do 
    if [ $timer = $1 ]; then
        echo "Docker-compose command didn't complete within" $1 "seconds"
        echo "Docker-compose command didn't complete within" $1 "seconds. Check your code." > testResult.txt 
        exit 1
    fi
    sleep 1
    timer=$((timer+1)); 
done

