#!/bin/bash

# default parameters
proj_dir="/data/project/template_t1"
subj_ls="$proj_dir/data/ABCD_datalad/code/TemplateT1_ABCDpreproc/lists/subj_ls_all_rand50EA50AA_subset10x2.txt"

main() {
    for tpl in Template_912AA Template_912EA; do
        case $tpl in
            Template_912AA) prefix=age9-12_AA;;
            Template_912EA) prefix=age9-12_EA;;
            *) echo "Unrecognized template name: $tpl"
            exit 1;;
        esac

        for s in $(cat $subj_ls); do
            for type in 1 2 3; do
                for t in $(seq 0 0.1 0.9); do
                    if [[ $t == 0.0 || $t == 0 ]]; then t=0.; fi
                    v=$thresholded_dir/$tpl/$s/thresholded/${prefix}_TMP${type}_to_reconall_brain_th${t}_overlap_gt.nii
                    mkdir -p $thresholded_dir/$tpl/figures
                    p=$thresholded_dir/$tpl/figures/${s}_TMP${type}_overlap_gt_th${t}
                    if [ ! -f ${p}_z.png ]; then
                        freeview -v ${v}:colormap=lut -viewport x -ss ${p}_x.png 
                        freeview -v ${v}:colormap=lut -viewport y -ss ${p}_y.png
                        freeview -v ${v}:colormap=lut -viewport z -ss ${p}_z.png
                    fi
                done
            done
        done
    done
}

# usage
usage() { echo "
NAME:
    freeview_thresholded_seg.sh

DESCRIPTION:
    Visualize the overlap between grount-truth tissue segmentations and registered 
    template TPMs at different thresholds.

OPTIONAL ARGUMENTS:
    -h                   : Print help.
    -d <thresholded_dir> : The directory which contains the .nii files storing the 
                           overlap between thresholded ground-truth individual 
                           segmentations and thresholded template TPMs.
    
    -s <subj_ls>         : Subject list. Default: $subj_ls

" 1>&2; exit 1; }

# input arguments
while [[ $# -gt 0 ]]; do
    flag=$1; shift;

    case $flag in
        -h) usage; exit;;
        -d) thresholded_dir=$1; shift;;
        -s) subj_ls=$1; shift;;
        *) echo "Unknown flag: $flag"
           usage; 1>&2; exit 1;;
    esac
done

arg1err() {
	echo "ERROR: flag $1 requires one argument"
	exit 1
}

if [ -z "$thresholded_dir" ]; then
	arg1err "-d"
fi

main
