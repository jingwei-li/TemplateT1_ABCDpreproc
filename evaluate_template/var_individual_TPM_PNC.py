import argparse, os
import nibabel as nib
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description = \
    'Calculate variance of co-registered tissue probability maps across each individual in a specific PNC group.')
parser.add_argument('--subj_csv', help='The csv file containing the subjects used to create a template.')
parser.add_argument('--PNC_dir', help='The directory containing the co-registered TPMs of each subject.', \
    default='/data/project/template_t1/data/PNC_LauraW/derivatives/cat12.7_default')
parser.add_argument('--outdir', help='Output directory.')
parser.add_argument('--outprefix', help='Prefix of the basename of output files.')
args = parser.parse_args()

df = pd.read_csv(args.subj_csv)
subjects = df['SUBJID'].values
subjects = ['sub-' + str(s) for s in subjects]

# read tpm of first subject to initialize numpy array with correct size
s = subjects[0]
tpm1 = nib.load(os.path.join(args.PNC_dir, s, 'ses-1', 'mri', 'wrp1' + s + '_ses-1_T1w_affine.nii'))
vol_shape = tpm1.shape
all_tpm1 = np.empty((0, np.prod(vol_shape)))
all_tpm2 = np.empty((0, np.prod(vol_shape)))
all_tpm3 = np.empty((0, np.prod(vol_shape)))

# collect all TPMs
for s in subjects:
    fname = os.path.join(args.PNC_dir, s, 'ses-1', 'mri', 'wrp1' + s + '_ses-1_T1w_affine.nii')
    if os.path.exists(fname):
        print(s)
        tpm1 = nib.load(fname)
        tpm2 = nib.load(os.path.join(args.PNC_dir, s, 'ses-1', 'mri', 'wrp2' + s + '_ses-1_T1w_affine.nii'))
        tpm3 = nib.load(os.path.join(args.PNC_dir, s, 'ses-1', 'mri', 'wrp3' + s + '_ses-1_T1w_affine.nii'))
        all_tpm1 = np.append(all_tpm1, [np.matrix.flatten(tpm1.get_fdata())], axis=0)
        all_tpm2 = np.append(all_tpm2, [np.matrix.flatten(tpm2.get_fdata())], axis=0)
        all_tpm3 = np.append(all_tpm3, [np.matrix.flatten(tpm3.get_fdata())], axis=0)

# compute std and mean, save to files
std_tpm1 = np.std(all_tpm1, axis=0).reshape(vol_shape)
img = nib.Nifti1Image(std_tpm1, tpm1.affine, tpm1.header)
nib.save(img, os.path.join(args.outdir, args.outprefix + '_TPM1_std.nii'))
std_tpm2 = np.std(all_tpm2, axis=0).reshape(vol_shape)
img = nib.Nifti1Image(std_tpm2, tpm2.affine, tpm2.header)
nib.save(img, os.path.join(args.outdir, args.outprefix + '_TPM2_std.nii'))
std_tpm3 = np.std(all_tpm3, axis=0).reshape(vol_shape)
img = nib.Nifti1Image(std_tpm3, tpm3.affine, tpm3.header)
nib.save(img, os.path.join(args.outdir, args.outprefix + '_TPM3_std.nii'))

mean_tpm1 = np.mean(all_tpm1, axis=0).reshape(vol_shape)
img = nib.Nifti1Image(mean_tpm1, tpm1.affine, tpm1.header)
nib.save(img, os.path.join(args.outdir, args.outprefix + '_TPM1_mean.nii'))
mean_tpm2 = np.mean(all_tpm2, axis=0).reshape(vol_shape)
img = nib.Nifti1Image(mean_tpm2, tpm2.affine, tpm2.header)
nib.save(img, os.path.join(args.outdir, args.outprefix + '_TPM2_mean.nii'))
mean_tpm3 = np.mean(all_tpm3, axis=0).reshape(vol_shape)
img = nib.Nifti1Image(mean_tpm3, tpm3.affine, tpm3.header)
nib.save(img, os.path.join(args.outdir, args.outprefix + '_TPM3_mean.nii'))
