#!/usr/bin/env python
# coding: utf-8
from random import shuffle
import glob
import os 
import numpy as np
import pickle

import PIL.Image
from IPython.display import display
import time
from datetime import timedelta

def make_image_label_pickle(directory, num_species, nwidth, nheight):
    # Start time.
    start_time = time.time()
    # Get the labels from the directory 
    labels = [x[1] for x in os.walk(directory)][0] 
    NUM_LABELS = len(labels)
    labels.sort()
    # build dictionary for indexes
    label_indexes = {labels[i]: i for i in range(0, len(labels))}  
    data_files = glob.glob(directory + '**/*.jpg', recursive=True)
    # shuffle the data 
    shuffle(data_files)
    num_data_files = len(data_files)
    data_labels = []
    # build the labels 
    for file in data_files:
        # file will be /data/{category}/image_name.jpg so we 
        # extract the category from there
        label = file.split('/')[-2]
        data_labels.append(label_indexes[label])

#     def one_hot(label_array, num_classes):
#         print(type(label_array))
#         print(label_array)
#         print(label_array.reshape(-1))
#         print(np.eye(2)[2])
#         return np.squeeze(np.eye(num_classes)[label_array.reshape(-1)])

    data_labels = np.array(data_labels)
    # we have 200 species in our dataset
#     data_labels = one_hot(data_labels, num_species) 
    # The percentage of the data which will be used in the test set
    TRAIN_TEST_SPLIT = 0.10
    nr_test_data = int(num_data_files * TRAIN_TEST_SPLIT)
    # Create arrays of the filepaths
    train_images = data_files[nr_test_data:]
    test_images = data_files[:nr_test_data]
    train_labels = data_labels[nr_test_data:]
    test_labels = data_labels[:nr_test_data]
    # Start the pickling process
    s = (len(train_images), nwidth, nheight, 3)
    allImage_train = np.zeros(s)
    allImage_test = np.zeros(s)
    i = 0
    j = 0
    # We save a pickle file of the images in each set.
    for filename_train in train_images:
        try:
            image_train = PIL.Image.open(filename_train)
            image_train = image_train.resize((nwidth, nheight))
            image_train = np.array(image_train)
            image_train = np.clip(image_train / 255.0, 0.0, 1.0)
            try:
                allImage_train[i] = image_train
                i += 1
            except:
                pass
                i += 1
        except:
            pass
#             image_train.reshape(nwidth, nheight, 3)
#             allImage_train[i] = image_train
    pickle.dump(allImage_train, open('images' + '.p', "wb"), protocol=4)
#     for filename_test in test_images:
#         image_test = PIL.Image.open(filename_test)
#         image_test = image_test.resize((nwidth, nheight))
#         image_test = np.array(image_test)
#         image_test = np.clip(image_test / 255.0, 0.0, 1.0)
#         print(image_test.shape)
#         try:
#             allImage_test[i] = image_test
#             j += 1
#         except:
#             pass
#             j += 1
        
#     pickle.dump(allImage_test, open('test' + '.p', "wb"), protocol=4)
    # Ending time.
    end_time = time.time()
    # Total run time.
    time_dif = end_time - start_time
    # Print the run time.
    print("Time to pickle: " + str(timedelta(seconds=int(round(time_dif)))))
    return train_labels

if __name__ == '__main__':
    assert num_data_files == len(data_labels)
    assert len(train_labels) + len(test_labels) == num_data_files * 0.9
    assert len(test_images) + len(train_images) == num_data_files * 0.1

