#!/usr/bin/env bash

# Install system dependencies needed for compiling packages
apt-get update -y
apt-get install -y build-essential python3-dev

# Then, proceed with the normal pip install
pip install -r requirements.txt
