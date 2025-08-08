#!/bin/bash

# Enhanced redeployment script with no-op if already up-to-date
exec > >(tee -a redeploy-site.log) 2>&1
set -e  # Exit immediately if any command fails

cd ~/mlh-pe-portfolio-site || exit 1

# Check if updates are available
git fetch
HEADHASH=$(git rev-parse HEAD)
UPSTREAMHASH=$(git rev-parse origin/main)

# Docker deployment
sudo docker compose -f compose.prod.yaml down
sudo docker compose -f compose.prod.yaml up -d --build

# Warm up server
echo "Waiting for server to start..."
for i in {1..10}; do
    if curl -s http://localhost:5000/ >/dev/null; then
        echo "Server is up and running!"
        exit 0
    fi
    sleep 3
done

echo "Server failed to start properly"
exit 1