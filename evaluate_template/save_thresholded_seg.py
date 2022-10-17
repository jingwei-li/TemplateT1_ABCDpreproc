# save thresholded ground-truth segmentations and thresholded template TPMs

import argparse, os
import nibabel as nib
import numpy as np

parser = argparse.ArgumentParser(description='save thresholded ground-truth segmentations and thresholded template TPMs to NIFTI files.')
parser.add_argument('--subj_ls', help='List of subject in test sets.')
parser.add_argument('--seg_dir', help='The directory which contains individual brain\'s segmentation in native space.')
parser.add_argument('--reg_dir', help='The directory which contains the template\'s TPMs registered to individual\'s native space.')
parser.add_argument('--age_min', default='9', help='Minimal age of the subjects used to construct the template.')
parser.add_argument('--age_max', default='12', help='Maximal age of the subjects used to construct the template.')
args = parser.parse_args()

with open(args.subj_ls) as file:
    subjects = file.readlines()
    subjects = [line.rstrip() for line in subjects]

threshold_ls = np.arange(0, 1, 0.1)
for s in subjects:
    # 1. threshold FAST segmented tissues [0-CSF 1-GM 2-WM]
    fast_seg0 = nib.load(os.path.join(args.seg_dir, s, 'reconall_brain_fast_pve_0.nii.gz'))
    fast_seg1 = nib.load(os.path.join(args.seg_dir, s, 'reconall_brain_fast_pve_1.nii.gz'))
    fast_seg2 = nib.load(os.path.join(args.seg_dir, s, 'reconall_brain_fast_pve_2.nii.gz'))
    gt0 = fast_seg0.get_fdata()
    gt1 = fast_seg1.get_fdata()
    gt2 = fast_seg2.get_fdata()

    if not os.path.exists(os.path.join(args.seg_dir, s, 'thresholded')):
        os.mkdir(os.path.join(args.seg_dir, s, 'thresholded'))

    for t in threshold_ls:
        gt0_bool = gt0 > t
        gt0_bool.astype(int)
        img = nib.Nifti1Image(gt0_bool, fast_seg0.affine, fast_seg0.header)
        nib.save(img, os.path.join(args.seg_dir, s, 'thresholded', 'reconall_brain_fast_pve_0_th' 
            + np.array2string(t, precision=2) + '.nii'))

        gt1_bool = gt1 > t
        gt1_bool.astype(int)
        img = nib.Nifti1Image(gt1_bool, fast_seg1.affine, fast_seg1.header)
        nib.save(img, os.path.join(args.seg_dir, s, 'thresholded', 'reconall_brain_fast_pve_1_th' 
            + np.array2string(t, precision=2) + '.nii'))

        gt2_bool = gt2 > t
        gt2_bool.astype(int)
        img = nib.Nifti1Image(gt2_bool, fast_seg2.affine, fast_seg2.header)
        nib.save(img, os.path.join(args.seg_dir, s, 'thresholded', 'reconall_brain_fast_pve_2_th' 
            + np.array2string(t, precision=2) + '.nii'))
    
    # 2. threshold each template's TPMs which were registered to individual native space
    for race in ['AA', 'EA']:
        fnirt_reg1 = nib.load(os.path.join(args.reg_dir, 'Template_' + args.age_min + args.age_max + race, 
            s, 'age' + args.age_min + '-' + args.age_max + '_' + race + '_TMP1_to_reconall_brain.nii.gz'))
        fnirt_reg2 = nib.load(os.path.join(args.reg_dir, 'Template_' + args.age_min + args.age_max + race, 
            s, 'age' + args.age_min + '-' + args.age_max + '_' + race + '_TMP2_to_reconall_brain.nii.gz'))
        fnirt_reg3 = nib.load(os.path.join(args.reg_dir, 'Template_' + args.age_min + args.age_max + race, 
            s, 'age' + args.age_min + '-' + args.age_max + '_' + race + '_TMP3_to_reconall_brain.nii.gz'))
        reg1 = fnirt_reg1.get_fdata()
        reg2 = fnirt_reg2.get_fdata()
        reg3 = fnirt_reg3.get_fdata()

        curr_reg_dir = os.path.join(args.reg_dir, 'Template_' + args.age_min + args.age_max + race, s, 'thresholded')
        if not os.path.exists(curr_reg_dir):
            os.mkdir(curr_reg_dir)
        
        for t in threshold_ls:
            gt1_bin = nib.load(os.path.join(args.seg_dir, s, 'thresholded', 'reconall_brain_fast_pve_1_th' 
                + np.array2string(t, precision=2) + '.nii')).get_fdata()
            reg1_bool = np.multiply(2, reg1 > t)
            #reg1_bool.astype(int)
            reg1_bool = reg1_bool + gt1_bin
            img = nib.Nifti1Image(reg1_bool, fnirt_reg1.affine, fnirt_reg1.header)
            nib.save(img, os.path.join(curr_reg_dir, 'age' + args.age_min + '-' + args.age_max + '_' + race + 
                '_TMP1_to_reconall_brain_th' + np.array2string(t, precision=2) + '_overlap_gt.nii'))

            gt2_bin = nib.load(os.path.join(args.seg_dir, s, 'thresholded', 'reconall_brain_fast_pve_2_th' 
                + np.array2string(t, precision=2) + '.nii')).get_fdata()
            reg2_bool = np.multiply(2, reg2 > t)
            reg2_bool = reg2_bool + gt2_bin
            #reg2_bool.astype(int)
            img = nib.Nifti1Image(reg2_bool, fnirt_reg2.affine, fnirt_reg2.header)
            nib.save(img, os.path.join(curr_reg_dir, 'age' + args.age_min + '-' + args.age_max + '_' + race + 
                '_TMP2_to_reconall_brain_th' + np.array2string(t, precision=2) + '_overlap_gt.nii'))

            gt0_bin = nib.load(os.path.join(args.seg_dir, s, 'thresholded', 'reconall_brain_fast_pve_0_th' 
                + np.array2string(t, precision=2) + '.nii')).get_fdata()
            reg3_bool = np.multiply(2, reg3 > t)
            reg3_bool = reg3_bool + gt0_bin
            #reg3_bool.astype(int)
            img = nib.Nifti1Image(reg3_bool, fnirt_reg3.affine, fnirt_reg3.header)
            nib.save(img, os.path.join(curr_reg_dir, 'age' + args.age_min + '-' + args.age_max + '_' + race + 
                '_TMP3_to_reconall_brain_th' + np.array2string(t, precision=2) + '_overlap_gt.nii'))

