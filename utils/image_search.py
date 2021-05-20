#!/usr/bin/env python3
import numpy as np
from numpy.linalg import norm
import cv2
import os
from tensorflow.keras.preprocessing.image import load_img, img_to_array # load functions
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input #Model with 50 layer, so very deep

def extract_features(img_path, model):
    """
    Extract features from image data using pretrained model (e.g. VGG16)
    Takes an image path and the model we are using
    Then it load an image and reshapes it.
    It is then converted a np array
    We then predict the features
    We flatten the image
    Normalise features
    It essentially gives out the feature embeddings 
    """
    # Define input image shape - remember we need to reshape
    input_shape = (256, 192, 3) #I'm setting my data to half of the actual size (this is done for effeciency)
    # load image from file path
    img = load_img(img_path, target_size=(input_shape[0], 
                                          input_shape[1]))
    # convert to array
    img_array = img_to_array(img)
    # expand to fit dimensions
    expanded_img_array = np.expand_dims(img_array, axis=0)
    # preprocess image - see last week's notebook
    preprocessed_img = preprocess_input(expanded_img_array)
    # use the predict function to create feature representation
    features = model.predict(preprocessed_img)
    # flatten
    flattened_features = features.flatten()
    # normalise features
    normalized_features = flattened_features / norm(features)
    return flattened_features

def get_file_list(root_dir):
    #This function iterates over a dir of images and creates a list 
    # define valid file extensions
    extensions = ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG']
    # create empty file list
    file_list = []
    # initialise counter
    counter = 1
    # use os.walk to create a list of image filepaths
    for root, directories, filenames in os.walk(root_dir):
        for filename in filenames:
            # keep only those with valid extensions
            if any(ext in filename for ext in extensions):
                file_list.append(os.path.join(root, filename))
                # increment counter
                counter += 1
    return file_list

#Don't run from command line
if __name__ == "__main__":
    pass