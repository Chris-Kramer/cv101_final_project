#!/usr/bin/env python3
"""
########### Import libs ###########
"""
# System tools
import os, sys
sys.path.append(os.path.join(".."))
# Data processing
import pandas as pd
#Timer
from tqdm import tqdm

# Data analysis and processing
import pandas as pd
import numpy as np
import math
#cleaning path names
import re

# Machine learning
from tensorflow.keras.applications.vgg16 import VGG16 #VG 16 model
from sklearn.neighbors import NearestNeighbors

# Ross' homebrewed functions
from utils.image_search import * #Import all functions

#Argparse
import argparse
from argparse import RawTextHelpFormatter

def main():
    """
    ########### Argparse ###########
    """
    # Create argparser
    ap = argparse.ArgumentParser(description = "Search for skins that share the same features. The output will be in the folder 'find_skins'", formatter_class = RawTextHelpFormatter)
    # Argument
    ap.add_argument("-i", "--image",
                   required = False,
                   default = "AK-47_Aquamarine_Revenge.png",
                   type = str,
                   help = 
                   "[INFO] The target image that you wan't to find nearest neighbours for. \n"
                   "[INFO] Must be located in the subfolder 'all_weapons' in the 'data folder. \n'"
                   "[TYPE] str \n"
                   "[DEFAULT] Butterfly_Knife_Crimson_Web.png \n"
                   "[EXAMPLE] --image AK-47_Aquamarine_Revenge.png")
    
    
    # Neighboru
    ap.add_argument("-rn", "--n_neighbours",
                   required = False,
                   default = 8,
                   type = int,
                   help =
                   "[INFO] How many neighbours to target skin should be returned in the output folder. \n"
                   "[TYPE] int \n"
                   "[DEFAULT] 8 \n"
                   "[EXAMPLE] --n_neighbours 5")
    
    # Return arguments
    args = vars(ap.parse_args())
    # Save arguments in variables (for readability)
    n_neighbours = args["n_neighbours"]
    image_name = args["image"]
    
    """
    ########### Read images and extract features ###########
    """
    # Load model
    model = VGG16(weights='imagenet', 
                  include_top=False,# Remove the fully connected network
                  pooling='avg', # Do average pooling
                  input_shape=(256, 192, 3)) #The size of images
    
    print("Loading image ...")
    #Target image
    image = cv2.imread(os.path.join("..", "data", "all_weapons", image_name))
    #DIrectory with image neighbours
    root_dir = os.path.join("..", "data", "all_weapons")
    #Filenames in root directory
    filenames = sorted(get_file_list(root_dir))
    
    print("Extracting features ...")
    #The index for the target image
    target_index = 0
    feature_list = []
    #Loop through the indexes of all files
    for i in tqdm(range(len(filenames))):
        #Save index of target image
        if str(filenames[i]) == str(image):
            target_index = i
        # Append features   
        feature_list.append(extract_features(filenames[i], model))
    
    """
    ########### Find nearest neighbours ###########
    """

    print("Finding neighbours ...")
    #Initialize nearest neighbour algorithm
    neighbors = NearestNeighbors(n_neighbors=n_neighbours + 1,
                             algorithm='brute', #Brute is good for smaller datasets. Compares everything
                             metric='cosine').fit(feature_list) #Cosine similarity
    
    #Find indeces and distances of k neighrest neighbours
    distances, indices = neighbors.kneighbors([feature_list[target_index]]) 
    
    """
    ########### Save results to folder and csv###########
    """ 
    print("Saving neighbours ...")
    # create dataframe
    df = pd.DataFrame(columns = ["filename", "neighbour_nr"])
    
    #Create a dir with results
    # Remove everything after punctuation
    target_name = re.findall("[^\.]*", image_name)[0]
    dir_path = os.path.join("..", "output", "find_skins", target_name)
    os.makedirs(dir_path, exist_ok = True)
    
    #Save target image in dir
    image_path = os.path.join(dir_path, "TARGET_" + image_name )
    cv2.imwrite(image_path, image)
    
    for i in range(1, n_neighbours + 1): #Plus one since range excludes last value
        print(f"[INFO] Target {i}, Image: {filenames[indices[0][i]]}, Distance: {distances[0][i]}, Index: {indices[0][i]}")
        neighbour_image = cv2.imread(filenames[indices[0][i]])
        neighbour_name = os.path.join(dir_path, "neighbour_" + str(i) + ".png")
        cv2.imwrite(neighbour_name, neighbour_image)
        df_row = {"filename": filenames[indices[0][i]], "neighbour_nr": i}
        df = df.append(df_row, ignore_index = True)
    
    # Save df as csv
    df.sort_values(by=["neighbour_nr"], ascending = True)
    df.to_csv(os.path.join(dir_path, target_name + "_neighbours.csv"), index=False)
    print(f"Done the results can be found in {dir_path}")
    
#Define behaviour when called from command line
if __name__ == "__main__":
    main()