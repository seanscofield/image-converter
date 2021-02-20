import os
import time

import boto3

endpoint_url = os.environ.get('AWS_ENDPOINT_URL', None)
sqs_queue_url = os.environ['SQS_QUEUE_URL']

sqs_client = boto3.client('sqs', region_name='us-east-1', endpoint_url=endpoint_url)

def main():
    print(f"Continually polling SQS queue {sqs_queue_url}...", flush=True)
    while True:
        for message in sqs_client.receive_message(QueueUrl=sqs_queue_url).get('Messages', []):
            print(f'Received message {message["MessageId"]}', flush=True)
            sqs_client.delete_message(QueueUrl=sqs_queue_url, ReceiptHandle=message['ReceiptHandle'])
            print(f'Successfully processed message {message["MessageId"]}', flush=True)

        print('Sleeping for 3 seconds...', flush=True)
        time.sleep(3)

if __name__ == '__main__':
    main()
