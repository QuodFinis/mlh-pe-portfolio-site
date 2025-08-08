#!/bin/bash

# Enhanced redeployment script with no-op if already up-to-date
exec > >(tee -a redeploy-site.log) 2>&1
set -e  # Exit immediately if any command fails

cd ~/mlh-pe-portfolio-site || exit 1

# Check if updates are available
git fetch
HEADHASH=$(git rev-parse HEAD)
UPSTREAMHASH=$(git rev-parse origin/main)

if [ "$HEADHASH" == "$UPSTREAMHASH" ]; then
    echo "Already up to date. Skipping redeployment."
    exit 0
fi

# Proceed with deployment
echo "New changes detected. Starting redeployment..."

# Reset to latest version
git reset --hard origin/main
chmod +x redeploy-site.sh

# Set up clean environment
if [ ! -d venv ]; then
    python -m venv venv
fi
source venv/bin/activate

# Install dependencies
pip install -U pip
pip install -r requirements.txt

# Run tests
if ! python -m unittest discover -v tests/; then
    echo "Tests failed. Reverting changes."
    git reset --hard "$HEADHASH"  # Revert to previous commit
    deactivate
    rm -rf venv
    exit 1
fi

# Clean up
deactivate
rm -rf venv

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