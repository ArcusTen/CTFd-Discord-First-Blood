#!/bin/bash

docker build -t discord-bot .

docker run -d --name discord-bot-container  discord-bot