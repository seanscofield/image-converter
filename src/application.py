import json
import os
import sys
import time
import traceback

import boto3
from PIL import Image

endpoint_url = os.environ.get('AWS_ENDPOINT_URL', None)
sqs_queue_url = os.environ['SQS_QUEUE_URL']

s3_client = boto3.client('s3', region_name='us-east-1', endpoint_url=endpoint_url)
sqs_client = boto3.client('sqs', region_name='us-east-1', endpoint_url=endpoint_url)


def convert_png_to_jpg(png_file_path, jpg_file_path):
    im = Image.open(png_file_path)
    im = im.convert('RGB')
    im.save(jpg_file_path, "JPEG")


def main():
    print(f"Continually polling SQS queue {sqs_queue_url}...", flush=True)
    while True:
        png_file_path, jpg_file_path = None, None
        for message in sqs_client.receive_message(QueueUrl=sqs_queue_url).get('Messages', []):
            try:
                print(f'Received message {message["MessageId"]}', flush=True)

                # Download png from s3, create jpeg from it, and upload jpeg back to S3. Note that this code isn't the best
                bucket, bucket_object = json.loads(message['Body'])['bucket'], json.loads(message['Body'])['object']
                png_file_path = f'/tmp/{bucket_object}'
                jpg_file_path = png_file_path.replace('.png', '.jpg')
                s3_client.download_file(bucket, bucket_object, png_file_path)
                convert_png_to_jpg(png_file_path, jpg_file_path)
                s3_client.upload_file(jpg_file_path, bucket, bucket_object.replace('.png', '.jpg'))
                print(f'New JPEG created from {bucket_object}: s3://{bucket}/{bucket_object.replace(".png", ".jpg")}')

                sqs_client.delete_message(QueueUrl=sqs_queue_url, ReceiptHandle=message['ReceiptHandle'])
                print(f'Successfully processed message {message["MessageId"]}', flush=True)
            except:
                print("Error encountered when trying to convert image!")
                traceback.print_exception(*sys.exc_info())
            finally:
                if png_file_path and os.path.exists(png_file_path):
                    os.remove(png_file_path)
                if jpg_file_path and os.path.exists(jpg_file_path):
                    os.remove(jpg_file_path)

        print('Sleeping for 3 seconds...', flush=True)
        time.sleep(3)

if __name__ == '__main__':
    main()
