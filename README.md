## Overview

This is the GitHub repository for a snow depth machine learning model originally developed by Catherine Breen and published in July 2024. The original model used time-lapse photography of snowpacks in the Western United States in a machine-learning model to predict the heights of the snowpacks in each photo. This estimation was based on the change in the height of a snowpole, also present in the photo.

The model in this repository is in the early stages of development, and seeks to expand on the original model by looking at 24-hour time-lapse photography in the Eastern United States. The original model only looked at images taken from the hours of 11 AM - 1 PM, so a 24-hour model is important in analyzing data in environments where there might be limited sunlight. 

DOI for Breen et al. 2024:  https://doi.org/10.1029/2023WR036682
Link to original GitHub repository:  https://github.com/catherine-m-breen/snowpoles


## Data Preprocess Code and Data Download

The study site for this model is the Sleeper's River Research Watershed in Danville, Vermont, USA. The time-lapse photography images were accessed through a Research File Share using the Microsoft Remote Desktop application. Photos have not been uploaded yet due to technical difficulties, but they will be soon. 

Images from Grand Mesa, Colorado and Okanogan, Washington were obtained through the original open access github repository published by Catherine Breen (https://github.com/catherine-m-breen/snowpoles/tree/main). While not all 9721 images are available, there is example data to look at.

Following the instructions from the original README document:

# Forked repository set up and installation
    !git clone https://github.com/eli-mancini/snowpoles
    %cd snowpoles
    !conda env update -f environment.yml
    !conda init
    !conda activate snowkeypoint
    !python src/demo.py

# Initial Photo labeling code
    python preprocess/rename_photos.py
    python src/labeling.py --datapath 'SleepersRiver' --pole_length '121.92' --subset_to_label '10'
