#!/bin/bash

proj_dir='/data/project/template_t1'
DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

CPUS='1'
RAM='5G'
LOGS_DIR=$proj_dir/data/ABCD_datalad/code/logs/templateTPMs_to_native
# create the logs dir if it doesn't exist
[ ! -d "${LOGS_DIR}" ] && mkdir -p "${LOGS_DIR}"

subj_ls="$proj_dir/data/ABCD_datalad/code/TemplateT1_ABCDpreproc/lists/subj_ls_all_rand50EA50AA_subset40x2.txt"

# print the .submit header
printf "# The environment
universe       = vanilla
getenv         = True
request_cpus   = ${CPUS}
request_memory = ${RAM}

# Execution
initial_dir    = $proj_dir
executable     = $DIR/fnirt_TemplateTPMs2native.sh
\n"

# loop over two custom templates
for grp in AA EA; do
    TPMdir="$proj_dir/data/PNC_LauraW/Templates/Template_912$grp"
    # loop over all subjects
    for s in $(cat $subj_ls); do
        ref_dir="$proj_dir/data/ABCD_datalad/tissue_seg/seg_individual_native_reconall_EA/$s"
        out_dir="$proj_dir/data/ABCD_datalad/tissue_seg/templateTPMs_to_native_reconall_EA/Template_912$grp/$s"
        printf "arguments = -s $s -g $grp -t $TPMdir -r $ref_dir -o $out_dir \n"
        printf "log       = ${LOGS_DIR}/\$(Cluster).\$(Process).${s}.log\n"
        printf "output    = ${LOGS_DIR}/\$(Cluster).\$(Process).${s}.out\n"
        printf "error     = ${LOGS_DIR}/\$(Cluster).\$(Process).${s}.err\n"
        printf "Queue\n\n"
    done
done