import cv2
import numpy as np
from pathlib import Path

script_path = Path(__file__).resolve()
chessboard_path = script_path.parent / 'Chessboards'

# Iterate through all images in the folder
image_list = list(chessboard_path.glob('*'))
print(f'Found {len(image_list)} images in {chessboard_path}')

# Read the first image from the list
image_path = image_list[0]
image = cv2.imread(str(image_path))

if image is not None:
    cv2.imshow("Orig Image", image)
    cv2.waitKey(0)
else:
    print("Could not read image")