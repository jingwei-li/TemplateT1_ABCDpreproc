#!/bin/bash
DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

main() {
    mkdir -p $out_dir

    # loop over white matter, grey matter, and CSF
    for tissue in 1 2 3; do
        in=$TPMdir/age9-12_${grp}_TMP${tissue}.nii
        ref=$ref_dir/reconall_brain.nii.gz

        # flirt
        aff=$out_dir/flirt_affine.mat
        flirt -ref $ref -in $in -omat $aff

        # fnirt
        iout=$out_dir/age9-12_${grp}_TMP${tissue}_to_reconall_brain.nii.gz
        cout=$out_dir/age9-12_${grp}_TMP${tissue}_warpcoef.nii.gz
        fout=$out_dir/age9-12_${grp}_TMP${tissue}_warpfield.nii.gz
        cnf=$DIR/fnirt_template2native.cnf
        fnirt --in=$in --ref=$ref --iout=$iout --cout=filename --fout=$fout --aff=$aff --config=$cnf -v
    done
}

# usage
usage() { echo "
NAME:
    fnirt_TemplateTPMs2native.sh

DESCRIPTION:
    Use FSL FLIRT and FNIRT to register template's tissue probability 
    maps (TPMs) to a subject's native space.

OPTIONAL ARGUMENTS:
    -h                 : Print help.
    -g <grp>     : Group: AA (African American) or EA (European American)
    -t <TPMdir>  : Directory containing the new template's TPMs.
    -r <ref_dir> : Directory containing the reference image of each 
                   individual subject. For example, it could be the 
                   output folder of 'tissue_segment_fast.sh'.
    -o <out_dir> : Output directory.
    -s <s>       : Subject ID.

" 1>&2; exit 1; }

# input arguments
while [[ $# -gt 0 ]]; do
    flag=$1; shift;

    case $flag in
        -h) usage;      exit;;
        -g) grp=$1;     shift;;
        -t) TPMdir=$1;  shift;;
        -r) ref_dir=$1; shift;;
        -o) out_dir=$1; shift;;
        -s) s=$1;       shift;;
        *) echo "Unknown flag: $flag"
           usage; 1>&2; exit 1;;
    esac
done

arg1err() {
	echo "ERROR: flag $1 requires one argument"
	exit 1
}

if [ -z "$grp" ]; then
    arg1err "-g"
fi
if [ -z "$TPMdir" ]; then
	arg1err "-TPMdir"
fi
if [ -z "$ref_dir" ]; then
	arg1err "-ref_dir"
fi
if [ -z "$out_dir" ]; then
	arg1err "-out_dir"
fi
if [ -z "$s" ]; then
	arg1err "-s"
fi

main
