#Legolization
The project is making your picture as if it was constructed from lego using lego colors only. 
On a small UI you can choose between different settings. 
It is a local application, hence your pictures are not uploaded and shared with anybody.
The program is entirely based on pillow package that can be directly installed without any configuration.
Credit for lego color codes is listed in the config.py. Those are collected by Ryan Howerter and can be reached here:
https://swooshable.com/parts/colors

## Getting started
These instructions will get you a copy of the project up and running on your local machine.

### Installing
First clone the repository to your local machine or download it manually from git.
The requirements.txt contains all the neccessary packages, please make sure you install them. In order to do this, use your existing virtual env or create a new one, navigate to the root folder of the project and execute:
```
pip install -r requirements.txt
```
Only for modules are used namly:
* pillow
* pysimplegui
* numpy
* matplotlib (used only for analysing the picture, not used in the main program)

## Running the program
After copying the repository you can start the program by running the following module from the root directory:
```
python app.py
```
or you can run from your IDE through the same entry point, app.py.

## Features
### Before after sample 
Photo by Saifuddin Ratlamwala from Pexels
<p align="center">
  <img src="/assets/sample_pic_readme.jpg" width="350" title="sample before">
  <img src="/assets/sample_pic_readme_legolized.png" width="350" title="sample after">
</p>

### Select colors
* You can select colors on the right hand side that are used for creating your lego-like image.
* The colors are grouped into 3 categories with the checkboxes you can manage the different groups. 
* Each group has a different tab.

### General settings
* Use the file browser to select a file to be legolized. Only .png and .jpg files can be used.
* You can set the number of bricks along the longer side of the image. Aspect ration of the image is not changed.
* You can select different brick types to legolize your picture: 1x1 plate, 1x1 flat tile, 1x1 stud and 1x1 flat stud
* In case of studs you can set the color of the base plate to grey, white, black and green
* If you like to save the legolized image, please set the name in the input box
* If you like to save the legolized image, please select the folder where it will be saved
* Saved files are always .png files

## Built With
* [pysimplegui](https://pysimplegui.readthedocs.io/en/latest/) - Lightweight python GUI builder.
* [pillow](https://pillow.readthedocs.io/en/stable/) - Very popular python image library.

