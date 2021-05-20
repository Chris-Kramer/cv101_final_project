# Final Project - Skin Tools: Nearest Neighbours
**Christoffer Kramer**  
**20-05-2021**  
**Link to pixplot visualization:** http://kramer-final-project.000webhostapp.com/  

## Description
This repository uses image embeddings as a tool for investigating cosmetic virtual items, also known as skins, in the video game Counter-Strike Global Offensive (CSGO). I’ve used image embeddings to create the following tools:
- Style-transfer (style_transfer.py)
- Pixplot visualizations 
- A search tool (find_skins.py)  

The search tool takes an input image and finds the specified number of nearest embedding neighbors. The style transfer tool takes two inputs: a content image and a style image. It then uses arbitrary style transfer to create a new skin.  
I’ve put the pixplot visualizations on a small website, which can be found here: http://kramer-final-project.000webhostapp.com/index.html. Note that the website uses a free hosting service, and I’m not trained in optimizing performance on websites. Therefore, the website might be a bit slow, but it works. However, you need to have WebGL enabled (this is enabled by default in most modern browsers) for the site to work.
You can read more about pixplot, and how it works, here: https://dhlab.yale.edu/projects/pixplot/. 


## Methods
To generate the pixplot visualization, I’ve created a script for web scraping the image and the associated metadata for each skin. I’m web scraping from this website: https://www.csgodatabase.com/weapons/. The image embeddings for style transfer come from the magenta model https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2, and the search tool uses the VGG16 model https://www.tensorflow.org/api_docs/python/tf/keras/applications/VGG16 to find the K-nearest embedding neighbors.  

## Usage  
This should work on both Linux, Mac, and Windows. However, If you are running on a local windows machine, you should run it from a bash emulator such as git bash. 
Before you can run the style transfer script and the search tool, you have to get the data. This data can be gathered by using the web scrape script.
However, since websites change all the time, my script might not work in the future. Therefore, I’ve also uploaded my data set to Kaggle:
www.kaggle.com/dataset/f278d9db7acf516c92626e8407b3c54cc33e11825e36935d9d8bdacbaff88188  
 
**Step 1 - Clone repo:**
- open terminal
- Navigate to destination for repo
- type the following command
 ```console
git clone https://github.com/Chris-Kramer/cv101_final_project.git  
 ```
**Step 2 - Navigate to folder:**
- Navigate to the folder "cv101_assignment_3".
```console
cd cv101_final_project
```  
**Step 3 - Run bash scripts**  
- Webscrape  
```console
bash run-webscrape.sh
```  
- Style transfer  
```console
bash run-style_transfer.sh
```  
- Search tool  
```console
bash run-find_skins.sh
```  
The script will print out `DONE! THE CROPPED PICTURES AND THE PICTURE OF CONTOUR LINES ARE LOCATED IN THE FOLDER'output'` when it is done running. 

### Running on windows without a bash emulator
If you're running on a local windows machine, and don't have a bash emulator, you have to set up a virtual environment, activate it, install dependencies (requirements.txt), and then run the python scripts manually from the src folder  

## Output
### Web scraping (webscrape.py)
The script for web scraping creates 4 subfolders in the data folder: “all_weapons”, “rarity”, “knives”, and “weapon_model”. All folders essentially contain the same images, however, the folders are structured differently, so they can be used for image classification (which I did in the previous portfolio by using the folder “weapon_model” to classify weapon models) and for creating the pixplot visualizations. Moreover, it also creates 3 CSV files containing metadata. Two of those files (“pixplot_metadata.csv” and “pixplot_metadata_knives.csv”) are used to generate metadata for the pixplot visualizations.  
- data  
    - pixplot_metadata.csv
    - pixplot_metadata_knives.csv
    - metadata.csv
    - all_weapons
        - skin_img1.png
        - skin_img2.png
        - etc.
    - rarity
        - Classified
            - skin_img1.png
            - skin_img2.png
            - etc.
        - Consumer
            - skin_img1.png
            - skin_img2.png
            - etc.
    - weapon_model
        - Ak-47
            - skin_img1.png
            - skin_img2.png
            - etc.
        - AUG
            - skin_img1.png
            - skin_img2.png
            - etc.
        - knives
            - skin_img1.png
            - skin_img2.png
            - etc.

### Seach tool (find_skins.py)
This script creates a subfolder with the input image’s name in the folder “find_skins”. The folder contains the target image, the n nearest neighbors (n can be specified by the user), and a CSV file with the neighbors' filenames and their neighbor number.
- output
    - find_skins_dir
        - input_image_name_dir
            - neighbours.csv
            - TARGET_image_name.png
            - neighbour_1.png
            - neighbour_2.png
            - etc.

### Style transfer (style_transfer.py)
The style transfer script creates a single plot containing the original image, the style image, and the stylized image. The output is located in the subfolder “style_tranfer” and the name of the output image can be specified by the user.  

## Parameters
The search tool and the style transfer tool takes parameters. They have been supplied with default values.  
### run-find_skins.sh / find_skins.py
- `--image ` The target image that you wan't to find nearest neighbours for. It must be located in the subfolder “all_weapons” in the 'data folder.  
    - DEFAULT = Butterfly_Knife_Crimson_Web.png  
- `--n_neighbours ` How many neighbours to target image should be returned as output.  
    - DEFAULT = 8  
#### Example  
**With bash script:**  
```console
bash run-find_skins.sh --image AK-47_Baroque_Purple.png --n_neighbours 6
```  
**Without bash script:**  
```console
python find_skins.py --image AK-47_Baroque_Purple.png --n_neighbours 6
```
### run-style_tranfer.sh / style_transfer.py 
- `--content_image` The content image for style transfer. It must be located in the subfolder “all_weapons” in the data folder.  
    - DEFAULT = M4A4_Bullet_Rain.png
- `--style_image` The style image for style transfer. It must be located in the subfolder “all_weapons” in the data folder. 
    - DEFAULT = M4A4_Buzz_Kill.png 
- `--output_image` The name of the plot with all images (content, style, and stylized image). It will be located in the subfolder “style_transfer” in the output folder.  
    - DEFAULT = style_transferred_img.png  
- `--image_size` The size of the input images. The content image and the style image will be resized to the specified dimensions. First value represents height, second value represents width.  
    - DEFAULT = 256 256  
   
#### Example:  
_With bash script_
```console
bash run-style_tranfer.sh --content_image AK-47_Hydroponic.png --style_image AK-47_Fuel_Injector.png --output_image AK-47_hydro_fuel.png --image_size 300 300
```  
_Without bash script_
```console
python style_tranfer.py --content_image AK-47_Hydroponic.png --style_image AK-47_Fuel_Injector.png --output_image AK-47_hydro_fuel.png --image_size 300 300
```  