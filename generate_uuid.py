#!/usr/bin/env python
# coding: utf-8
import uuid
import glob
import os
import shutil

directory = '/home/devon/Desktop/BirdPi/temp img/'
image_list = glob.glob(directory + '**/*.jpg', recursive=True)
for file in image_list:
    uuid_temp = uuid.uuid1()
    label = file.split('/')[-2]
    new_name = '/home/devon/Desktop/BirdPi/images/{}/{}.jpg'.format(label, uuid_temp)
    os.rename(file, new_name)
    shutil.move(file, new_name)
    print(uuid_temp)
    print(label)
    print(file)
    print(new_name)



