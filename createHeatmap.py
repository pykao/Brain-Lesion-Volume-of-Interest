import paths
import os
import SimpleITK as sitk
import numpy as np


heatmaps_dir = os.path.join('.', 'heatmaps')

if not os.path.exists(heatmaps_dir):
	os.mkdir(heatmaps_dir)

seg_name = 'seg_MNI152_1mm'

seg_filepaths = [os.path.join(root, name) for root, dirs, files in os.walk(paths.brats2018_training_path) \
for name in files if seg_name in name and name.endswith('.nii.gz')]
seg_filepaths.sort()

assert(len(seg_filepaths)==285)

heatmap_edema = np.zeros((182,218,182), dtype=np.int16)
heatmap_necrosis = np.zeros((182,218,182), dtype=np.int16)
heatmap_tumor = np.zeros((182,218,182), dtype=np.int16)


for seg_file in seg_filepaths:

	seg_img = sitk.ReadImage(seg_file)
	seg_nda = sitk.GetArrayFromImage(seg_img)

	edema = np.zeros((182,218,182), dtype=np.int16)
	edema[seg_nda==2] = 1
	heatmap_edema += edema

	necrosis = np.zeros((182,218,182), dtype=np.int16)
	necrosis[seg_nda==1] = 1
	heatmap_necrosis += necrosis
	
	tumor = np.zeros((182,218,182), dtype=np.int16)
	tumor[seg_nda==4] = 1
	heatmap_tumor += tumor

heatmap_edema_img = sitk.GetImageFromArray(heatmap_edema)
heatmap_edema_img.CopyInformation(seg_img)
sitk.WriteImage(heatmap_edema_img, os.path.join(heatmaps_dir,'edema_heatmap.nii.gz'))
heatmap_necrosis_img = sitk.GetImageFromArray(heatmap_necrosis)
heatmap_necrosis_img.CopyInformation(seg_img)
sitk.WriteImage(heatmap_necrosis_img, os.path.join(heatmaps_dir,'necrosis_heatmap.nii.gz'))
heatmap_tumor_img = sitk.GetImageFromArray(heatmap_tumor)
heatmap_tumor_img.CopyInformation(seg_img)
sitk.WriteImage(heatmap_tumor_img, os.path.join(heatmaps_dir,'tumor_heatmap.nii.gz'))
