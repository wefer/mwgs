#!/usr/bin/env bash 
PROJECT=${1?Please provide projectID!}
shopt -s expand_aliases
source ${HOME}/.aliases
for DIR in /mnt/hds/proj/bioinfo/MICROBIAL/projects/${PROJECT}/M*
do echo $DIR
echo "mwgs add $DIR/statistics.yml"
mwgs add $DIR/statistics.yml
done
