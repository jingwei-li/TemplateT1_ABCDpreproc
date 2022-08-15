import argparse, os
import nibabel as nib 
import numpy as np 

parser = argparse.ArgumentParser()
parser.add_argument('--subj_ls', help='List of subject in either AA or EA groups who passed fmriprep.')
parser.add_argument('--seg_dir', help='The directory which contains individual brains\' segmentation in native space.')
parser.add_argument('--space', help='Name of brain template.')
parser.add_argument('--threshold', help='Threshold to cutoff tissue probability maps.')
parser.add_argument('--out_csv', help='Output CSV file which will contain the tissue segmentation accuracies.')
args = parser.parse_args()

with open(args.subj_ls) as file:
    subjects = file.readlines()
    subjects = [line.rstrip() for line in subjects]

ses = 'ses-baselineYear1Arm1'
for s in subjects:
    # FAST segmented tissues of each subject in native space [0-CSF 1-GM 2-WM]
    fast_seg0 = nib.load(os.path.join(seg_dir, s, 'reconall_brain_fast_pve_0.nii.gz'))
    fast_seg1 = nib.load(os.path.join(seg_dir, s, 'reconall_brain_fast_pve_1.nii.gz'))
    fast_seg2 = nib.load(os.path.join(seg_dir, s, 'reconall_brain_fast_pve_2.nii.gz'))
    gt0 = fast_seg0.get_fdata()
    gt1 = fast_seg1.get_fdata()
    gt2 = fast_seg2.get_fdata()

    # transform template TPMs to individual native space