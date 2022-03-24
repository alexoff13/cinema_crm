#!/usr/bin/env bash

export PYTHONUNBUFFERED=TRUE
gunicorn -b 0.0.0.0:8050 --preload --workers 32 --threads 8 -t 600 -R manage:app
