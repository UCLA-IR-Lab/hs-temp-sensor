#! /usr/bin/bash

short_opt_str=':vrih'
long_opt_str=':verbose,reset,id,temp,test,help'

VALID_ARGS=$(getopt -o "$short_opt_str" -l "$long_opt_str" -- "$@")
if [ $? -ne 0 ]; then
    echo "Invalid arguments. Use -h for help."
    exit 1;
fi

eval set -- "$VALID_ARGS"
while true; do
    case "$1" in
    '-v'|'--verbose')
        COMMAND="uv run src/hs_temp_sensor -vvvv"
        break
        ;;  
    '-r'|'--reset')
        COMMAND="uv run src/hs_temp_sensor -r -vvvv"
        break
        ;;
    '-i'|'--id')
        COMMAND="uv run src/hs_temp_sensor --id -vvvv"
        break
        ;;
    '--temp')
        COMMAND="uv run src/hs_temp_sensor --temp -vvvv"
        break
        ;;
    '--test')
        COMMAND="uv run src/hs_temp_sensor --test -vvvv"
        break
        ;;
    '--')
        shift
        break
        ;;
    '-h'|'--help')
        echo "Help: deploy.sh [-v] [-r] [-h]"
        exit 0
        ;;
    esac
done

SERVER="hispec-pi"
PRECOMMANDS="source $HOME/.profile &&"
PRECOMMANDS+="cd $HOME/hs-temp-sensor &&"
PRECOMMANDS+="git pull > /dev/null 2>&1 &&"
PRECOMMANDS+="uv sync > /dev/null 2>&1 &&"

ssh $SERVER $PRECOMMANDS $COMMAND;

exit 0;