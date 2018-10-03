#!/usr/bin/env bash

shopt -s nullglob
shopt -s expand_aliases
source ${HOME}/.bashrc
source ${HOME}/servers/resources/activate-prod.sh
set -eu

########
# VARS #
########

INDIR=${1?'please provide dir holding all projects'}

#############
# FUNCTIONS #
#############

log() {
    local NOW=$(date +"%Y%m%d%H%M%S")
    echo "[$NOW] $@"
}

########
# MAIN #
########

for PROJECT_DIR in ${INDIR}/*; do
    PROJECT=$(basename $PROJECT_DIR)
    if [[ -d ${PROJECT_DIR} && ! -f ${PROJECT_DIR}/analysis_started.txt ]]; then
        log "${PROJECT}: starting!"
        mwgs project ${PROJECT_DIR}
        date > ${PROJECT_DIR}/analysis_started.txt
    else
        log "${PROJECT}: already started"
    fi
done
