#!/usr/bin/env python3
"""
########### Import libs ##########
"""
# Webscraping
from urllib.error import HTTPError #Handling errors
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4  import BeautifulSoup 
# System tool
import os
# Image processing
import cv2
# Data processing
import pandas as pd
# Data cleaning
import re
import math
from datetime import datetime

# Main function
def main():
    # Create csv-file with metadata
    df_pixplot = pd.DataFrame(columns = ["filename", "category", "permalink", "description"])
    df_metadata = pd.DataFrame(columns = ["filename", "weapon_model", "rarity", "link", "date", "factory_new_price"])

    #Make dir with all_weapons
    os.makedirs(os.path.join("..", "data", "all_weapons"), exist_ok = True)    
    #Make dir with knives
    os.makedirs(os.path.join("..", "data", "knives"), exist_ok = True)
    #Make dir with weapon_model
    os.makedirs(os.path.join("..", "data", "weapon_model"), exist_ok = True)
    #Make dir with rarirty
    os.makedirs(os.path.join("..", "data", "rarity"), exist_ok = True)
    
    #List for filtering knives (used for creating metadata for knives)
    knives = []
    """
    ########### Scrape page with weapon models ###########
    """
    # Read html site
    soup = BeautifulSoup(urlopen("https://www.csgodatabase.com/weapons/").read(), features="html.parser")
    # Get div elements with the class attribute "weaponBox"
    div_elements = soup.find_all("div", attrs = {"class" : "weaponBox"})
    # For each div element in the list of div elements
    for div_element in div_elements:
        knife = False #Bool for control flow
        # Get the a element (link)
        a_element = div_element.find("a")
        # Get the href attribute from the a element and save the full link
        link = "https://www.csgodatabase.com/" + a_element.get("href")
        # Get the weapon model's name
        weapon_model = a_element.getText().replace(" ", "_")
        
        # Make dir in data folder with the weapon model's name
        filepath_model = os.path.join("..", "data", "weapon_model", weapon_model)
        os.makedirs(filepath_model, exist_ok = True)
        
        # I don't think that there are broken link on the page for weapon models
        # But just to be sure my script is reproducible, I make a try-except statement 
        try:
            # Read site  with skins for this weapon model
            soup = BeautifulSoup(urlopen(link).read(), features="html.parser")
        except HTTPError:
            print(f"[WARNING!] LINK ERROR, SITE NOT FOUND... SKIPPING {link}")
            continue
        # Get div elements from site
        skins_div = soup.find_all("div", attrs = {"class" : "skin-box-container"})

        # Knives have another class attribute, so this if-statements makes sure that I get knives as well
        # save the knife model name in list (used for creating pixplot dataset with knives)
        if len(skins_div) == 0:
            skins_div = soup.find_all("div", attrs = {"class" : "item-box"})
            knives.append(weapon_model)
            knife = True
        
        """
        ########### Scrape page with skins related to weapon model ###########
        """
        # Get for each element in list of divs on site with skins
        for skin_element in skins_div:
            # for each child of the div element
            for element in skin_element:
                #get img element
                img_element = skin_element.find("img")
                #Get the src attribute (the link to the image)
                img_link = img_element.get("src")
            
            # Some few skins cause an unicode error.
            # Rather than dealing with these few edgecase, I'm ignoring these skins.
            # This makes sure that the script won't break if csgo realeases another skin with a weird name in the future 
            try:
                # Get the name of the img
                img_name = re.findall(r"(?!.*/).*png", img_link)[0]
                print(img_name)
                # Path to folder with image models and the name of the skin
                image_path_model = os.path.join(filepath_model, img_name)
                # Save image from url
                urlretrieve(img_link, image_path_model) 
                image = cv2.imread(image_path_model)
                # Path to folder with all skins "all_weapons" (this folder is used for pixplot)
                image_path_all = os.path.join("..", "data", "all_weapons", img_name)
                # Save image in "all_weapons"
                cv2.imwrite(image_path_all, image)
                # Save image in "weapon_model"
                cv2.imwrite(image_path_model, image)
                # If it is a knive, save an image in the knives folder
                if knife:
                    image_path_knives = os.path.join("..", "data", "knives", img_name)
                    cv2.imwrite(image_path_knives, image)
                    
                """
                ########### Scrape metadata for skin ###########
                """
                # Get a elements
                skin_a_element = skin_element.find("a")
                # Get link (href attribute) to the skin's page
                skin_link = skin_a_element.get("href")
                
                # Most subpages for skins related to the "classic knife" apparently doesn't work
                # If this is the case I skip the site
                try:
                    # Read page
                    soup = BeautifulSoup(urlopen(skin_link).read(), features="html.parser")
                except HTTPError:
                    print(f"[WARNING!] LINK ERROR, SITE NOT FOUND... SKIPPING {link}")
                    continue
                # Get name of skin and rarity
                skin_name = soup.find_all("span", attrs = {"class" : "details-value"})[1].getText().replace(" ", "_")
                rarity = soup.find_all("span", attrs = {"class" : "details-value"})[2].getText().replace(" ", "_")
                
                # Get the date the skin was introduced
                # some skins dont have data on creation date, if this is the case set string to unknown
                # Used for description in metadata for pixplot
                try:
                    creation_date = soup.find_all("span", attrs = {"class" : "details-value"})[3].getText().replace(" ", "-")
                    creation_date = datetime.strptime(creation_date, "%d-%B-%Y") # Transform to datetime format
                    creation_date_str = creation_date.strftime("%d-%b-%Y")
                except ValueError:
                     creation_date_str = "unknown"
                
                # Get price data
                # Some skins don't have price data, in that case I set the value to nan
                try: 
                    # Get price listings for skins with low float (NOT THE DATATYPE BUT THE EMIC TERM) (factory new)
                    # I'm also converting the price listing to a float value (which certainly doesn't makes the terminology less confusing)
                    factory_new_price = float(soup.find_all("div", attrs = {"class" : "steam-pricing-buy"})[0].getText().replace("$", "").replace(",", ""))
                except IndexError:
                    factory_new_price = math.nan
                
                # Make dir in data folder corresponding to the rarity
                filepath = os.path.join("..", "data", "rarity", rarity)
                os.makedirs(filepath,  exist_ok = True)
                
                # Save image in the folder corresponding to its rarity
                image_path_rarity = os.path.join(filepath, img_name)
                cv2.imwrite(image_path_rarity, image)
                
                """
                ########### Create metadata ###########
                """
                # Create rows for metadata
                # Pixplot metadata
                row_pixplot = {"filename": img_name, "category": weapon_model, "permalink": skin_link,
                               "description": f"Introduced: {creation_date_str}, Price for factory new: {factory_new_price}$, Rarity: {rarity}, Weapon Model: {weapon_model}"} #description
                # general metadata
                metadata_row = {"filename": img_name, "rarity": rarity, "weapon_model": weapon_model,
                                "link": skin_link, "date": creation_date, "factory_new_pice": factory_new_price}
                # Add rows to df
                df_pixplot = df_pixplot.append(row_pixplot, ignore_index = True)
                df_metadata = df_metadata.append(metadata_row, ignore_index = True)
                
            # Pass on unicode error    
            except UnicodeEncodeError:
                continue
    
    # Create pixplot df for knives
    df_pixplot_knives = df_pixplot[df_pixplot["category"].isin(knives)]
    #Create metadata csv files
    df_pixplot_knives.to_csv(os.path.join("..", "data", "pixplot_metadata_knives.csv"), index=False)
    df_pixplot.to_csv(os.path.join("..", "data", "pixplot_metadata.csv"), index=False)
    df_metadata.to_csv(os.path.join("..", "data", "metadata.csv"), index=False)
    print("Done, the images can be found in the 'data' folder")
    
#Define behaviour when called from command line
if __name__ == "__main__":
    main()