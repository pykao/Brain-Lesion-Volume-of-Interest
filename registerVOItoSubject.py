import os
import subprocess
import SimpleITK as sitk
import numpy as np

import paths
import shutil

from natsort import natsorted


def ReadImage(file_path):
    ''' This code returns the numpy nd array for a MR image at path'''
    return sitk.GetArrayFromImage(sitk.ReadImage(file_path)).astype(np.float32)

def FindOneElement(s, ch):
	''' This function gives the indexs of one element ch on the string s'''
	return [i for i, ltr in enumerate(s) if ltr == ch]

def SubjectID(bratsPath):
	''' This function gives you the subject ID'''
	return bratsPath[FindOneElement(bratsPath,'/')[-2]+1:FindOneElement(bratsPath,'/')[-1]]

def RegisterLabels2Subject(refVol_path, bp_filepaths, mni2subject_mat, temp_dir):
    ''' register indivudial labels from MNI 152 space to subject space '''
    print("Registering individual labels from MNI 152 space to subject space...")
    for j in range(len(bp_filepaths)):
        label_name = os.path.join(temp_dir, "lab"+str(j+1)+".nii.gz")
        # Register Brain Labels to Subject Space
        subprocess.call(["flirt", "-in", bp_filepaths[j], "-ref", refVol_path, "-out", label_name, "-init", mni2subject_mat, "-applyxfm"])


def SubjectLabels2ParcellationArgmax(subject_bp_filepaths, subject_name):
    print('Mapping brain parcellation to subject...')
    subjectBrainParcellations = np.zeros((len(subject_bp_filepaths)+1, 155, 240, 240), dtype=np.float32)
    img = sitk.ReadImage(subject_bp_filepaths[0])
    for j, bp in enumerate(subject_bp_filepaths):
        subjectBrainParcellations[j+1,:] = ReadImage(bp)
    brainParcellation = np.argmax(subjectBrainParcellations, axis=0)
    brainParcellationFloat = brainParcellation.astype(np.float32)
    brainParcellationFloat_img = sitk.GetImageFromArray(brainParcellationFloat)
    brainParcellationFloat_img.CopyInformation(img)
    sitk.WriteImage(brainParcellationFloat_img, subject_name)

dest_path = paths.brats2018_training_path

train_dir = './train'
if not os.path.exists(train_dir):
	os.mkdir(train_dir)
if 'train' in train_dir:
	output_dir = train_dir

refvol2invol_paths = [os.path.join(root, name) for root, dirs, files in os.walk(dest_path) for name in files if 'refvol2invol' in name and name.endswith('.mat')]
refvol2invol_paths = natsorted(refvol2invol_paths, key=lambda y: y.lower())

refVol_paths = [os.path.join(root, name) for root, dirs, files in os.walk(dest_path) for name in files if 't1_N4ITK_corrected' in name and name.endswith('.nii.gz')]
refVol_paths = natsorted(refVol_paths, key=lambda y: y.lower())

VOI_path = './VOI'

voi_filepaths = [os.path.join(root, name) for root, dirs, files in os.walk(VOI_path) for name in files if 'lab' in name and name.endswith('.nii.gz')]
voi_filepaths = natsorted(voi_filepaths, key=lambda y: y.lower())


for i in range(len(refVol_paths)):
	subject_ID = SubjectID(refVol_paths[i])
	print('Working on: ', subject_ID)

	temp_dir = os.path.join('./temp')

	if not os.path.exists(temp_dir):
		os.mkdir(temp_dir)
	RegisterLabels2Subject(refVol_paths[i], voi_filepaths, refvol2invol_paths[i], temp_dir)
	subject_bp_filepaths = [os.path.join(root, name) for root, dirs, files in os.walk(temp_dir) for name in files if 'lab' in name and name.endswith('.nii.gz')]
	subject_bp_filepaths = natsorted(subject_bp_filepaths, key=lambda y: y.lower())
	subject_name = os.path.join(output_dir, subject_ID+'_VOI-1mm.nii.gz')
	SubjectLabels2ParcellationArgmax(subject_bp_filepaths, subject_name)
	shutil.rmtree(temp_dir)
