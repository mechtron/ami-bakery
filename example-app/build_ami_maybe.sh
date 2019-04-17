#!/usr/bin/env bash

docker run --rm -t \
    -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
    -e AWS_SUBNET_ID=$AWS_SUBNET_ID \
    -e PACKER_JSON_PATH=`pwd`/example-app/ami/packer/ami.json \
    -e AMI_DEFINITION_DIRS=`pwd`/example-app/ami/ \
    --mount type=bind,source=`pwd`,target=`pwd` \
    --mount type=bind,source=$HOME/.aws/,target=/root/.aws \
    mechtron/ami-bakery:latest
