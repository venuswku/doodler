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
import sys, os, getopt
sys.path.insert(1, '../src')
# from annotations_to_segmentations import *
from image_segmentation import *

from glob import glob
import skimage.util
from tqdm import tqdm

from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
import matplotlib
import matplotlib.pyplot as plt

###===========================================================
try:
    from my_defaults import *
    print("Your session defaults loaded")
except:
    from defaults import *


###===========================================================
def do_viz_npz(npz_type,show_plot,print_fig):

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    direc = askdirectory(title='Select directory of results (annotations)', initialdir=os.getcwd()+os.sep+'results')
    files = sorted(glob(direc+'/*.npz'))

    if npz_type==0:
        files = [f for f in files if 'labelgen' not in f]
        files = [f for f in files if '4zoo' not in f]

    if npz_type==1:
        files = [f for f in files if 'labelgen' in f]

    if npz_type==2:
        files = [f for f in files if '4zoo' in f]

    if npz_type==3:
        files = [f for f in files if 'proc' in f]

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    classfile = askopenfilename(title='Select file containing class (label) names', filetypes=[("Pick classes.txt file","*.txt")])

    with open(classfile) as f:
        classes = f.readlines()
    class_string = '_'.join([c.strip() for c in classes])


    class_label_names = [c.strip() for c in classes]

    NUM_LABEL_CLASSES = len(class_label_names)

    if NUM_LABEL_CLASSES<=10:
        class_label_colormap = px.colors.qualitative.G10
    else:
        class_label_colormap = px.colors.qualitative.Light24

    # we can't have fewer colors than classes
    assert NUM_LABEL_CLASSES <= len(class_label_colormap)

    colormap = [
        tuple([fromhex(h[s : s + 2]) for s in range(0, len(h), 2)])
        for h in [c.replace("#", "") for c in class_label_colormap]
    ]

    cmap = matplotlib.colors.ListedColormap(class_label_colormap[:NUM_LABEL_CLASSES])

    #### loop through each file
    for anno_file in tqdm(files):

        # print("Working on %s" % (file))
        print("Working on %s" % (anno_file))
        dat = np.load(anno_file)
        data = dict()
        for k in dat.keys():
            try:
                data[k] = dat[k]
            except:
                pass
        del dat

        if npz_type==0:
        #if 'image' in data.keys():

            if print_fig:
                plt.subplot(121)
                plt.imshow(data['image']); plt.axis('off')
                plt.imshow(data['doodles'], alpha=0.5, vmin=0, vmax=NUM_LABEL_CLASSES, cmap=cmap) #'inferno')
                plt.axis('off')

                plt.subplot(122)
                plt.imshow(data['image']); plt.axis('off')
                plt.imshow(np.argmax(data['label'],-1), alpha=0.5, vmin=0, vmax=NUM_LABEL_CLASSES, cmap=cmap) #'inferno')
                plt.axis('off')
                plt.savefig(anno_file.replace('.npz','_disp.png'), dpi=200, bbox_inches='tight')
                plt.close()

            if show_plot:
                plt.subplot(121)
                plt.imshow(data['image']); plt.axis('off')
                plt.imshow(data['doodles'], alpha=0.5, vmin=0, vmax=NUM_LABEL_CLASSES, cmap=cmap) #'inferno')
                plt.axis('off')

                plt.subplot(122)
                plt.imshow(data['image']); plt.axis('off')
                plt.imshow(np.argmax(data['label'],-1), alpha=0.5, vmin=0, vmax=NUM_LABEL_CLASSES, cmap=cmap) #'inferno')
                plt.axis('off')
                plt.show()

        if npz_type==1: ##labelgen

            if print_fig:
                plt.subplot(121)
                plt.imshow(data['image']); plt.axis('off')
                plt.imshow(data['doodles'], alpha=0.5, vmin=0, vmax=NUM_LABEL_CLASSES, cmap=cmap) #'inferno')
                plt.axis('off')

                plt.subplot(122)
                plt.imshow(data['image']); plt.axis('off')
                plt.imshow(np.argmax(data['label'],-1), alpha=0.5, vmin=0, vmax=NUM_LABEL_CLASSES, cmap=cmap) #'inferno')
                plt.axis('off')
                plt.savefig(anno_file.replace('.npz','_disp.png'), dpi=200, bbox_inches='tight')
                plt.close()

            if show_plot:
                plt.subplot(131)
                plt.imshow(data['image']); plt.axis('off')
                plt.imshow(data['doodles'], alpha=0.5, vmin=0, vmax=NUM_LABEL_CLASSES, cmap=cmap) #'inferno')
                plt.axis('off')

                plt.subplot(132)
                plt.imshow(data['image']); plt.axis('off')
                plt.imshow(np.argmax(data['label'],-1), alpha=0.5, vmin=0, vmax=NUM_LABEL_CLASSES, cmap=cmap) #'inferno')
                plt.axis('off')

                plt.subplot(133)
                plt.imshow(data['image']); plt.axis('off')
                # try:
                plt.imshow(np.argmax(data['final_label'],-1), alpha=0.5, vmin=0, vmax=NUM_LABEL_CLASSES, cmap=cmap) #'inferno')
                # except:
                #     plt.imshow(np.argmax(data['final_label'][:,:,:NUM_LABEL_CLASSES,0],-1), alpha=0.5, vmin=0, vmax=NUM_LABEL_CLASSES, cmap=cmap) #'inferno')

                plt.axis('off')

                plt.show()

        if npz_type==2: #4zoo

            if print_fig:
                plt.imshow(data['arr_0']); plt.axis('off')
                plt.imshow(np.argmax(data['arr_1'],-1), alpha=0.5, vmin=0, vmax=NUM_LABEL_CLASSES, cmap=cmap) #'inferno')
                plt.axis('off')
                plt.savefig(anno_file.replace('.npz','_disp.png'), dpi=200, bbox_inches='tight')
                plt.close()

            if show_plot:
                plt.imshow(data['arr_0']); plt.axis('off')
                plt.imshow(np.argmax(data['arr_1'],-1), alpha=0.5, vmin=0, vmax=NUM_LABEL_CLASSES, cmap=cmap) #'inferno')
                plt.axis('off')
                plt.show()


        if npz_type==3: #pred

            if print_fig:
                plt.imshow(data['image']); plt.axis('off')
                plt.imshow(data['final_label'], alpha=0.5, vmin=0, vmax=NUM_LABEL_CLASSES, cmap=cmap) #'inferno')
                plt.axis('off')
                plt.savefig(anno_file.replace('.npz','_disp.png'), dpi=200, bbox_inches='tight')
                plt.close()

            if show_plot:
                plt.imshow(data['image']); plt.axis('off')
                plt.imshow(data['final_label'], alpha=0.5, vmin=0, vmax=NUM_LABEL_CLASSES, cmap=cmap) #'inferno')
                plt.axis('off')
                plt.show()

###==================================================================
#===============================================================
if __name__ == '__main__':

    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"h:t:p:l:")
    except getopt.GetoptError:
        print('======================================')
        print('python viz_npz.py [-t npz type {0}/1/2 -p show plot {1}/0 -l print fig 1/{0} ]') #
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('======================================')
            print('Example usage: python viz_npz.py')
            print('npz_type codes. 0 (default) = normal, 1=labelgen, 2=npz_zoo, 3=pred')
            print('======================================')
            sys.exit()
        elif opt in ("-p"):
            show_plot = arg
            show_plot = bool(show_plot)
        elif opt in ("-l"):
            print_fig = arg
            print_fig = bool(print_fig)
        elif opt in ("-t"):
            npz_type = arg
            npz_type = int(npz_type)

    if 'show_plot' not in locals():
        show_plot = True
    if 'print_fig' not in locals():
        print_fig = False
    if 'npz_type' not in locals():
        npz_type = 0

    #ok, dooo it
    do_viz_npz(npz_type,show_plot,print_fig)