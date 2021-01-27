# Written by Dr Daniel Buscombe, Marda Science LLC
# for the USGS Coastal Change Hazards Program
#
# MIT License
#
# Copyright (c) 2020, Marda Science LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ##========================================================

# allows loading of functions from the src directory
import sys
sys.path.insert(1, 'src')
import plotly.express as px
import os
from glob import glob
from datetime import datetime

from image_segmentation import extract_features, crf_refine
from annotations_to_segmentations import img_to_ubyte_array, label_to_colors
# import itertools
import numpy as np
from joblib import load

import matplotlib.pyplot as plt
from skimage.filters.rank import median
from skimage.morphology import disk
from skimage.io import imsave


## user defined parameters
##=========================================================

multichannel = True
intensity = True
texture = True
edges = True
sigma_min=0.5
sigma_max=16
downsample_value = 4
crf_theta_slider_value = 40
crf_mu_slider_value = 100
crf_downsample_factor = 2
median_filter_value = 3
RF_model_file = 'RandomForestClassifier-monterey.pkl.z' #'RandomForestClassifier-watermask-binary.pkl.z' #'RandomForestClassifier.pkl.z'

##========================================================

with open('classes.txt') as f:
    classes = f.readlines()

class_label_names = [c.strip() for c in classes]

NUM_LABEL_CLASSES = len(class_label_names)


if NUM_LABEL_CLASSES<=10:
    class_label_colormap = px.colors.qualitative.G10
else:
    class_label_colormap = px.colors.qualitative.Light24


# # we can't have less colors than classes
# assert NUM_LABEL_CLASSES <= len(class_label_colormap)
#
# class_labels = list(range(NUM_LABEL_CLASSES))


results_folder = 'results/results'+datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

try:
    os.mkdir(results_folder)
    print("Results will be written to %s" % (results_folder))
except:
    pass


files = sorted(glob('assets/*.jpg'))

files = [f for f in files if 'dash' not in f]

clf = load(RF_model_file) #load RF model from file

for file in files:
    print("Working on %s" % (file))
    img = img_to_ubyte_array(file) # read image into memory

    features = extract_features(
        img,
        multichannel=multichannel,
        intensity=intensity,
        edges=edges,
        texture=texture,
        sigma_min=sigma_min,
        sigma_max=sigma_max,
    ) # extract image features

    # downsample
    features = features[::downsample_value]

    # use model in predictive mode
    sh = features.shape
    features = features.reshape((sh[0], np.prod(sh[1:]))).T
    result = clf.predict(features)
    del features
    result = result.reshape(sh[1:])

    result, _ = crf_refine(result, img, crf_theta_slider_value, crf_mu_slider_value, crf_downsample_factor) #CRF refine

    # median filter
    result = median(result, disk(median_filter_value)).astype(np.uint8)

    imsave(file.replace('assets',results_folder).replace('.jpg','_label.png'),
            label_to_colors(result-1, img[:,:,0]==0, alpha=128, colormap=class_label_colormap, color_class_offset=0, do_alpha=False))

    imsave(file.replace('assets',results_folder).replace('.jpg','_label_greyscale.png'), result)
    del result, img

# turn to black and white / binary
###for file in *_greyscale.png; do convert -monochrome $file "${file%label_greyscale.png}mask.jpg"; done