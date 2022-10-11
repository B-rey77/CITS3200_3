#!/bin/bash

# This bash script is used during the DeployCode stage of
# the pipeline. The AWS CodeDeploy agent uses this script to
# delete all source code files that are copied to the
# EC2 instance

rm -rf /tmp/webapp/
for x in $(docker container ls -a --format '{{.ID}}' | grep -v pg); do
    docker container rm $x
done

for x in $(docker volume ls --format '{{.Name}}'); do
    docker volume rm $x
done