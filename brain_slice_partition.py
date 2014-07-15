# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import argparse
import re
import subprocess

# <codecell>

# add file name argument.

parser = argparse.ArgumentParser()
parser.add_argument("img_file",help="choose file to crop include full path")
args = parser.parse_args()
img_path = args.img_file #path to the image to be partitioned
q = re.compile('_x..+')
txt_name = img_path.replace(re.findall(q,img_path)[0],'.txt').split('/')[-1]
path2txt = '/oasis/projects/nsf/csd181/yuncong/DavidData/bounding_box_data/'+txt_name

# <codecell>

#creates a folder for the partitions in the same folder as x5,x1.25,...,etc.  Working
p = re.compile('_.*_')
new_folder= img_path.replace('_z0.tif','/')
new_folder = new_folder.replace(re.findall(p,new_folder)[0],'_').split('/')[-2]
path2folder = '/oasis/projects/nsf/csd181/yuncong/DavidData/'+new_folder+'/'
cur_dir_list = subprocess.Popen(["ls","/oasis/projects/nsf/csd181/yuncong/DavidData/"],stdout=subprocess.PIPE).communicate()[0].split("\n")
if new_folder not in cur_dir_list:
    subprocess.call(['mkdir',path2folder])    

# <codecell>

#creates crop_dim ;list of tuples from txt_name.txt.  Working
crop_dim=[tuple(line.split()) for line in open(path2txt)]

# <codecell>

#uses subprocess with imagemagick to determine size and stores as w,h as a
#string variable.  Working

img_id = subprocess.Popen(["identify", img_path],stdout=subprocess.PIPE)
img_id_list=img_id.communicate()[0].split()
tot_w = img_id_list[2].split('x')[0]
tot_h = img_id_list[2].split('x')[1]

# <codecell>

#Crops image in accordance with the list crop_dim, and is saved into a new folder.
i=-1
j=0
old_crop_img_name = new_folder #gets the new file name

#List of all images already cropped to avoid overwriting previously cropped images in the folder
current_image_list = subprocess.Popen(["ls",path2folder],stdout=subprocess.PIPE).communicate()[0].split("\n")
for (x,y,w,h) in crop_dim:
    (x,y,w,h) = (int(int(tot_w)*float(x)),int(int(tot_h)*float(y)),int(int(tot_w)*float(w)),int(int(tot_h)*float(h)))
    i = i+1
    j = j+1
    new_crop_img_name = old_crop_img_name + '_' + str(i).zfill(4) +'.tif'
    while new_crop_img_name in current_image_list: #checks to make sure name isn't already present in folder
        i = i+1
        new_crop_img_name = old_crop_img_name + '_' + str(i).zfill(4) +'.tif'
    geom =str(w)+'x'+str(h)+'+'+str(x)+'+'+str(y)           
    subprocess.call(["convert",img_path,"-crop",geom,path2folder+new_crop_img_name])
    print "Processed Image "+str(j)

# <codecell>


