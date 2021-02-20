#!/usr/bin/env bash
# SQS SETUP
set -x  # turn on and off outputting of the commands being executed

awslocal sqs create-queue --queue-name image_converter

# S3 setup
awslocal s3 mb s3://images
set +x