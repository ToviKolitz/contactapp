#!/bin/bash

# add credHelpers 
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 006262944085.dkr.ecr.us-east-2.amazonaws.com

if [ "$BRANCH_NAME" = "master" ]; then
    export TAG="1.0.$BUILD_NUMBER" 
elif [ "$BRANCH_NAME" = "dev" ]; then
    tag_tail=$(git rev-parse HEAD)
    export TAG="dev-$tag_tail"

else 
    tag_tail=$(git rev-parse HEAD)
    export TAG="stg-$tag_tail"
                 
fi 

docker tag server:1.0 006262944085.dkr.ecr.us-east-2.amazonaws.com/contactapp:$TAG
docker push 006262944085.dkr.ecr.us-east-2.amazonaws.com/contactapp:$TAG

