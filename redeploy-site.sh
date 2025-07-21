#!/bin/bash

# go to the project directory
cd ~/mlh-pe-portfolio-site || exit 1

# update code from GitHub main branch
git fetch && git reset origin/main --hard

# give redeploy-site exec perms
chmod +x redeploy-site.sh

# enter virtual environment & install dependencies
source venv/bin/activate
pip install -r requirements.txt
deactivate

# restart myportfolio service
systemctl restart myportfolio
systemctl status myportfolio