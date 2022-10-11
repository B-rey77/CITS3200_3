#!/bin/bash

# This bash script is used during the DeployCode stage of
# the pipeline. The AWS CodeDeploy agent uses this script to
# run the Docker container on the EC2 instance

export SMTP_HOST="$(aws ssm get-parameter --region ap-southeast-2 --name CITS3200_SMTP_HOST --output text --query "Parameter.Value")"
export SMTP_USER="$(aws ssm get-parameter --region ap-southeast-2 --name CITS3200_SMTP_USER --output text --query "Parameter.Value")"
export SMTP_PASSWORD="$(aws ssm get-parameter --region ap-southeast-2 --name CITS3200_SMTP_PASSWORD --with-decryption --output text --query "Parameter.Value")"
export DJANGO_HOSTNAME="$(aws ssm get-parameter --region ap-southeast-2 --name CITS3200_HOSTNAME --output text --query "Parameter.Value")"
export ADMIN_EMAIL="$(aws ssm get-parameter --region ap-southeast-2 --name CITS3200_ADMIN_EMAIL --output text --query "Parameter.Value")"
#export ADMIN_PASSWORD="$(aws ssm get-parameter --region ap-southeast-2 --name CITS3200_ADMIN_PASSWORD --with-decryption --output text --query "Parameter.Value")"
export LETS_ENCRYPT_EMAIL=$ADMIN_EMAIL
export DJANGO_DEBUG=0
#docker run -d --rm -p 5432:5432 -v pgsql-data:/var/lib/postgresql/data -e POSTGRES_DB=django -e POSTGRES_USER=django -e POSTGRES_PASSWORD=password postgres:13-alpine
#docker run -d --rm -p 
#docker run -d --rm -e SMTP_HOST=$SMTP_HOST -e SMTP_USER=$SMTP_USER -e SMTP_PASSWORD=$SMTP_PASSWORD \
    #-p 80:80 -p 443:443 strep-a-database:latest


cd /tmp/webapp
docker-compose up -d