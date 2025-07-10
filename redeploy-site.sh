#!/bin/bash

# kill any existing tmux server and sessions
tmux kill-server

# go to the project directory
cd ~/mlh-pe-portfolio-site || exit 1

# update code from GitHub main branch
git fetch && git reset origin/main --hard

# enter virtual environment & install dependencies
source venv/bin/activate
pip install -r requirements.txt
deactivate

# start a new detached tmux session named deploy-site
tmux new-session -d -s deploy-site "source venv/bin/activate && flask run --host=0.0.0.0"
