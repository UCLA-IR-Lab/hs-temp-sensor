#! /usr/bin/bash

while getopts ":vrh" OPTARG; do
    case $OPTARG in
    v)
        COMMAND="uv run src/hs_temp_sensor -vvvv"
        ;;  
    r)
        COMMAND="uv run src/hs_temp_sensor -r -vvvv"
        ;;
    h)
        echo "Help: deploy.sh [-v] [-r] [-h]"
        exit 0
        ;;
    \?)
        echo "Invalid option: -$OPTARG" >&2
        exit 1
        ;;
    esac
done

SERVER="hispec-pi"
PRECOMMANDS="source $HOME/.profile &&"
PRECOMMANDS+="cd $HOME/hs-temp-sensor &&"
PRECOMMANDS+="git pull > /dev/null 2>&1 &&"
PRECOMMANDS+="uv sync > /dev/null 2>&1 &&"

ssh $SERVER $PRECOMMANDS $COMMAND;

exit;