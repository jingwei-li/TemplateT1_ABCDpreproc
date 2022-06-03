import os
import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('--proc_dir', help='BIDS directory of fmriprep preprocessed data (absolute path).')
parser.add_argument('--subj_ls', help='Subject list (absolute path).')
parser.add_argument('--err_ls', help='List of subjects with error message.')
args = parser.parse_args()

with open(args.subj_ls) as file:
    subjects = file.readlines()
    subjects = [line.rstrip() for line in subjects]

subj_err = []
subj_noerr = []

for s in subjects:
    html = os.path.join(args.proc_dir, s+'.html')
    if not os.path.exists(html):
        subj_err.append(s)  # if output html file doesn't exist, this subject needs to be checked manually
    else:
        with open(html) as f:
            soup = BeautifulSoup(f, 'html.parser')
            if 'No errors to report!' in soup.get_text():
                subj_noerr.append(s)
            else:
                subj_err.append(s)

with open(args.err_ls, 'w') as f:
    for item in subj_err:
        f.write("%s\n" % item)