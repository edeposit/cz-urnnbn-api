#! /usr/bin/env bash
#
export PYTHONPATH="src:$PYTHONPATH"
export TEST_PATH="tests"
export ARGS=`echo $@ | sed 's/\-a//g;s/\-i//g;s/\-u//g'`

function show_help {
    echo -e "Usage: $0 [-h] [-a] [-i] [-u]"
    echo
    echo -e "\t-h"
    echo -e "\t\tShow this help."
    echo -e "\t-a"
    echo -e "\t\tRun all tests."
    echo -e "\t-i"
    echo -e "\t\tRun integration test (requires sudo)."
    echo -e "\t-u"
    echo -e "\t\tRun unittest."
    echo
    exit;
}

function run_all_tests {
    py.test $TEST_PATH $@;
    exit
}

function run_int_tests {
    py.test "$TEST_PATH/integration" $ARGS;
    exit
}

function run_unit_tests {
    py.test "$TEST_PATH/unit" $ARGS;
    exit
}

while getopts "haiu" optname; do
    case "$optname" in
        "a")
            run_all_tests;
        ;;
        "i")
            run_int_tests;
        ;;
        "u")
            run_unit_tests;
        ;;
        "h")
            show_help;
        ;;
        "?")
            echo "Unknown option $OPTARG"
        ;;
        ":")
            echo "No argument value for option $OPTARG"
        ;;
        *)
            echo "Unknown error while processing options"
        ;;
    esac
done

show_help;