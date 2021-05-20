#!/usr/bin/env python3
"""
########### Import libs ###########
"""
# System tools
import os, sys
sys.path.append(os.path.join(".."))

# Data analysis and processing
import pandas as pd
import numpy as np

import tensorflow as tf
import tensorflow_hub as hub

import cv2

# Ross' homebrewed style utils
from utils.styletransfer import * #Import all functions

#Argparse
import argparse
from argparse import RawTextHelpFormatter


def main():
    """
    ########### Argparse ###########
    """
    #Create argparser
    ap = argparse.ArgumentParser(description = "Generate new skins with style transfer. New images will be located in the subfolder 'style_transfer' in the output folder", formatter_class = RawTextHelpFormatter)
    
    #Content image
    ap.add_argument("-c", "--content_image",
                   required = False,
                   type = str,
                   default = "Butterfly_Knife_Tiger_Tooth.png",
                   help =
                   "[INFO] The content image for style transfer \n"
                   "[INFO] Must be located in the subfolder 'all_weapons' in the data folder \n"
                   "[TYPE] str \n"
                   "[DEFAULT] M4A4_Bullet_Rain.png \n"
                   "[EXAMPLE] --content_image M4A1-S_Master_Piece.png")
    #Style image
    ap.add_argument("-st", "--style_image",
                   required = False,
                   type = str,
                   default = "Butterfly_Knife_Damascus_Steel.png",
                   help =
                   "[INFO] The style image for style transfer. \n"
                   "[INFO] Must be located in the subfolder 'all_weapons' in the data folder \n"
                   "[TYPE] str \n"
                   "[DEFAULT] M4A4_Buzz_Kill.png \n"
                   "[EXAMPLE] --style_image M4A1-S_Knight.png")
    #output image
    ap.add_argument("-o", "--output_image",
                   required= False,
                   type = str,
                   default = "style_transferred_img.png",
                   help = 
                   "[INFO] The name of the plot with all images (content, style, and stylized image) \n"
                   "[INFO] It will be located in the subfolder 'style_transfer' in the output folder \n"
                   "[TYPE] str \n"
                   "[DEFAULT] style_transferred_img.png \n"
                   "[EXAMPLE] --output_image new_style_m4a4.png")
    
    ap.add_argument("-i", "--image_size",
                   required = False,
                   type = int,
                   default = (256, 256),
                   nargs = "*",
                   help =
                   "[INFO] The size of the input images \n"
                   "[INFO] The content image and the style image will be resized to the specified dimensions \n"
                   "[INFO] First value represents height, second value represents width \n"
                   "[TYPE] List of ints \n"
                   "[DEFAULT] 256 256 \n"
                   "[EXAMPLE] --image_size 120 120")
    
    # Return arguments
    args = vars(ap.parse_args())
    image_size = args["image_size"]
    #Save arguments in variables
    content_image = st_load(os.path.join("..", "data", "all_weapons", args["content_image"]), image_size=(image_size[0], image_size[1]))
    style_image = st_load(os.path.join("..", "data", "all_weapons", args["style_image"]), image_size=(image_size[0], image_size[1]))
    output_image = os.path.join("..", "output", "style_transfer", args["output_image"])
    
    hub_handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
    hub_module = hub.load(hub_handle)

    outputs = hub_module(content_image, style_image) #Get outputs from model
    
    stylized_image = outputs[0] #Get stylized image

    show_n([content_image, style_image, stylized_image],
       titles=['Original skin', 'Style skin', 'Stylized skin'], output = output_image)
    
    print("Done, The stylized image can be found in the subfolder 'style_transfer' in the 'output' folder")
#Define behaviour when called from terminal
if __name__ == "__main__":
    main()