#!/bin/bash

proj_dir="/data/project/template_t1"
PNCtpl_dir="$proj_dir/data/PNC_LauraW/Templates"
TPL_DIR="$proj_dir/child/data/T1/TemplateFlow"
age_min="9"
age_max="12"

for eth in AA EA; do
    mkdir -p $TPL_DIR/tpl-PNC${eth}${age_min}${age_max}

    # 1mm as resolution 1
    gzip -c $PNCtpl_dir/Template_${age_min}${age_max}${eth}/age${age_min}-${age_max}_${eth}_1mm.nii > \
        $TPL_DIR/tpl-PNC${eth}${age_min}${age_max}/tpl-PNC${eth}${age_min}${age_max}_res-01_T1w.nii.gz
    gzip -c $PNCtpl_dir/Template_${age_min}${age_max}${eth}/age${age_min}-${age_max}_${eth}_brainmask.nii > \
        $TPL_DIR/tpl-PNC${eth}${age_min}${age_max}/tpl-PNC${eth}${age_min}${age_max}_res-01_desc-brain_mask.nii.gz

    # 1.5mm as resolution 2
    gzip -c $PNCtpl_dir/Template_${age_min}${age_max}${eth}/age${age_min}-${age_max}_${eth}.nii > \
        $TPL_DIR/tpl-PNC${eth}${age_min}${age_max}/tpl-PNC${eth}${age_min}${age_max}_res-02_T1w.nii.gz
    gzip -c $PNCtpl_dir/Template_${age_min}${age_max}${eth}/age${age_min}-${age_max}_${eth}_brainmask.nii > \
        $TPL_DIR/tpl-PNC${eth}${age_min}${age_max}/tpl-PNC${eth}${age_min}${age_max}_res-02_desc-brain_mask.nii.gz

    # create json file
    python3 create_tf_json.py $eth $age_min $age_max $TPL_DIR/tpl-PNC${eth}${age_min}${age_max} 
done