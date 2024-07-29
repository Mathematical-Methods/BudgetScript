from pytesseract import*
import argparse 
import cv2 
from PIL import Image 
import numpy as np
import math
  
def deskew_(image,reqconf):
    # inputs: 
    # 1. image -> image file, can be a .png, .jpg, or a .ppm file. Anything readable by cv2.imread
    # 2. reqconf -> required minimum confidence needed to acknowledge the existence of a character or word. 
    # ############# Influences the rectangle that tells us how much the image needs rotation.

    # output: 
    # 1. Cropped image file in PIL image format.

    # We load the input image and then convert it to RGB from BGR. We then use Tesseract
    # to localize each area of text in the input image.    
    #rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
    results = pytesseract.image_to_data(image, output_type=Output.DICT)

    # We create a list object that will contain the coodinates of the corners of the rectangles
    # surrounding each word.
    textPoints=[]

    # Then loop over each of the individual text 
    # localizations
    for i in range(0, len(results["text"])): 

        conf = int(results["conf"][i]) # Get the confidence value for ith recognized word.
        
        if conf > reqconf: # filter out weak confidence text localizations 

            # We can then extract the bounding box coordinates 
            # of the text region from the current result 
            x = results["left"][i] 
            y = results["top"][i] 
            w = results["width"][i] 
            h = results["height"][i] 
        
            textPoints.append([x, y]) # Append point coordinates to list of points.
            textPoints.append([x + w, y])
            textPoints.append([x, y + h])
            textPoints.append([x + w, y + h])

    # Take the full list of point coordinates and convert to a numpy array.
    textPoints = np.array(textPoints)

    # Calculate the minimum area rectangle which can surround the points in textPoints.
    rectangle = cv2.minAreaRect(textPoints)

    # Store the coordinates of the center of the previously calculated minimum "rectangle."
    rectcenter_x=int(rectangle[0][0])
    rectcenter_y=int(rectangle[0][1])

    # Store the values of the height and width of the calculated "rectangle."
    rect_h=int(rectangle[1][0]) + int(rectangle[1][0])*0.1
    rect_w=int(rectangle[1][1]) + int(rectangle[1][1])*0.1

    ## I assume that the rectangle when the angle = 0
    ## is vertically oriented perfectly.

    angle = int(rectangle[2]) # Store the orientation value from the minimum area rectangle.

    # This conditional checks and corrects the orientation value returned by minAreaRect.
    if angle <= 90 and angle > 45: # If vertical rectangle surrounding receipt is oriented like this slash: /
    
        angle = angle-90 # Take the angle and subtract 90 degrees. 

        # When the receipt is oriented like this slash: /
        # the cv2.minAreaRect() function will swap the rectangle height and width.
        # This action corrects this.
        rect_h = int(rectangle[1][1]) + int(rectangle[1][1])*0.1
        rect_w = int(rectangle[1][0]) + int(rectangle[1][0])*0.1

    else: # If vertical rectangle surrounding receipt is oriented like this slash: \
        angle = angle

    # Rotate the Image
    (h, w) = image.shape[:2] # Get the height and width of the input image.
    center = (w // 2, h // 2) # Find the center coordinates of the input image. 
    M = cv2.getRotationMatrix2D(center, angle, 1.0) # Return the 2D rotation matrix.

    # Take the input image and rotate it.
    rotated = cv2.warpAffine(image, M, (w, h),
    	flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    rectcenter=[rectcenter_x,rectcenter_y]
    recthw=[rect_h,rect_w]

    return [rotated, rectcenter, recthw]


def deskew(image):
    #image = cv2.imread(image)
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pytesseract.image_to_osd(image, output_type=Output.DICT)
    if results["orientation"] == 0:
        return image
    else:
        conf=0
        while True:
            image_info = deskew_(image,conf)[0]
            results = pytesseract.image_to_osd(image_info[0], output_type=Output.DICT)
            if results["orientation"] == 0:
                return image_info
                break
            else:
                conf += 25