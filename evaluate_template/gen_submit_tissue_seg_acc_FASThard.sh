#!/bin/bash

proj_dir="/data/project/template_t1"
DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

CPUS='1'
RAM='5G'
LOGS_DIR=$proj_dir/data/ABCD_datalad/code/logs/tissue_seg_acc

subj_ls="$proj_dir/data/ABCD_datalad/code/TemplateT1_ABCDpreproc/lists/subj_ls_all_rand50EA50AA_subset40x2.txt"
seg_dir="$proj_dir/data/ABCD_datalad/tissue_seg/seg_individual_native"
reg_dir="$proj_dir/data/ABCD_datalad/tissue_seg/templateTPMs_to_native"
out_dir="$proj_dir/data/ABCD_datalad/tissue_seg/dice"

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

printf "arguments = tissue_segmentation_acc_FASThard.py --subj_ls $subj_ls --seg_dir $seg_dir \
--reg_dir $reg_dir --age_min 9 --age_max 12 --race AA --out_dir $out_dir \n"
printf "log       = ${LOGS_DIR}/\$(Cluster).\$(Process).log\n"
printf "output    = ${LOGS_DIR}/\$(Cluster).\$(Process).out\n"
printf "error     = ${LOGS_DIR}/\$(Cluster).\$(Process).err\n"
printf "Queue\n\n"

printf "arguments = tissue_segmentation_acc_FASThard.py --subj_ls $subj_ls --seg_dir $seg_dir \
--reg_dir $reg_dir --age_min 9 --age_max 12 --race EA --out_dir $out_dir \n"
printf "log       = ${LOGS_DIR}/\$(Cluster).\$(Process).log\n"
printf "output    = ${LOGS_DIR}/\$(Cluster).\$(Process).out\n"
printf "error     = ${LOGS_DIR}/\$(Cluster).\$(Process).err\n"
printf "Queue\n\n"