#!/bin/bash

# default parameters
proj_dir="/data/project/template_t1"
in_dir="$proj_dir/data/ABCD_datalad/preprocessed/PNCAA912/freesurfer"
out_dir="$proj_dir/data/ABCD_datalad/tissue_seg/seg_individual_native"

main() {
    # convert mgz file to nifti
    mgz="$in_dir/$s/mri/brain.mgz"
    mkdir -p $out_dir/$s
    nii="$out_dir/$s/reconall_brain.nii.gz"
    if [ ! -f $nii ]; then
        mri_convert $mgz $nii
    fi

    # fast
    base=$out_dir/$s/reconall_brain_fast
    fast -g -o ${base} -n 3 $nii 
}


# usage
usage() { echo "
NAME:
    tissue_segment_fast.sh

DESCRIPTION:
    Use FSL FAST to segment individual brain in native space.

OPTIONAL ARGUMENTS:
    -h            : Print help.
    -i <in_dir>   : Input directory which contains the freesurfer recon-all processed, 
                    skull-striped individual T1 brains. Default:
                    $in_dir
    -o <out_dir>  : Output directory which will store the segmented brain tissues in 
                    native space. Default:
                    $out_dir
    -s <s>        : Subject ID.

" 1>&2; exit 1; }

# input arguments
while [[ $# -gt 0 ]]; do
    flag=$1; shift;

    case $flag in
        -h) usage; exit;;
        -i) in_dir=$1; shift;;
        -o) out_dir=$1; shift;;
        -s) s=$1; shift;;
        *) echo "Unknown flag: $flag"
           usage; 1>&2; exit 1;;
    esac
done

arg1err() {
	echo "ERROR: flag $1 requires one argument"
	exit 1
}

if [ -z "$in_dir" ]; then
	arg1err "-i"
fi
if [ -z "$out_dir" ]; then
	arg1err "-o"
fi
if [ -z "$s" ]; then
	arg1err "-s"
fi

main