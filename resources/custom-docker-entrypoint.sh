#!/usr/bin/env bash

if [ "$ENV" = "LOCAL" ]; then
    echo "Sleeping for 20 seconds to give localstack time to spin up services..."
    sleep 20;
fi

echo "running application..."
image_converter
