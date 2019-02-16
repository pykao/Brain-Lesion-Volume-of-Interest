import numpy as np
import SimpleITK as sitk

edema_heatmap = './heatmaps/edema_heatmap.nii.gz'

necrosis_heatmap = './heatmaps/necrosis_heatmap.nii.gz'

tumor_heatmap = './heatmaps/tumor_heatmap.nii.gz'

edema_heatmap_nda = sitk.GetArrayFromImage(sitk.ReadImage(edema_heatmap))

necrosis_heatmap_nda = sitk.GetArrayFromImage(sitk.ReadImage(necrosis_heatmap))

tumor_heatmap_nda = sitk.GetArrayFromImage(sitk.ReadImage(tumor_heatmap))

print(np.count_nonzero(edema_heatmap_nda), np.sum(edema_heatmap_nda))

print(np.count_nonzero(necrosis_heatmap_nda), np.sum(necrosis_heatmap_nda))

print(np.count_nonzero(tumor_heatmap_nda), np.sum(tumor_heatmap_nda))