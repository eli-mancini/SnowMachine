# -*- coding: utf-8 -*-
"""editlabeling.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1p-ijSD90cKD8y48WcAk0s-1R8DwCO158
"""

# -*- coding: utf-8 -*-
"""EDITlabeling.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/eli-mancini/SnowMachine/blob/main/updatemodel/EDITlabeling.ipynb
"""

'''
written by Catherine M. Breen
cbreen@uw.edu
edited by Eli D. Mancini
mpmancin@syr.edu

Use of our keypoint detection model currently requires ~10 images per camera. We provide a labeling script below that when pointed
at a camera directory (i.e., data > cam1 or data > cam2, etc), walks the user through labeling every 10th image and saves as labels.csv in a specified direrctory.

We estimate it will take about 5 imgs/min or about 300 imgs per hour.

x1,y1 = top
x2,y2 = bottom

The labels.csv file can then be directly pointed at train.py for fine-tuning. The user can then run predict.py to extract the snow depth.

example run

python src/labeling.py --datapath 'nontrained_data' --pole_length '168' --subset_to_label '2'

'''

import cv2
!pip install -q google.colab
import google.colab
import matplotlib.pyplot as plt
import glob
import argparse
import tqdm
import math
import pandas as pd
import os
import datetime
import IPython
import numpy as np
import sys
from google.colab import drive
drive.mount('/content/drive')
include_colab_link = True

# Argument parser for command-line arguments:
parser = argparse.ArgumentParser(description='Labeling script for snow depth estimation.')
parser.add_argument('--datapath', type=str, help='Path to the directory containing images.')
parser.add_argument('--pole_length', type=int, default='168', help='Length of the pole in cm.')
parser.add_argument('--subset_to_label', type=int, default=5, help='Subset of images to label (e.g., every 2nd image).')
parser.add_argument('-lengths_file', type=str, default=None, help='path to csv file with lengths')
parser.set_defaults(datapath='/content/drive/MyDrive/starting100', pole_length='168', subset_to_label='2', lengths_file='/content/drive/MyDrive/updatelengths.csv')
args = parser.parse_args([])

def main():
  print("Entering main function")
  coords_df = pd.read_csv('/content/drive/MyDrive/pixelcoordinates.csv')
  ## labeling data
  data = []
  filename = []
  PixelLengths = []
  x1, x2, y1, y2 = [],[],[],[]
  creationTimes = []

  ## customized data
  pole_length = np.float64(args.pole_length)
  subset_to_label = np.int16(args.subset_to_label)

  ## some metadata data
  dir_list = glob.glob(f'{args.datapath}/*')
  dir_list.sort()
  pole_lengths = []
  first_pole_pixel_length = []
  conversions = []
  heights = []
  widths = []
  pole_lengths_px = []
  pixel_cm_conversions = []
  print("Main function starting ok")
  ### loop to label every nth photo!
  lengths_df = None
  if args.lengths_file:
      lengths_df = pd.read_csv(args.lengths_file)
  first_valid_entry = lengths_df[lengths_df['lengths'] > 0].iloc[0]
  first_base_filename = first_valid_entry['filename']
  first_actual_length = first_valid_entry['lengths']
  first_image_processed = False
  first_image_height = None
  i = 0
  for j, (file, base_filename) in tqdm.tqdm(enumerate(zip(dir_list, [os.path.basename(f) for f in dir_list]))):
      base_filename = os.path.basename(file)
      filename.append(base_filename)
      creationTimes.append(datetime.datetime.fromtimestamp(os.path.getctime(file)).strftime('%Y-%m-%d %H:%M:%S'))

      PixelLength = np.nan
      x1_val= np.nan
      y1_val= np.nan
      x2_val= np.nan
      y2_val= np.nan

      x1.append(x1_val)
      y1.append(y1_val)
      x2.append(x2_val)
      y2.append(y2_val)
      PixelLengths.append(PixelLength)

      if i % subset_to_label == 0:
        img = cv2.imread(file)
        if img is not None:
          width, height, channel = img.shape
          first_image_processed = True
          if first_image_height is None:
            first_image_height = height
          if lengths_df is not None:
            length_row = lengths_df[lengths_df['filename']== base_filename]
          else:
            length_row= pd.read_csv('/content/drive/MyDrive/updatelengths.csv')

          if not length_row.empty:
            actual_Length = length_row['lengths'].values[0]
            conversion = np.nan
            if actual_Length != 0:
              PixelLength = (actual_Length / pole_length) * height
              conversion = pole_length / PixelLength
              if not first_pole_pixel_length:
                first_pole_pixel_length.append(PixelLength)
                conversions.append(conversion)
                pole_lengths.append(pole_length)
                first_image_processed = True

            print(f"Filename: {base_filename}, Actual Length: {actual_Length}, Pixel Length: {PixelLength}")
            pole_lengths.append(pole_length)
            first_pole_pixel_length.append(PixelLength)
            conversions.append(conversion)
            heights.append(height)
            widths.append(width)
            PixelLengths[-1]=PixelLength

        coords_row= coords_df[coords_df['filename']==base_filename]
        if not coords_row.empty:
                  x1[-1] = (coords_row['bottomX'].values[0])
                  y1[-1] = (coords_row['bottomY'].values[0])
                  x2[-1] = (coords_row['topX'].values[0])
                  y2[-1] = (coords_row['topY'].values[0])
      i += 1


      plt.close()

  print("no loop issue")

  print(f'lengths_df is empty: {lengths_df is None or lengths_df.empty}')
  print(f'base_filename: {base_filename}')
  print(f'PixelLengths[0]: {PixelLengths[0]}')
  print(f'first_image_processed:{first_image_processed}')
  if not first_image_processed and PixelLengths:
    PixelLength = PixelLengths[0]
    conversion = pole_length / PixelLength
    first_pole_pixel_length.append(PixelLength)
    conversions.append(conversion)
    pole_lengths.append(pole_length)

  df = pd.DataFrame({'filename': filename, 'datetime':creationTimes, 'x1':x1, 'y1':y1, 'x2':x2, 'y2':y2, 'PixelLengths':PixelLengths})
  ## simplified table for snow depth conversion later on
  list_lengths = [len(pole_lengths), len(first_pole_pixel_length), len(conversions), len(heights), len(widths)]
  max_len = max(list_lengths)
  pole_lengths.extend([np.nan] * (max_len - len(pole_lengths)))
  first_pole_pixel_length.extend([np.nan] * (max_len - len(first_pole_pixel_length)))
  conversions.extend([np.nan] * (max_len - len(conversions)))
  widths.extend([np.nan] * (max_len - len(widths)))
  heights.extend([np.nan] * (max_len - len(heights)))
  metadata = pd.DataFrame({'pole_length_cm':pole_lengths,
                           'pole_length_px':first_pole_pixel_length,
                          'pixel_cm_conversion':conversions,'width':widths,'height':heights})
  print("After creating DataFrame")
  df.to_csv(f'{args.datapath}/labels.csv', index=False)
  print("After saving to CSV")
  metadata.to_csv(f'{args.datapath}/pole_metadata.csv', index=False)

if __name__ == '__main__':
        main()

if os.path.exists(f'{args.datapath}/labels.csv'):
    print("labels.csv was created successfully!")
else:
    print("labels.csv was not created.")

df=pd.read_csv(f'{args.datapath}/labels.csv')
df['filename']=df['filename'].apply(lambda x: os.path.basename(x))
df.to_csv(f'{args.datapath}/labels.csv', index=False)

