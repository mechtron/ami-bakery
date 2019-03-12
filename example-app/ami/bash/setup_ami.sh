#!/usr/bin/env bash

sudo apt-get -y update

# Install common apps
sudo apt-get install -y logrotate jq ntp htop iftop

# Install Python 3
sudo apt-get install -y software-properties-common python3-pip

# Bootstrap script permissions
sudo chmod +x /opt/bootstrap/bootstrap.py

echo "Hi"

