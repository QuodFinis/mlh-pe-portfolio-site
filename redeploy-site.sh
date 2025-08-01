#!/bin/bash

exec > >(tee -a redeploy-site.log) 2>&1

# go to the project directory
cd ~/mlh-pe-portfolio-site || exit 1

# update code from GitHub main branch
git fetch && git reset origin/main --hard

# install dependencies and check if tests pass
pip install -r requirements.txt
if ! python -m unittest discover -v tests/; then
    echo "Tests failed. Exiting redeployment."
    exit 1
fi

# undo code update and dependencies if tests fail to revert back to previous state
git reset --hard HEAD@{1}

# if tests pass deactivate and remove venv and pip installed packages
if [ -d venv ]; then
    deactivate
    rm -rf venv
fi

# give redeploy-site exec perms
chmod +x redeploy-site.sh

# build the Docker image
docker compose -f compose.prod.yaml down
docker compose -f compose.prod.yaml up -d --build