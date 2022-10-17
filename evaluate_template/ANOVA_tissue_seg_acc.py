import argparse, os
import pandas as pd 
import numpy as np 
import statsmodels.api as sm 
from statsmodels.formula.api import ols
from statsmodels.stats.multitest import multipletests

parser = argparse.ArgumentParser(description = 
    'Two-way ANOVA to test the effects of test group and template on tissue segmentation accuracy')
parser.add_argument('--csv_tplAA', help= 
    'The csv file of tissue segmentation accuracies (GM) for the AA template. \
    The algorithm will replace GM with WM or CSF automatically.')
parser.add_argument('--csv_tplEA', help=
    'The csv file of tissue segmentation accuracies (GM) for the EA template. \
    The algorithm will replace GM with WM or CSF automatically.')
parser.add_argument('--subj_AA', help='A txt file containing the test AA subject IDs.')
parser.add_argument('--subj_WA', help='A txt file containing the test WA subject IDs.')
args = parser.parse_args()

def per_tissue(csv_tplAA, csv_tplEA, AA, WA):
    df_tplAA = pd.read_csv(csv_tplAA)
    df_tplEA = pd.read_csv(csv_tplEA)
    # collect thresholds
    headers = df_tplAA.columns
    headers = headers[1:]
    i = 0  # skip the first header SUBID
    thresholds = []
    while i < len(headers):
        h = headers[i].split()
        h = h[-1]
        thresholds.append(float(h))
        i+=1
    thresholds = np.array(thresholds)

    df_tplAA_testAA = df_tplAA.loc[df_tplAA['SUBID'].map(lambda x: True if x in AA else False),:]
    df_tplAA_testWA = df_tplAA.loc[df_tplAA['SUBID'].map(lambda x: True if x in WA else False),:]
    df_tplEA_testAA = df_tplEA.loc[df_tplEA['SUBID'].map(lambda x: True if x in AA else False),:]
    df_tplEA_testWA = df_tplEA.loc[df_tplEA['SUBID'].map(lambda x: True if x in WA else False),:]

    p = []
    for h in headers:
        acc_tplAA_testAA = np.array(df_tplAA_testAA[h])
        acc_tplAA_testWA = np.array(df_tplAA_testWA[h])
        acc_tplEA_testAA = np.array(df_tplEA_testAA[h])
        acc_tplEA_testWA = np.array(df_tplEA_testWA[h])
        acc = np.concatenate((acc_tplAA_testAA, acc_tplAA_testWA, acc_tplEA_testAA, acc_tplEA_testWA), axis=0)
        tpl = np.concatenate((np.repeat(['AA'], len(acc_tplAA_testAA) + len(acc_tplAA_testWA)), 
            np.repeat(['EA'], len(acc_tplEA_testAA) + len(acc_tplEA_testWA))), axis=0)
        test_grp = np.repeat(np.concatenate((np.repeat(['AA'], len(acc_tplAA_testAA)), 
            np.repeat(['WA'], len(acc_tplAA_testWA))), axis=0), 2)
        df = pd.DataFrame({'acc': acc, 'template': tpl, 'test_grp': test_grp})
        model = ols('acc ~ C(template) + C(test_grp) + C(template):C(test_grp)', data=df).fit()
        result = sm.stats.anova_lm(model, type=2)
        p.append(result.loc['C(template):C(test_grp)', 'PR(>F)'])
    
    return p

#############
with open(args.subj_AA) as file:
    AA = file.readlines()
    AA = [line.rstrip() for line in AA]
with open(args.subj_WA) as file:
    WA = file.readlines()
    WA = [line.rstrip() for line in WA]

# replace '_GM' with '_WM' or '_CSF'
csv_dir = os.path.dirname(args.csv_tplAA)
GM_AAbase = os.path.basename(args.csv_tplAA)
GM_EAbase = os.path.basename(args.csv_tplEA)
WM_AAbase = GM_AAbase.replace('_GM', '_WM')
WM_EAbase = GM_EAbase.replace('_GM', '_WM')
CSF_AAbase = GM_AAbase.replace('_GM', '_CSF')
CSF_EAbase = GM_EAbase.replace('_GM', '_CSF')

# run ANOVA for each tissue type
# for each tissue type, the output is a list of p values according to different thresholds
p_GM = per_tissue(args.csv_tplAA, args.csv_tplEA, AA, WA)
p_WM = per_tissue(os.path.join(csv_dir, WM_AAbase), os.path.join(csv_dir, WM_EAbase), AA, WA)
p_CSF = per_tissue(os.path.join(csv_dir, CSF_AAbase), os.path.join(csv_dir, CSF_EAbase), AA, WA)
p_all = p_GM + p_WM + p_CSF

mt = multipletests(p_all, method='fdr_by')
reject = mt[0]
p_corrected = mt[1]
print('Rejct? :')
print(reject)
print('P values after correction :')
print(p_corrected)