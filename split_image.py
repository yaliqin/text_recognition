# -*- coding:utf-8 -*-
import os
import sys
from os import path
import glob
from PIL import Image
from reorder_axle import reorder_axle


sys.path.append(os.getcwd())
sys.path.append(path.abspath('/Users/ally/Documents/GitHub/text_recognition'))

def split_image(input_location_file,input_image_file,img_out_file_prefix,output_path):
    data = reorder_axle(input_location_file)
    # file = os.path.basename(input_image_file)
    im = Image.open(input_image_file)
    im_w, im_h = im.size
    split_number = len(data)
    print('Image width:%d height:%d  will split into (%d) ' % (im_w, im_h, split_number))
    i=0
    for line in data: #data is stored as left,up,right,lower
        box = [int(x) for x in line.split(",")]
        print(box)
        # for item in data[num]:
        #     box.append(int(item))
        piece = im.crop(box)
        # tmp_img = Image.new('L', (im_w, im_h), 255)
        # tmp_img.paste(piece)
        img_path = os.path.join(output_path,'split_image_'+ img_out_file_prefix+'_'+("%d.png" %i))
        piece.save(img_path)
        print('split_image_'+ img_out_file_prefix+'_'+("%d.png" %i))
        i = i +1
    return split_number