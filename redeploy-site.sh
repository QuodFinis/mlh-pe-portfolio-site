#!/bin/bash

# go to the project directory
cd ~/mlh-pe-portfolio-site || exit 1

# update code from GitHub main branch
git fetch && git reset origin/main --hard

# give redeploy-site exec perms
chmod +x redeploy-site.sh

# build the Docker image
docker compose -f compose.prod.yaml down
docker compose -f compose.prod.yaml up -d --build