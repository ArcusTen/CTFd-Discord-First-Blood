#!/bin/bash

docker build -t discord-bot .
docker run -d --env-file .env my-python-app