import numpy as np
import SimpleITK as sitk
import os

def find_percentiles(x):
	x_flat = np.reshape(x, (-1, 1))
	x_float = x_flat.astype(np.float64)
	y = np.ma.masked_where(x_float == 0, x_float)
	y = np.ma.filled(y, np.nan)
	return np.nanpercentile(y, 25), np.nanpercentile(y, 50), np.nanpercentile(y, 75)

heatmaps_dir = './heatmaps/'

edema_heatmap_dir = os.path.join(heatmaps_dir, 'edema_heatmap.nii.gz')
necrosis_heatmap_dir = os.path.join(heatmaps_dir, 'necrosis_heatmap.nii.gz')
tumor_heatmap_dir = os.path.join(heatmaps_dir, 'tumor_heatmap.nii.gz')

edema_heatmap_img = sitk.ReadImage(edema_heatmap_dir)
edema_nda = sitk.GetArrayFromImage(edema_heatmap_img)

necrosis_heatmap_img = sitk.ReadImage(necrosis_heatmap_dir)
necrosis_nda = sitk.GetArrayFromImage(necrosis_heatmap_img)

tumor_heatmap_img = sitk.ReadImage(tumor_heatmap_dir)
tumor_nda = sitk.GetArrayFromImage(tumor_heatmap_img)

VOI = np.zeros(tumor_nda.shape, tumor_nda.dtype)

ed25, ed50, ed75 = find_percentiles(edema_nda)
ne25, ne50, ne75 = find_percentiles(necrosis_nda)
tu25, tu50, tu75 = find_percentiles(tumor_nda)
print('Edema:', ed25, ed50, ed75)
print('Necrosis:', ne25, ne50, ne75)
print('Tumor:', tu25, tu50, tu75)

VOI[edema_nda>=ed25] = 1
VOI[necrosis_nda>=ne25] = 2
VOI[tumor_nda>=tu25] = 3

VOI[edema_nda>=ed50] = 4
VOI[necrosis_nda>=ne50] = 5
VOI[tumor_nda>=tu50] = 6

VOI[edema_nda>=ed75] = 7
VOI[necrosis_nda>=ne75] = 8
VOI[tumor_nda>=tu75] = 9

VOI_img = sitk.GetImageFromArray(VOI)
VOI_img.CopyInformation(edema_heatmap_img)


VOI_path = './VOI'
if not os.path.exists(VOI_path):
	os.mkdir(VOI_path)

sitk.WriteImage(VOI_img, os.path.join(VOI_path, 'VOI-1mm.nii.gz'))

for i in range(1,10):
	VOI_lab = np.zeros(VOI.shape, VOI.dtype)
	VOI_lab_name = 'VOI-1mm-lab'+str(i)+'.nii.gz'
	VOI_lab[VOI == i] = 1
	VOI_lab_img = sitk.GetImageFromArray(VOI_lab)
	VOI_lab_img.CopyInformation(edema_heatmap_img)
	sitk.WriteImage(VOI_lab_img, os.path.join(VOI_path, VOI_lab_name))


