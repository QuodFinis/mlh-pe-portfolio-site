#!/bin/bash

exec > >(tee -a redeploy-site.log) 2>&1

cd ~/mlh-pe-portfolio-site || exit 1

git fetch && git reset origin/main --hard

chmod +x redeploy-site.sh

if [ ! -d venv ]; then
    python -m venv venv
fi

source venv/bin/activate

pip install -r requirements.txt

if ! python -m unittest discover -v tests/; then
    echo "Tests failed. Exiting redeployment."
    deactivate
    git reset --hard HEAD@{1}
    rm -rf venv
    exit 1
fi

deactivate
rm -rf venv

docker compose -f compose.prod.yaml down
docker compose -f compose.prod.yaml up -d --build