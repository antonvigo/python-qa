#!/bin/bash
export PYTHONPATH="$HOME/qa-system/lib:$HOME/qa-system"
export PATH="$PATH:$HOME/tmp/apache-jmeter-5.3/bin"

mv ./.pylintrc ~/

sudo apt install -y jq python3-pip pylint
