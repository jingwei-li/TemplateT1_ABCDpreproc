#!/bin/bash

# get the directory of current script, use this to get the directory of the code repository on any machine
code_dir=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)

# Default parameters
data_dir='/data/project/template_t1/data/ABCD_datalad/inm7-superds/original/abcd'
N=10
seed=42

main() {
    # collect all subject IDs available and write them to a full subject list text file in this repository.
    cd $data_dir
    subjects=( $(find . -maxdepth 1 -type d -name "sub-NDARINV*" -exec basename {} \;) )
    mkdir -p $code_dir/lists
    printf "%s\n" "${subjects[@]}" > $code_dir/lists/subj_ls_all.txt

    # select random N (=10) lines from the full subject list and write into another list
    shuf -n $N --random-source=<(get_seeded_random $seed) \
        $code_dir/lists/subj_ls_all.txt > $code_dir/lists/subj_ls_rand$N.txt
}

# setup random seed
get_seeded_random() {
    seed="$1"
    openssl enc -aes-256-ctr -pass pass:"$seed" -nosalt \
        </dev/zero 2>/dev/null
}

# usage
usage() { echo "
NAME:
    rand_select_subj.sh

DESCRIPTION:
    Randomly select \$N (specified by -n argument) subjects from all available subject IDs under the datalad dataset.
    These randomly selected subjects are used for trying out different versions of preprocessing pipelines.

OPTIONAL ARGUMENTS:
    -h            : Print help.
    -d <data_dir> : BIDS directory of original dataset. Default:
                    $data_dir
    -n <N>        : Number of subjects selected.
    -s <seed>     : Pass in a random seed for replication purpose. Default: $seed.

" 1>&2; exit 1; }

# input arguments
while [[ $# -gt 0 ]]; do
    flag=$1; shift;

    case $flag in
        -h) usage; exit;;
        -d) data_dir=$1; shift;;
        -n) N=$1; shift;;
        -s) seed=$1; shift;;
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
if [ -z "$N" ]; then
	arg1err "-n"
fi
if [ -z "$seed" ]; then
	arg1err "-s"
fi

main
