#!/bin/bash

data_dir='/data/project/template_t1/data/ABCD_datalad/inm7-superds/original/abcd'
# Default only download json files to avoid accidentally downloading 
#     all NIFTI files which takes too much space
json_only=1
subj_ls=""

main() {
    cd $data_dir
    # get subject IDs
    if [ -z "$subj_ls" ]; then
        subjects=( $(find . -maxdepth 1 -type d -name "sub-NDARINV*" -exec basename {} \;) )
    else
        subjects=$(cat $subj_ls)
    fi
    echo $subjects

    # general `datalad get` command & get top-level json files
    cmd="datalad get -s inm7-storage"
    eval "$cmd task-rest_bold.json"
    eval "$cmd dataset_description.json"

    ses='ses-baselineYear1Arm1'
    for sid in $subjects; do
        # get information of subject sub-dataset
        eval "$cmd -n $sid"

        # generate file lists necessary for fmriprep
        if [ "$json_only" == "1" ]; then
            flist="anat/${sid}_${ses}_*T1w.json anat/${sid}_${ses}_*T2w.json \
dwi/${sid}_${ses}_*dwi.json fmap/${sid}_${ses}_acq-dwi_dir-*_epi.json"
        else
            flist="anat/${sid}_${ses}_*T1w.json anat/${sid}_${ses}_*T2w.json dwi/${sid}_${ses}_dwi.json \
fmap/${sid}_${ses}_acq-dwi_dir-*_epi.json anat/${sid}_${ses}_*T1w.nii.gz anat/${sid}_${ses}_*T2w.nii.gz"
        fi

        if [ -L $sid/$ses/func/${sid}_${ses}_task-rest_bold.nii.gz ]; then
            flist="$flist func/${sid}_${ses}_task-rest_bold.json"
            if [ "$json_only" != "0" ]; then
                flist="$flist func/${sid}_${ses}_task-rest_bold.nii.gz"
            fi
        fi
        for run in {01..06}; do # maximal 4 fMRI runs
            if [ -L $sid/$ses/func/${sid}_${ses}_task-rest_run-${run}_bold.nii.gz ]; then
                flist="$flist func/${sid}_${ses}_task-rest_run-${run}_bold.json"
                if [ "$json_only" != "0" ]; then
                    flist="$flist func/${sid}_${ses}_task-rest_run-${run}_bold.nii.gz"
                fi
            fi
        done
        echo $flist

        # download every file in the list
        for f in $flist; do
            eval "$cmd $sid/$ses/$f"
        done
    done
}

# usage
usage() { echo "
NAME:
    datalad_get_files.sh

DESCRIPTION:
    Install sub-dataset of individual subject. Download necessary .json and .nii.gz files for fmriprep.

ARGUMENTS:
    -h            : Print help.
    -d <data_dir> : BIDS directory of original dataset. Default:
                    $data_dir
    -s <subj_ls>  : Absolute path of subject list.
    -a            : If this flag is not used, only .json files will be downloaded. If used, NIFTI files 
                    will also be downloaded.
" 1>&2; exit 1; }

# parse arguments
while [[ $# -gt 0 ]]; do
    flag=$1; shift;

    case $flag in
        -h) usage; exit;;
        -d) data_dir=$1; shift;;
        -s) subj_ls=$1; shift;;
        -a) json_only=0; ;;
        *) echo "Unknown flag: $flag"
           usage; 1>&2; exit 1;;
    esac
done

arg1err() {
	echo "ERROR: flag $1 requires one argument"
	exit 1
}

if [ -z "$data_dir" ]; then
	arg1err "-d"
fi
if [ -z "$subj_ls" ]; then
	arg1err "-s"
fi

main