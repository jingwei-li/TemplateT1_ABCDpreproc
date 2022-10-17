import argparse, os
import nibabel as nib 
import numpy as np 
import pandas as pd 

def dice_coef(gt, reg, reg_threshold):
    gt = gt.flatten()
    reg = reg.flatten()
    #gt_bool = gt>reg_threshold
    gt_bool = gt>0
    reg_bool = reg > reg_threshold
    union = np.sum(gt_bool) + np.sum(reg_bool)
    if union == 0: return 1
    intersection = np.sum( gt_bool * reg_bool )
    return 2 * intersection / union

parser = argparse.ArgumentParser()
parser.add_argument('--subj_ls', help='List of subject in either AA or EA groups who passed fmriprep.')
parser.add_argument('--seg_dir', help='The directory which contains individual brains\' segmentation in native space.')
parser.add_argument('--reg_dir', help='The directory which contains the template\'s TPMs registered to individual\'s native space.')
parser.add_argument('--age_min', help='Minimal age of the subjects used to construct the template.')
parser.add_argument('--age_max', help='Maximal age of the subjects used to construct the template.')
parser.add_argument('--race', help='Ethnicity/race of the subjects used to construct the template: AA or EA.')
parser.add_argument('--out_dir', help='Output directory for generated CSV files (full-path) which will contain the tissue segmentation accuracies.')
args = parser.parse_args()

with open(args.subj_ls) as file:
    subjects = file.readlines()
    subjects = [line.rstrip() for line in subjects]


threshold_ls = np.arange(0, 1, 0.1)
headers = ['SUBID']
for threshold in threshold_ls:
    headers.append('Cut-off = ' + np.array2string(threshold, precision=2))

ses = 'ses-baselineYear1Arm1'
data_wm = []
data_gm = []
data_csf = []
for s in subjects:
    # FAST segmented tissues of each subject in native space [0-CSF 1-GM 2-WM]
    # performed by `tissue_segment_fast.sh`
    fast_seg0 = nib.load(os.path.join(args.seg_dir, s, 'reconall_brain_fast_pve_0.nii.gz'))
    fast_seg1 = nib.load(os.path.join(args.seg_dir, s, 'reconall_brain_fast_pve_1.nii.gz'))
    fast_seg2 = nib.load(os.path.join(args.seg_dir, s, 'reconall_brain_fast_pve_2.nii.gz'))
    gt0 = fast_seg0.get_fdata()
    gt1 = fast_seg1.get_fdata()
    gt2 = fast_seg2.get_fdata()

    # transform template TPMs to individual native space [1-GM, 2-WM, 3-CSF]
    # performed by `fnirt_TemplateTPMs2native.sh`
    fnirt_reg1 = nib.load(os.path.join(args.reg_dir, 'Template_' + args.age_min + args.age_max + args.race, 
        s, 'age' + args.age_min + '-' + args.age_max + '_' + args.race + '_TMP1_to_reconall_brain.nii.gz'))
    fnirt_reg2 = nib.load(os.path.join(args.reg_dir, 'Template_' + args.age_min + args.age_max + args.race, 
        s, 'age' + args.age_min + '-' + args.age_max + '_' + args.race + '_TMP2_to_reconall_brain.nii.gz'))
    fnirt_reg3 = nib.load(os.path.join(args.reg_dir, 'Template_' + args.age_min + args.age_max + args.race, 
        s, 'age' + args.age_min + '-' + args.age_max + '_' + args.race + '_TMP3_to_reconall_brain.nii.gz'))
    reg1 = fnirt_reg1.get_fdata()
    reg2 = fnirt_reg2.get_fdata()
    reg3 = fnirt_reg3.get_fdata()

    # threshold TPMs and calculate Dice overlap with FAST segmentations
    Dice_WM = [s]
    Dice_GM = [s]
    Dice_CSF = [s]
    for threshold in threshold_ls:
        Dice_WM.append(dice_coef(gt2, reg2, threshold))
        Dice_GM.append(dice_coef(gt1, reg1, threshold))
        Dice_CSF.append(dice_coef(gt0, reg3, threshold))
    data_wm.append(Dice_WM)
    data_gm.append(Dice_GM)
    data_csf.append(Dice_CSF)

if not os.path.isdir(args.out_dir):
    os.mkdir(args.out_dir)
wm_csv = os.path.join(args.out_dir, 'Template_'  + args.age_min + args.age_max + args.race + '_WM.csv')
df_wm = pd.DataFrame(data_wm)
df_wm.to_csv(wm_csv, header=headers, index=False)
gm_csv = os.path.join(args.out_dir, 'Template_'  + args.age_min + args.age_max + args.race + '_GM.csv')
df_gm = pd.DataFrame(data_gm)
df_gm.to_csv(gm_csv, header=headers, index=False)
csf_csv = os.path.join(args.out_dir, 'Template_'  + args.age_min + args.age_max + args.race + '_CSF.csv')
df_csf = pd.DataFrame(data_csf)
df_csf.to_csv(csf_csv, header=headers, index=False)