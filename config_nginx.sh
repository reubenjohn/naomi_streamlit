#!/bin/bash

# Check if the port argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <port>"
  exit 1
fi

port=$1

# Define the source and destination paths
SOURCE="./nginx.conf"
DESTINATION="/etc/nginx/conf.d/streamlit_api.conf"

# Replace __PORT__ with the provided port argument
sed "s/__PORT__/$port/g" $SOURCE > /tmp/nginx_temp.conf

# Copy the modified nginx configuration file to the destination
sudo cp /tmp/nginx_temp.conf $DESTINATION

echo "Nginx configuration has been updated:"

echo

cat "$DESTINATION"
