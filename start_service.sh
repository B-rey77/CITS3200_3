#!/bin/bash

# This bash script is used during the DeployCode stage of
# the pipeline. The AWS CodeDeploy agent uses this script to
# run the Docker container on the EC2 instance

SMTP_HOST="$(aws ssm get-parameter --region ap-southeast-2 --name CITS3200_SMTP_HOST --output text --query "Parameter.Value")"
SMTP_USER="$(aws ssm get-parameter --region ap-southeast-2 --name CITS3200_SMTP_USER --output text --query "Parameter.Value")"
SMTP_PASSWORD="$(aws ssm get-parameter --region ap-southeast-2 --name CITS3200_SMTP_USER --output text --query "Parameter.Value")"

#docker run -d --rm -p 5432:5432 -v pgsql-data:/var/lib/postgresql/data -e POSTGRES_DB=django -e POSTGRES_USER=django -e POSTGRES_PASSWORD=password postgres:13-alpine
#docker run -d --rm -p 
docker run -d --rm -e SMTP_HOST=$SMTP_HOST -e SMTP_USER=$SMTP_USER -e SMTP_PASSWORD=$SMTP_PASSWORD \
    -p 80:8000 strep-a-database:latest
