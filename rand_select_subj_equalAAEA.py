import os, argparse, random
import pandas as pd

# input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--csv', help='The CSV file containing race/ethnicity information. (absolute path)', 
    default='/data/project/template_t1/data/ABCD_datalad/inm7-superds/original/abcd/phenotype/phenotype/acspsw03.txt')
parser.add_argument('--subj_ls', help='Full subject list (absolute path).')
parser.add_argument('-N', type=int, help='Number of subjects to be selected per group.', default=50)
parser.add_argument('--outdir', help='Output directory')
args = parser.parse_args()

# read subject list
with open(args.subj_ls) as file:
    subjects = file.readlines()
    subjects = [line.rstrip() for line in subjects]
    subjects = ['NDAR_' + line[8:] for line in subjects ]

# read csv file, grab subset of the dataframe that is necessary
df = pd.read_csv(args.csv, delimiter='\t')
df = df[df.subjectkey.isin(subjects) & df.eventname.isin(['baseline_year_1_arm_1'])]
df = df[['subjectkey', 'race_ethnicity']]

# race_ethnicity: 1=White, 2=Black, 3=Hispanic, 4=Asian, 5=Other
EA = df[df.race_ethnicity == 1].subjectkey.tolist()
AA = df[df.race_ethnicity == 2].subjectkey.tolist()
random.seed(10)
EA = random.sample(EA, args.N)
AA = random.sample(AA, args.N)

EAnew = []
AAnew = []
for item in EA:
    item = 'sub-' + item[0:4] + item[5:]
    EAnew.append(item)
for item in AA:
    item = 'sub-' + item[0:4] + item[5:]
    AAnew.append(item)
all_new = EAnew + AAnew

# write subject IDs into two separate text files
if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)
basename = os.path.splitext(args.subj_ls)[0]
EA_ls = os.path.join(args.outdir, basename + '_rand' + str(args.N) + 'EA.txt')
AA_ls = os.path.join(args.outdir, basename + '_rand' + str(args.N) + 'AA.txt')
full_ls = os.path.join(args.outdir, basename + '_rand' + str(args.N) + 'EA' + str(args.N) + 'AA.txt')
with open(EA_ls, 'w') as f:
    for item in EAnew:
        f.write("%s\n" % item)
with open(AA_ls, 'w') as f:
    for item in AAnew:
        f.write("%s\n" % item)

with open(full_ls, 'w') as f:
    for item in all_new:
        f.write("%s\n" % item)
