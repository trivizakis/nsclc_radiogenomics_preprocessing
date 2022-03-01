#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: trivizakis

@github: github.com/trivizakis
"""

import os
import nibabel
import numpy as np
from scipy import ndimage
# import SimpleITK as sitk

def resample(image, pixel_spacing, new_spacing):    
    resize_factor = pixel_spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = pixel_spacing / real_resize_factor
    
    resampled_image = ndimage.interpolation.zoom(image, real_resize_factor)
    
    return resampled_image, new_spacing

dataset_dir = "dataset/to_segment/"

# cts_mins=[]
# cts_maxs=[]
# pets_mins=[]
# pets_maxs=[]
spacings = []
for _,patients,_ in os.walk(dataset_dir):
    for patient in patients:
        print(patient)
        for _,_,examinations in os.walk(dataset_dir+patient):
            for examination in examinations:
                print(examination)
                #extract statistics
                # vol = nibabel.load(dataset_dir+patient+"/"+examination).get_data() #get the numpy array
                #CT min/max
                # if "_ct_" in examination:
                #     cts_mins.append(vol.ravel().min()) #-3024
                #     cts_maxs.append(vol.ravel().max()) #3071
                # elif "ct" in examination:
                #     continue
                # else:
                ##PET max pixel intensity 
                #     pets_mins.append(vol.ravel().min()) #MIN: 0
                #     pets_maxs.append(vol.ravel().max()) #MAX: 1486250, MINmax: 30111, meanOfMaxes: 207979.64, stdOfMaxes: 194756.12
                
                #save npy
                vol = nibabel.load(dataset_dir+patient+"/"+examination)
                spacings.append(np.array((abs(vol.header["srow_x"][0]),abs(vol.header["srow_y"][1]),abs(vol.header["srow_z"][2]))))
                spacing = np.array((abs(vol.header["srow_x"][0]),abs(vol.header["srow_y"][1]),abs(vol.header["srow_z"][2])))
                imgs = vol.get_data()
                desired_spacing = np.array(2,2,3)#THIS VALUE MUST BE OPTIMIZED to both maintain spatial information and harmonize the scans in the same scale space
                print("Before resampling: "+str(imgs.shape)+", "+str(spacing))
                fixed, new_spacing = resample(imgs, spacing, (desired_spacing))
                print("After resampling: "+str(fixed.shape)+", "+str(new_spacing))

                max_ = fixed.ravel().max()
                min_ = fixed.ravel().min()
                final = (((fixed-min_)/max_-min_)*255).astype(np.uint8) #scanner intensities to uint8, per scan!
                np.save(dataset_dir+patient+"/"+examination[:-7]+str(desired_spacing), final)
               
#MEAN spacing (x,y,z)
#2.5
#2.5
#3.3



