# Create SQS queue
awslocal sqs create-queue --queue-name image_converter

# Create S3 bucket
awslocal s3 mb s3://images
