#!/bin/bash

# add credHelpers 
aws configure set aws_access_key_id AKIAYJCRSQ3QSJOMG7XI
aws configure set aws_secret_access_key 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
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 569254250209.dkr.ecr.us-east-2.amazonaws.com

if [ "$BRANCH_NAME" = "master" ]; then
    export TAG="1.0.$BUILD_NUMBER" 
elif [ "$BRANCH_NAME" = "dev" ]; then
    tag_tail=$(git rev-parse HEAD)
    export TAG="dev-$tag_tail"

else 
    tag_tail=$(git rev-parse HEAD)
    export TAG="stg-$tag_tail"
                 
fi 

docker tag server:1.0 569254250209.dkr.ecr.us-east-2.amazonaws.com/contactapp:$TAG
docker push 569254250209.dkr.ecr.us-east-2.amazonaws.com/contactapp:$TAG

