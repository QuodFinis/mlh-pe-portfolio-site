#!/bin/bash

# Enhanced redeployment script with no-op if already up-to-date
exec > >(tee -a redeploy-site.log) 2>&1

cd ~/mlh-pe-portfolio-site || exit 1

# Reset local repo to match main branch
git fetch && git reset origin/main --hard

# spin containers down to prevent out of memory issues
docker compose -f docker-compose.prod.yml down

# Rebuild and start container
docker compose -f docker-compose.prod.yml up -d --build

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
