#!/bin/bash

proj_dir='/data/project/template_t1'
DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

CPUS='1'
RAM='5G'
LOGS_DIR=$proj_dir/data/ABCD_datalad/code/logs/tissue_seg_fast

subj_ls="$proj_dir/data/ABCD_datalad/code/TemplateT1_ABCDpreproc/lists/subj_ls_all_rand50EA50AA_subset40x2.txt"
in_dir="$proj_dir/data/ABCD_datalad/preprocessed/PNCEA912/freesurfer"
out_dir="$proj_dir/data/ABCD_datalad/tissue_seg/seg_individual_native_reconall_EA"

# create the logs dir if it doesn't exist
[ ! -d "${LOGS_DIR}" ] && mkdir -p "${LOGS_DIR}"

# print the .submit header
printf "# The environment
universe       = vanilla
getenv         = True
request_cpus   = ${CPUS}
request_memory = ${RAM}

# Execution
initial_dir    = $proj_dir
executable     = $DIR/tissue_segment_fast.sh
\n"

# loop over all subjects
#for sub in $(cat $subj_ls); do
for sub in sub-NDARINVW0VV53Y4; do
    printf "arguments = -s $sub -i $in_dir -o $out_dir \n"
    printf "log       = ${LOGS_DIR}/\$(Cluster).\$(Process).${sub}.log\n"
    printf "output    = ${LOGS_DIR}/\$(Cluster).\$(Process).${sub}.out\n"
    printf "error     = ${LOGS_DIR}/\$(Cluster).\$(Process).${sub}.err\n"
    printf "Queue\n\n"
done