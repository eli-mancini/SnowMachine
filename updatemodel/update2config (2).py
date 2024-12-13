# -*- coding: utf-8 -*-
"""UPDATE2config.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LKmgXiYD1OwLg_Zca7ccpyX_5aB8cg56
"""

import torch
import os
import google
from google.colab import drive
drive.mount('/content/drive')
include_colab_link: True

### THESE PATHS ARE FOR THE DEMO NONTRAINED DATA; PLEASE UPDATE WITH OWN PATHS"
### All in snowpoles_data
ROOT_PATH = '/content/drive/MyDrive/starting100'
OUTPUT_PATH = '/content/drive/MyDrive/newmodel'  ## the folder where you want to store your custom model
metadata = './content/drive/MyDrive/starting100/pole_metadata.csv'
labels = './content/drive/MyDrive/starting100/labels.csv'

# learning parameters
BATCH_SIZE = 64
LR = 0.0001
EPOCHS = 20 #1000
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# train/test split
TEST_SPLIT = 0.2
# show dataset keypoint plot
SHOW_DATASET_PLOT = False
AUG = True

keypointColumns = ['x1', 'y1', 'x2', 'y2'] ## update

# Fine-tuning set-up
## make sure to download model from Zenodo
FINETUNE = True
FT_PATH = './models/CO_and_WA_model.pth'