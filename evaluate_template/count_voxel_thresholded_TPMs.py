import argparse, os
import numpy as np
import nibabel as nib

parser = argparse.ArgumentParser(description='Count the number of voxels in a template\'s tissue maps with different thresholds.')
parser.add_argument('--tpl_dir', help='Directory to the template. This folder should contain files named with _TMP?.nii.')
parser.add_argument('--prefix', help='Prefix of TMPs\' basenames before _TMP?.nii.')
args = parser.parse_args()

threshold_ls = np.arange(0, 1, 0.1)

for i in ['1', '2', '3']:
    TMP = nib.load(os.path.join(args.tpl_dir, args.prefix + '_TMP' + i + '.nii'))
    vol = TMP.get_fdata()

    if i is '1':
        tissue = 'GM'
    elif i is '2':
        tissue = 'WM'
    else:
        tissue = 'CSF'

    print('Number of voxels in ' + tissue + ' mask:')
    for t in threshold_ls:
        vol_bool = vol > t
        count = np.sum(vol_bool.flatten())
        if t==0:
            count0 = count
        print('Threshold = ' + np.array2string(t, precision=2) + ';   count = ' + 
            str(count) + ';   fraction to threshold=0: ' + np.array2string(np.divide(count, count0), precision=3))