#!/bin/bash
set -e

REQS=requirements_common.txt

VENV=ve_system
PACKS=${PWD}/packages

if [ ! -d $VENV ];then
    virtualenv $VENV_EXTRA_ARGS --no-site-packages --never-download $VENV
fi

source $VENV/bin/activate

pip install --no-index --find-links=file://$PACKS -r $REQS

