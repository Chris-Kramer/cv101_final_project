#!/usr/bin/env bash

VENVNAME=final_proj_venv
echo "Creating environment"
python -m venv $VENVNAME

# This makes sure that the bash script can be run from bash emulator on windows 
# Test if the folder bin in venvname exists
if [ -d "$VENVNAME/bin" ]

    then
        source $VENVNAME/bin/activate
        echo "Building venv for Linux/Mac ..."
    
    else
        source $VENVNAME/Scripts/activate
        echo "Building venv for Windows ..."
fi

echo "Upgrading pip and installing dependencies"
#Upgrade pip
# I'm specifying that I'm using pip from python, since my pc have problems upgrading pip locally if I don't do it.
python -m pip install --upgrade pip

# Test if requirements exist and install it
test -f requirements.txt && python -m pip install -r requirements.txt

# Move to source folder
cd src

echo "running script"
# Run python script
python webscrape.py $@

echo "deactivating and removing environment"
# Deavtivate environment
deactivate

# Move to home directory
cd ..

# Remove virtual environment (I'm just doing this to test if this is possible)
rm -rf $VENVNAME

#Print this to the screen 
echo "Done! The results can be found in the folder 'output'"