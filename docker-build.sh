#!/bin/bash

docker build -t discord-bot .

docker run -d --name my-discord-con --env-file ./app/.env discord-bot