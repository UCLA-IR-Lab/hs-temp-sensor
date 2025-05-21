#! /usr/bin/bash

SERVER="hispec-pi"
COMMANDS="source $HOME/.profile &&"
COMMANDS+="cd $HOME/hs-temp-sensor &&"
COMMANDS+="git pull > /dev/null 2>&1 &&"
COMMANDS+="uv sync > /dev/null 2>&1 &&"
# COMMANDS+="source .venv/bin/activate &&"
COMMANDS+="uv run src/hs_temp_sensor"

ssh $SERVER $COMMANDS;

exit;