import argparse, os
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

parser = argparse.ArgumentParser()
parser.add_argument('--subj_ls', help='The test subject list.')
parser.add_argument('--csv_tpl1', help='CSV filename corresponding to the first template (full path).')
parser.add_argument('--csv_tpl2', help='CSV filename corresponding to the second template (full path).')
parser.add_argument('--label1', help='The label used in the plot to represent the first template.')
parser.add_argument('--label2', help='The label used in the plot to represent the second template.')
parser.add_argument('--out_png', help='Name of the output figure (without extension).')
parser.add_argument('--min', default=0, help='Minimal cut-off threshold. Default = 0.')
parser.add_argument('--max', default=1, help='Maximal cut-off threshold. Default = 1.')
args = parser.parse_args()

df1 = pd.read_csv(args.csv_tpl1)
df2 = pd.read_csv(args.csv_tpl2)
if df1.size != df2.size:
    raise ValueError('Two CSV files have different size.')

### get row indices
# read subjects of interest
with open(args.subj_ls) as file:
    subjects = file.readlines()
    subjects = [line.rstrip() for line in subjects]
# compare with SUBID in csv files
all_sub = df1.SUBID.values.tolist()
row = []
for s in all_sub:
    row.append(s in subjects)

### collect thresholds
headers = df1.columns
i = 1  # skip the first header SUBID
thresholds = []
while i < len(headers):
    h = headers[i].split()
    h = h[-1]
    thresholds.append(float(h))
    i+=1
thresholds = np.array(thresholds)
a = thresholds <= args.max
b = thresholds >= args.min
col = a & b  # boolean array of which thresholds are in the required range
col = np.insert(col, 0, False) # prepend False because the first colmn should be SUBID

### extract corresponding Dice coefficients, convert to 1-D numpy array
data1 = df1.iloc[row, col].values
data2 = df2.iloc[row, col].values

### plot
orange = [245/255, 117/255, 5/255, 1]
sky = [6/255, 155/255, 229/255, 1]

fig = plt.figure(figsize=(8, 8))
# transparent background
ax = plt.gca()
ax.patch.set_alpha(0)
# invisible right and upper axes
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

x = thresholds[col[1:]]
l1 = plt.errorbar(x, data1.mean(axis=0), data1.std(axis=0), color=orange, marker='o', label=args.label1)
l2 = plt.errorbar(x, data2.mean(axis=0), data2.std(axis=0), color=sky, marker='o', label=args.label2)
l2[-1][0].set_linestyle('-.')
plt.legend(fontsize=16, frameon=False, loc='best')

plt.ylabel('Dice coefficient', fontsize=18)
plt.xlabel('Probability thresholds', fontsize=18)

### save
outdir = os.path.dirname(args.out_png)
if not os.path.isdir(outdir):
    os.mkdir(outdir)
plt.savefig(args.out_png+'.png', format='png', transparent=False)
plt.savefig(args.out_png+'.eps', format='eps', transparent=True)

#### only plot standard deviation
fig = plt.figure(figsize=(8, 8))
# transparent background
ax = plt.gca()
ax.patch.set_alpha(0)
# invisible right and upper axes
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

x = thresholds[col[1:]]
l1 = plt.plot(x, data1.std(axis=0), color=orange, marker='o', label=args.label1)
l2 = plt.plot(x, data2.std(axis=0), color=sky, marker='o', label=args.label2)
plt.legend(fontsize=16, frameon=False, loc='best')

plt.ylabel('STD of Dice coefficient', fontsize=18)
plt.xlabel('Probability thresholds', fontsize=18)

plt.savefig(args.out_png+'_std.png', format='png', transparent=False)
plt.savefig(args.out_png+'_std.eps', format='eps', transparent=True)