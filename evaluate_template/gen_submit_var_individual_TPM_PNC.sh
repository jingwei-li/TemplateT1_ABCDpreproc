#!/bin/bash

proj_dir="/data/project/template_t1"
DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

CPUS='1'
RAM='5G'
LOGS_DIR=$proj_dir/data/ABCD_datalad/code/logs/var_individual_TPM_PNC

out_dir="$proj_dir/data/ABCD_datalad/tissue_seg/figures/PNC_individual_TPMs"

# create the logs dir if it doesn't exist
[ ! -d "${LOGS_DIR}" ] && mkdir -p "${LOGS_DIR}"

# print the .submit header
printf "# The environment
universe       = vanilla
getenv         = True
request_cpus   = ${CPUS}
request_memory = ${RAM}

# Execution
initial_dir    = $DIR
executable     = /usr/bin/python3
transfer_executable   = False
\n"

printf "arguments = var_individual_TPM_PNC.py --subj_csv $proj_dir/data/PNC_LauraW/code/age9-12_AA.csv \
--outdir $out_dir --outprefix 912AA \n"
printf "log       = ${LOGS_DIR}/912AA_\$(Cluster).\$(Process).log\n"
printf "output    = ${LOGS_DIR}/912AA_\$(Cluster).\$(Process).out\n"
printf "error     = ${LOGS_DIR}/912AA_\$(Cluster).\$(Process).err\n"
printf "Queue\n\n"

printf "arguments = var_individual_TPM_PNC.py --subj_csv $proj_dir/data/PNC_LauraW/code/age9-12_EA.csv \
--outdir $out_dir --outprefix 912EA \n"
printf "log       = ${LOGS_DIR}/912EA_\$(Cluster).\$(Process).log\n"
printf "output    = ${LOGS_DIR}/912EA_\$(Cluster).\$(Process).out\n"
printf "error     = ${LOGS_DIR}/912EA_\$(Cluster).\$(Process).err\n"
printf "Queue\n\n"
