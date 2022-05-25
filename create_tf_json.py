import os
import json
import argparse
import nibabel as nib
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('ethnicity')
parser.add_argument("age_min")
parser.add_argument('age_max')
parser.add_argument('tpl_dir')
args = parser.parse_args()
eth = args.ethnicity
age_min = args.age_min
age_max = args.age_max
tpl_dir = args.tpl_dir

# read template header information to be written to the json file
res1_fn = os.path.realpath(os.path.join(tpl_dir, 
    'tpl-PNC' + eth + age_min + age_max + '_res-01_T1w.nii.gz'))
res2_fn = os.path.realpath(os.path.join(tpl_dir, 
    'tpl-PNC' + eth + age_min + age_max + '_res-02_T1w.nii.gz'))

img1 = nib.load(res1_fn)
img2 = nib.load(res2_fn)

origin1 = np.stack((img1.header['qoffset_x'], img1.header['qoffset_y'], img1.header['qoffset_z'])).tolist()
origin2 = np.stack((img2.header['qoffset_x'], img2.header['qoffset_y'], img2.header['qoffset_z'])).tolist()
shape1 = list(img1.shape)
shape2 = list(img2.shape)
zoom1 = img1.header['pixdim'][1:4].tolist()
zoom2 = img2.header['pixdim'][1:4].tolist()

# create json dictionary
aList = {"Authors": "Jingwei Li, Felix Hoffstaedter, Kaustubh Patil, Sarah Genon", 
    "Acknowledgements": "", "BIDSVersion": "1.1.0", "HowToAcknowledge": "", 
    "Identifier": "test", "License": "See LICENSE file",    
    "Name": "tpl-PNC" + eth + age_min + age_max,
    "RRID": "None",
    "ReferencesAndLinks": ["None"],
    "TemplateFlowVersion": "1.0.0",
    "res": {"01": {"origin": origin1, "shape": shape1, "zooms": zoom1}, 
    "02": {"origin": origin2, "shape": shape2, "zooms": zoom2}}}

jsonString = json.dumps(aList, indent = 4)
jsonFile = open(os.path.join(tpl_dir, "template_description.json"), "w")
jsonFile.write(jsonString)
jsonFile.close()