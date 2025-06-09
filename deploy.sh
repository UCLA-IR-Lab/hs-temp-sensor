#! /usr/bin/bash

short_opt_str=':vd:rih'
long_opt_str=':verbose,device:,reset,id,temp,test,rtd,sd,help'

VALID_ARGS=$(getopt -o "$short_opt_str" -l "$long_opt_str" -- "$@")
if [ $? -ne 0 ]; then
    echo "Invalid arguments. Use -h for help."
    exit 1;
fi
 
OPT=""
eval set -- "$VALID_ARGS"
while true; do
    case "$1" in
    '-v'|'--verbose')
        VERBOSE=true
        # break
        shift
        ;;
    '-d'|'--device')
        DEVICE="-d $2"
        # break
        shift 2
        ;;
    '-r'|'--reset')
        OPT+="-r"
        # break
        shift
        ;;
    '-i'|'--id')
        OPT+="--id"
        # break
        shift
        ;;
    '--temp')
        OPT+="--temp"
        # break
        shift
        ;;
    '--read')
        OPT+="--read"
        # break
        shift
        ;;
    '--test')
        OPT+="--test"
        # break
        shift
        ;;
    '--rtd')
        OPT+=" --rtd"
        # break
        shift
        ;;
    '--sd')
        OPT+=" --sd"
        # break
        shift
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

if [ "$VERBOSE" = true ]; then
    COMMAND="uv run src/hs_temp_sensor -vvvv $DEVICE $OPT"
else
    COMMAND="uv run src/hs_temp_sensor $DEVICE $OPT"
fi

ssh $SERVER $PRECOMMANDS $COMMAND;

exit 0;