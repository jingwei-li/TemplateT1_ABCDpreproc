import numpy as np 
import nibabel as nib 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('path1')
parser.add_argument('path2')
parser.add_argument('out')
args = parser.parse_args()

img1 = nib.load(args.path1)
img2 = nib.load(args.path2)
data1 = img1.get_fdata()
data2 = img2.get_fdata()

idx = np.where(np.logical_and(data1==data2, data2!=0))
data = np.full_like(data1, 0)
data[idx] = 1
img = nib.Nifti1Image(data, img1.affine, img1.header)
nib.save(img, args.out)
