'''
@author: pkao

This code plots the histogram of different lesions in different brain parcellation regions
'''

import matplotlib
matplotlib.use('Agg')
import SimpleITK as sitk
import numpy as np
import os
import matplotlib.pyplot as plt

def lesionHistogramBP(heatmap_location, brainparcellation_location, MNI152_brain_mask_location, nameOfHeatmap):
	''' output the histogram of different lesions in differnt brain parcellation'''

	# get the numpy array from brain parcellation in MNI152 space
	BP_img = sitk.ReadImage(brainparcellation_location)
	BP_nda = sitk.GetArrayFromImage(BP_img)

	print('Brain parcellation has ' + str(np.amax(BP_nda).astype(int)) + ' subregions.')


	# get the numpy array from heat maps in MNI152 space

	heatmap_img = sitk.ReadImage(heatmap_location)
	heatmap_nda = sitk.GetArrayFromImage(heatmap_img)
	MNI152_brain_mask_img = sitk.ReadImage(MNI152_brain_mask_location)
	MNI152_brain_mask_nda = sitk.GetArrayFromImage(MNI152_brain_mask_img)

    #print MNI152_brain_mask_nda.shape
        
	hist_lesion = np.zeros(np.amax(BP_nda).astype(int)+1)
	bp_regions = np.zeros(np.amax(BP_nda).astype(int)+1)
	for i in range(np.amax(BP_nda).astype(int)+1):
		if i == 0:
			bp_regions[i] = np.count_nonzero(np.logical_and(MNI152_brain_mask_nda, BP_nda == 0))
		if i != 0:
			bp_regions[i] = np.count_nonzero(BP_nda == i)

        #print bp_regions 




	for i in range(BP_nda.shape[0]):
		for j in range(BP_nda.shape[1]):
			for k in range(BP_nda.shape[2]):
				if heatmap_nda[i,j,k] > 0:
					hist_lesion[BP_nda[i,j,k].astype(int)] = hist_lesion[BP_nda[i,j,k].astype(int)] + heatmap_nda[i,j,k]
	print('Normalized histogram for ' + nameOfHeatmap + ' brain parcellation subregions: ')
	
	normalized_hist_lesion =  np.divide(hist_lesion, bp_regions)
	
	'''print(normalized_hist_lesion)
	plt.figure()
	plt.bar(np.arange(len(normalized_hist_lesion)), normalized_hist_lesion, align='center', alpha=0.5)
	plt.ylabel('Normalzed Number of Voxel')
	plt.xticks(np.arange(len(hist_lesion)))
	plt.title('Normalized histogram for ' + nameOfHeatmap + ' in HarvardOxford')
	plt.savefig('./histogram/The_normalized_histogram_for_' + nameOfHeatmap + '_in_HarvardOxford_parcellation_subregions.png')
	plt.clf()'''
	return normalized_hist_lesion


#BPlocation = '/usr/share/fsl/data/atlases/HarvardOxford/HarvardOxford-sub-maxprob-thr0-1mm.nii.gz'
BPlocation = './VOI/VOI-1mm.nii.gz'

heatMapsLocation = './heatmaps/'
MNI152_brain_mask_location = './MNI152_T1_1mm_brain_mask.nii.gz'

if not os.path.exists('./histogram'):
	os.mkdir('./histogram')

#completeTumorHeatMap = os.path.join(heatMapsLocation, 'heatmapCompleteTumorMNI152.nii.gz')
#tumorCoreHeatMap = os.path.join(heatMapsLocation, 'heatmapTumorCoreMNI152.nii.gz')
edemaHeatMap = os.path.join(heatMapsLocation, 'edema_heatmap.nii.gz')
enhancingTumorHeatMap = os.path.join(heatMapsLocation, 'tumor_heatmap.nii.gz')
necrosisHeatMap = os.path.join(heatMapsLocation, 'necrosis_heatmap.nii.gz')

#lesionHistogramBP(completeTumorHeatMap, BPlocation, MNI152_brain_mask_location, 'Complete Tumor')
#lesionHistogramBP(tumorCoreHeatMap,BPlocation, MNI152_brain_mask_location, 'Tumor Core')
normalized_histogram_edema = lesionHistogramBP(edemaHeatMap,BPlocation, MNI152_brain_mask_location, 'Edema')
normalized_histogram_tumor = lesionHistogramBP(enhancingTumorHeatMap, BPlocation, MNI152_brain_mask_location, 'Enhancing Tumor')
normalized_histogram_necrosis = lesionHistogramBP(necrosisHeatMap, BPlocation, MNI152_brain_mask_location, 'Necrosis')

n_regions = 10

fig, ax = plt.subplots()
index = np.arange(n_regions)
bar_width = 0.2
opacity = 0.6


plt.figure()
rects1 = plt.bar(index , normalized_histogram_necrosis, bar_width, 
                 alpha=opacity,
                 color='b',
                 label='Necrosis & Non-Enhancing Tumor')

rects2 = plt.bar(index + bar_width, normalized_histogram_edema, bar_width,
                 alpha=opacity,
                 color='g',
                 label='Edema')

rects3 = plt.bar(index - bar_width, normalized_histogram_tumor, bar_width,
                 alpha=opacity,
                 color='r',
                 label='Enhancing Tumor')
plt.xlabel('Voxel-of-Interest Map Label', size=25)
plt.ylabel('Percentage', size=25)
plt.legend(loc = 'best', fontsize=10)
plt.xticks(np.arange(n_regions), size = 20)
plt.yticks(np.arange(0, 30, 5), size = 15)
plt.tight_layout()
plt.show()
plt.savefig('./histogram/VOI_histogram.png')