# Overview

This is an example application intended to demonstrate how to easily develop and test an AWS-based application locally. When this application runs, it will continually poll an Amazon SQS queue whose messages should contain the path to a PNG file stored in Amazon S3. Upon receiving a message from the queue, the app will proceed to download that PNG file, convert it, and then upload the resulting JPEG file to a different location in S3.

## Requirements

* `python` (only Python 3.x is supported)
* `pip` (python package manager)
* `Docker`

## Running this application

#### Running using Docker

This repo contains a _Makefile_ with some helpful commands to build and run this application directly on one's computer:

* `make` - Packages this application into a docker image
* `make deploy` - Spins up a docker container from the built image. Also spins up a [localstack](https://github.com/localstack/localstack/blob/master/README.md) docker container (a fully functional local AWS cloud stack), and creates the SQS queue and S3 bucket that our application will leverage (note that some users will need to run `docker swarm init` before this deploy will work; also note that it could take up to 30 seconds for everything to start up)
* `make clean` - Tears down all of the docker containers

In order to interact with this application once it's up and running, refer to the "Interacting with this application" section further down in the README.

#### Running directly with Python

For anyone looking to run this application directly with python, it can be installed by running the following command from within the top-level directory of this repo:

```
pip install .
```

Before you start running the application, however, you'll need to make sure that _localstack_ and our SQS/S3 resources have been spun up. The easiest way to do this is by running `docker-compose up -d localstack`, which, as touched upon in the previous section, will spin up a [localstack](https://github.com/localstack/localstack/blob/master/README.md) docker container (again, note that it could take up to 30 seconds for localstack to boot up all the way).

At this point, you'll have to set up some fake AWS credentials and other environment variables needed by our application:

```
# Initialize fake AWS credentials and other environment variables
export AWS_ACCESS_KEY_ID=foo
export AWS_SECRET_ACCESS_KEY=bar
export SQS_QUEUE_URL=http://localhost:4566/000000000000/image_converter
export AWS_ENDPOINT_URL=http://localhost:4566
export LOCAL_DEVELOPMENT=True
```

And now you're ready to go! You can either run:

```
python src/application.py
```

or use the script that was installed as part of the earlier _pip install:_

```
image_converter
```

## Interacting with this application (during local development)

Once you've gotten things up and running, the application will continuously poll an SQS queue in localstack for messages containing the S3 path to a png file awaiting conversion. You can upload an example png file and send a message to the SQS queue using the following commands:

```
export AWS_ACCESS_KEY_ID=foo
export AWS_SECRET_ACCESS_KEY=bar
aws --endpoint-url https://localhost:4566 s3 cp resources/example.png s3://images/ --no-verify-ssl
aws --endpoint-url http://localhost:4566 sqs send-message --message-body "{\"bucket\": \"images\", \"object\": \"example.png\"}" --queue-url http://localhost:4566/queue/image_converter --region us-east-1
```

Upon running both of those ^ commands, you should be able to see the application spit out a jpeg file to the **images** S3 bucket in localstack, e.g.:
```
C02WW05LJG5J:image-converter sescofield$ aws --endpoint-url https://localhost:4566 s3 ls s3://images/ --no-verify-ssl
2021-02-20 01:20:12      47365 example.jpg
2021-02-20 01:16:40     497762 example.png
```

## Future updates
- Add an event notification configuration to our localstack S3 bucket to automatically trigger an SQS message whenever a new png file is uploaded
