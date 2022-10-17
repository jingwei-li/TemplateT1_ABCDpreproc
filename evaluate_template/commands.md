
## plot tissue segmentation accuracy

```
# CSF
python3 ./plot_tissue_seg_acc.py --subj_ls /data/project/template_t1/data/ABCD_datalad/code/TemplateT1_ABCDpreproc/lists/subj_ls_all_rand50AA_subset40.txt --csv_tpl1 /data/project/template_t1/data/ABCD_datalad/tissue_seg/dice/Template_912AA_CSF_FASThard.csv --csv_tpl2 /data/project/template_t1/data/ABCD_datalad/tissue_seg/dice/Template_912EA_CSF_FASThard.csv --label1 Template_912AA --label2 Template_912EA --out_png /data/project/template_t1/data/ABCD_datalad/tissue_seg/figures/reconall_AA/FASThard/CSF_subj_rand50AA_subset40_Templates_912AAvsEA

python3 ./plot_tissue_seg_acc.py --subj_ls /data/project/template_t1/data/ABCD_datalad/code/TemplateT1_ABCDpreproc/lists/subj_ls_all_rand50EA_subset40.txt --csv_tpl1 /data/project/template_t1/data/ABCD_datalad/tissue_seg/dice/Template_912AA_CSF_FASThard.csv --csv_tpl2 /data/project/template_t1/data/ABCD_datalad/tissue_seg/dice/Template_912EA_CSF_FASThard.csv --label1 Template_912AA --label2 Template_912EA --out_png /data/project/template_t1/data/ABCD_datalad/tissue_seg/figures/reconall_AA/FASThard/CSF_subj_rand50EA_subset40_Templates_912AAvsEA

# GM
python3 ./plot_tissue_seg_acc.py --subj_ls /data/project/template_t1/data/ABCD_datalad/code/TemplateT1_ABCDpreproc/lists/subj_ls_all_rand50AA_subset40.txt --csv_tpl1 /data/project/template_t1/data/ABCD_datalad/tissue_seg/dice/Template_912AA_GM_FASThard.csv --csv_tpl2 /data/project/template_t1/data/ABCD_datalad/tissue_seg/dice/Template_912EA_GM_FASThard.csv --label1 Template_912AA --label2 Template_912EA --out_png /data/project/template_t1/data/ABCD_datalad/tissue_seg/figures/reconall_AA/FASThard/GM_subj_rand50AA_subset40_Templates_912AAvsEA

python3 ./plot_tissue_seg_acc.py --subj_ls /data/project/template_t1/data/ABCD_datalad/code/TemplateT1_ABCDpreproc/lists/subj_ls_all_rand50EA_subset40.txt --csv_tpl1 /data/project/template_t1/data/ABCD_datalad/tissue_seg/dice/Template_912AA_GM_FASThard.csv --csv_tpl2 /data/project/template_t1/data/ABCD_datalad/tissue_seg/dice/Template_912EA_GM_FASThard.csv --label1 Template_912AA --label2 Template_912EA --out_png /data/project/template_t1/data/ABCD_datalad/tissue_seg/figures/reconall_AA/FASThard/GM_subj_rand50EA_subset40_Templates_912AAvsEA

# WM
python3 ./plot_tissue_seg_acc.py --subj_ls /data/project/template_t1/data/ABCD_datalad/code/TemplateT1_ABCDpreproc/lists/subj_ls_all_rand50AA_subset40.txt --csv_tpl1 /data/project/template_t1/data/ABCD_datalad/tissue_seg/dice/Template_912AA_WM_FASThard.csv --csv_tpl2 /data/project/template_t1/data/ABCD_datalad/tissue_seg/dice/Template_912EA_WM_FASThard.csv --label1 Template_912AA --label2 Template_912EA --out_png /data/project/template_t1/data/ABCD_datalad/tissue_seg/figures/reconall_AA/FASThard/WM_subj_rand50AA_subset40_Templates_912AAvsEA

python3 ./plot_tissue_seg_acc.py --subj_ls /data/project/template_t1/data/ABCD_datalad/code/TemplateT1_ABCDpreproc/lists/subj_ls_all_rand50EA_subset40.txt --csv_tpl1 /data/project/template_t1/data/ABCD_datalad/tissue_seg/dice/Template_912AA_WM_FASThard.csv --csv_tpl2 /data/project/template_t1/data/ABCD_datalad/tissue_seg/dice/Template_912EA_WM_FASThard.csv --label1 Template_912AA --label2 Template_912EA --out_png /data/project/template_t1/data/ABCD_datalad/tissue_seg/figures/reconall_AA/FASThard/WM_subj_rand50EA_subset40_Templates_912AAvsEA
```

## plot age distributions

```
python3 age_hist_tpl_eval.py --ABCD_AA_ls /data/project/template_t1/data/ABCD_datalad/code/TemplateT1_ABCDpreproc/lists/subj_ls_all_rand50AA_subset40.txt --ABCD_WA_ls /data/project/template_t1/data/ABCD_datalad/code/TemplateT1_ABCDpreproc/lists/subj_ls_all_rand50EA_subset40.txt --outdir /data/project/template_t1/data/ABCD_datalad/tissue_seg/figures/age_hist
```

## Two-way ANOVA to test tissue segmentation accuracy differences

```
python3 ANOVA_tissue_seg_acc.py --csv_tplAA /data/project/template_t1/data/ABCD_datalad/tissue_seg/dice/Template_912AA_GM_FASThard.csv --csv_tplEA /data/project/template_t1/data/ABCD_datalad/tissue_seg/dice/Template_912EA_GM_FASThard.csv --subj_AA /data/project/template_t1/data/ABCD_datalad/code/TemplateT1_ABCDpreproc/lists/subj_ls_all_rand50AA_subset40.txt --subj_WA /data/project/template_t1/data/ABCD_datalad/code/TemplateT1_ABCDpreproc/lists/subj_ls_all_rand50EA_subset40.txt
```