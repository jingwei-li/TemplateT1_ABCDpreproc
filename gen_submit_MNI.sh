#!/bin/bash
# v1.3

proj_dir='/data/project/template_t1'

CPUS='1'
RAM='8G'
DISK='90G'
LOGS_DIR="$proj_dir/data/ABCD_datalad/code/logs/fmriprep"

FMRIPREP='/data/project/singularity/fmriprep-20.2.0.simg'
WORK_DIR='/tmp'
BIDS_DIR="$proj_dir/data/ABCD_datalad/inm7-superds/original/abcd"
OUTPUT_DIR="$proj_dir/data/ABCD_datalad/preprocessed/MNI152NLin6Asym"

subj_ls="$proj_dir/data/ABCD_datalad/code/TemplateT1_ABCDpreproc/lists/subj_ls_rand10.txt"

# create the logs dir if it doesn't exist
[ ! -d "${LOGS_DIR}" ] && mkdir -p "${LOGS_DIR}"

# print the .submit header
printf "# The environment
universe       = vanilla
getenv         = True
request_cpus   = ${CPUS}
request_memory = ${RAM}
request_disk   = ${DISK}

# Execution
initial_dir    = \$ENV(HOME)/htcondor-templates/fmriprep
executable     = /usr/bin/singularity
\n"

# loop over all subjects
for sub in $(cat $subj_ls); do
#for sub in 003RTV85; do
    #sub="sub-NDARINV${sub}"
    printf "arguments = run --cleanenv -B ${WORK_DIR},${BIDS_DIR},${OUTPUT_DIR},/opt/freesurfer/6.0/license.txt:/opt/freesurfer/license.txt \
                        ${FMRIPREP} \
                        --n_cpus ${CPUS} \
                        --skull-strip-fixed-seed \
                        --work-dir ${WORK_DIR} \
                        ${BIDS_DIR} ${OUTPUT_DIR} participant \
                        --participant-label ${sub} --skip-bids-validation \
                        -t rest --output-spaces MNI152NLin6Asym \
                        --md-only-boilerplate --skull-strip-fixed-seed \
                        --fd-spike-threshold 0.5 --dvars-spike-threshold 1.5\n"
    printf "log       = ${LOGS_DIR}/\$(Cluster).\$(Process).${sub}.log\n"
    printf "output    = ${LOGS_DIR}/\$(Cluster).\$(Process).${sub}.out\n"
    printf "error     = ${LOGS_DIR}/\$(Cluster).\$(Process).${sub}.err\n"
    printf "Queue\n\n"
done
