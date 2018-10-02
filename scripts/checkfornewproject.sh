#!/bin/bash

set -eu
shopt -s nullglob
shopt -s expand_aliases
source ~/.bashrc

########
# VARS #
########

MAILTO=clinical-demux@scilifelab.se
MAILTO_ERR=clinical-demux@scilifelab.se
INDIR=${1?'please provide dir holding all projects'}

#############
# FUNCTIONS #
#############

log() {
    local NOW=$(date +"%Y%m%d%H%M%S")
    echo "[$NOW] $@"
}

failed() {
    echo "Error starting ${PROJECT}: $(caller)" | mail -s "ERROR starting ${PROJECT}" ${MAILTO_ERR}
}
trap failed ERR

########
# MAIN #
########

for PROJECT_DIR in ${INDIR}/*; do
    PROJECT=$(basename $PROJECT_DIR)
    if [[ ! -f ${PROJECT_DIR}/analysis_started.txt ]]; then
        log "${PROJECT}: starting!"
        mwgs project ${PROJECT_DIR}
    else
        log "${PROJECT}: already started"
    fi
done
