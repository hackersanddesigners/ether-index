#!/bin/bash

gunicorn main:app \
         --log-level DEBUG \
         --reload \
         --workers 4 \
         --worker-class uvicorn.workers.UvicornWorker \
         --bind 127.0.0.1:44777
