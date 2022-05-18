#!/bin/bash

proj_dir="/data/project/template_t1"
PNCtpl_dir="$proj_dir/data/PNC_LauraW/Templates"
TPL_DIR="$proj_dir/child/data/T1/TemplateFlow"
age_min="9"
age_max="12"

for eth in AA EA; do
    mkdir -p $TPL_DIR/tpl-PNC_${eth}_${age_min}_${age_max}
    ln -s $PNCtpl_dir/Template_${age_min}${age_max}${eth}/age${age_min}-${age_max}_${eth}.nii \
        $TPL_DIR/tpl-PNC_${eth}_${age_min}_${age_max}/tpl-PNC_${eth}_${age_min}_${age_max}_res-01_T1w.nii.gz
    ln -s $PNCtpl_dir/Template_${age_min}${age_max}${eth}/age${age_min}-${age_max}_${eth}_brainmask.nii \
        $TPL_DIR/tpl-PNC_${eth}_${age_min}_${age_max}/tpl-PNC_${eth}_${age_min}_${age_max}_res-01_desc-brain_mask.nii.gz

    flirt -in $TPL_DIR/tpl-PNC_${eth}_${age_min}_${age_max}/tpl-PNC_${eth}_${age_min}_${age_max}_res-01_T1w.nii.gz \
        -ref $TPL_DIR/tpl-PNC_${eth}_${age_min}_${age_max}/tpl-PNC_${eth}_${age_min}_${age_max}_res-01_T1w.nii.gz \
        -applyisoxfm 1 -nosearch \
        -out $TPL_DIR/tpl-PNC_${eth}_${age_min}_${age_max}/tpl-PNC_${eth}_${age_min}_${age_max}_res-02_T1w.nii.gz

    flirt -in $TPL_DIR/tpl-PNC_${eth}_${age_min}_${age_max}/tpl-PNC_${eth}_${age_min}_${age_max}_res-01_desc-brain_mask.nii.gz \
        -ref $TPL_DIR/tpl-PNC_${eth}_${age_min}_${age_max}/tpl-PNC_${eth}_${age_min}_${age_max}_res-01_desc-brain_mask.nii.gz \
        -applyisoxfm 1 -nosearch \
        -out $TPL_DIR/tpl-PNC_${eth}_${age_min}_${age_max}/tpl-PNC_${eth}_${age_min}_${age_max}_res-02_desc-brain_mask.nii.gz
    
    mri_binarize --i $TPL_DIR/tpl-PNC_${eth}_${age_min}_${age_max}/tpl-PNC_${eth}_${age_min}_${age_max}_res-02_desc-brain_mask.nii.gz \
        --o $TPL_DIR/tpl-PNC_${eth}_${age_min}_${age_max}/tpl-PNC_${eth}_${age_min}_${age_max}_res-02_desc-brain_mask.nii.gz --min 0.4999
done