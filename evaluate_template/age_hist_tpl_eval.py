import os, argparse
import pandas as pd
import matplotlib.pyplot as plt

def age_hist(data, title, labels, outname):
    orange = [245/255, 117/255, 5/255, 1]
    sky = [6/255, 155/255, 229/255, 1]

    fig = plt.figure(figsize=(12, 8))
    # transparent background
    ax = plt.gca()
    ax.patch.set_alpha(0)
    # invisible right and upper axes
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    # histogram
    nbins = 20
    plt.hist(data, bins=nbins, label=labels)

    plt.title(title, fontweight ="bold", fontsize=19)
    plt.legend(fontsize=16, frameon=False, loc='best')
    plt.ylabel('# subjects', fontsize=18)
    plt.xlabel('Age in months', fontsize=18)

    # save
    plt.savefig(outname + '.png', format='png', transparent=False)
    plt.savefig(outname + '.eps', format='eps', transparent=True)

parser = argparse.ArgumentParser(description='Age distributions of the subjects used for template construction and evaluation.')
parser.add_argument('--ABCD_AA_ls', help='List of test ABCD subjects who are African Americans.')
parser.add_argument('--ABCD_WA_ls', help='List of test ABCD subjects who are white Americans.')
parser.add_argument('--outdir', help='Output directory (full path).')
args = parser.parse_args()

if not os.path.isdir(args.outdir):
    os.mkdir(args.outdir)

# read the age of subjects used for creating brain templates
proj_dir = '/data/project/template_t1'
df_pnc_AA = pd.read_csv(os.path.join(proj_dir, 'data', 'PNC_LauraW', 'code', 'age9-12_AA.csv'))
df_pnc_EA = pd.read_csv(os.path.join(proj_dir, 'data', 'PNC_LauraW', 'code', 'age9-12_EA.csv'))
pnc_AA_age = df_pnc_AA.ageAtScan.values
pnc_EA_age = df_pnc_EA.ageAtScan.values

# read the subject IDs which are used for template evaluation
with open(args.ABCD_AA_ls) as file:
    ABCD_AA = file.readlines()
    ABCD_AA = [line.rstrip() for line in ABCD_AA]
with open(args.ABCD_WA_ls) as file:
    ABCD_WA = file.readlines()
    ABCD_WA = [line.rstrip() for line in ABCD_WA]

# ABCD csv
abcd_csv_dir = os.path.join(proj_dir, 'data', 'ABCD_datalad', 'inm7-superds', 'original', 'abcd', 'phenotype', 'phenotype')
pwd = os.getcwd()
os.chdir(abcd_csv_dir)
os.system('datalad get abcd_lt01.txt')
df_abcd = pd.read_csv(os.path.join(abcd_csv_dir, 'abcd_lt01.txt'), delimiter='\t', low_memory=False)
os.system('datalad drop abcd_lt01.txt')
os.chdir(pwd)

# age of subjects used for evaluating brain templates
df_abcd = df_abcd[df_abcd.eventname == 'baseline_year_1_arm_1']
all_sub = df_abcd.subjectkey.values.tolist()
AA_row = []
WA_row = []
for s in all_sub:
    s = s.replace('NDAR_', 'sub-NDAR')
    print(s)
    AA_row.append(s in ABCD_AA)
    WA_row.append(s in ABCD_WA)

df_abcd_AA = df_abcd.iloc[AA_row, :]
df_abcd_WA = df_abcd.iloc[WA_row, :]
abcd_AA_age = df_abcd_AA.interview_age.values
abcd_AA_age = [eval(i) for i in abcd_AA_age]
abcd_WA_age = df_abcd_WA.interview_age.values
abcd_WA_age = [eval(i) for i in abcd_WA_age]
print(abcd_AA_age)
print(abcd_WA_age)

# plot
age_hist([pnc_AA_age, pnc_EA_age], 'Age distribution of PNC subjects\nused to construct templates', ['PNC AA', 'PNC EA'], os.path.join(args.outdir, 'pnc'))
age_hist([abcd_AA_age, abcd_WA_age], 'Age distribution of ABCD subjects\nused to evaluate templates', ['ABCD AA', 'ABCD EA'], os.path.join(args.outdir, 'abcd'))