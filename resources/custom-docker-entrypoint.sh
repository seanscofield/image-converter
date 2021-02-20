#!/usr/bin/env bash

if [ "$ENV" = "LOCAL" ]; then
    echo "Sleeping for 30 seconds to give localstack time to spin up services..."
    sleep 30;
fi

echo "running application..."
image_converter
