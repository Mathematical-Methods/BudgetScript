# Python program to explain cv2.erode() method 

# importing cv2 
import cv2 
from PIL import Image
# importing numpy 
import numpy as np 
from matplotlib import pyplot as plt
# path 
path = "/home/unknown/Documents/00.Repositories/BudgetScript/receipt_database/1-2-2022 $3.04 Target Miscellaneous.jpg"

# Reading an image in default mode 
image = cv2.imread(path) 

# Window name in which image is displayed 
window_name = 'Image'
def erosion_dilation(image):
    image = np.asarray(image)
    # Creating kernel 
    kerneld = np.ones((3, 3), np.uint8) 
    kernele = np.ones((4, 4), np.uint8)
    # Using cv2.erode() method 
    image = cv2.erode(image, kernele) 
    image = cv2.dilate(image, kerneld)
    image = cv2.erode(image, kernele)
    image = Image.fromarray(image, 'RGB')
    return image


image.save('output_image.jpg')