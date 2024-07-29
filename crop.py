from pytesseract import*
import argparse 
import cv2 
from PIL import Image 
import numpy as np
import math

def crop_(image, reqconf):

    if len(image) == 3:
        image = image[0]
        rectcenter = image[1]
        recthw = image[2]
    else:
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
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
        rectcenter=[rectcenter_x,rectcenter_y]
        # Store the values of the height and width of the calculated "rectangle."
        rect_h=int(rectangle[1][0]) + int(rectangle[1][0])*0.1
        rect_w=int(rectangle[1][1]) + int(rectangle[1][1])*0.1
        recthw=[rect_h,rect_w]

# 3. Calculate the post rotation rectangle position.
    # Find the height and width of the rotated image.
    (hR, wR) = image.shape[:2]

# 4. Crop the image
    # Calculate and store the starting position and end position of the receipt edges.
    rect_start_x=int(rectcenter[0]-(recthw[0]/2))
    rect_end_x=int(rectcenter[0]+(recthw[0]/2))
    rect_start_y=int(rectcenter[1]-(recthw[1]/2))
    rect_end_y=int(rectcenter[1]+(recthw[1]/2))

    # Correct the starting and ending positions if they end up outside of the image.
    if rect_start_x <= 0:
        rect_start_x = 0
    if rect_start_y <= 0:
        rect_start_y = 0
    if rect_end_x >= wR:
        rect_end_x = wR-1
    if rect_end_y >= hR:
        rect_end_y = hR-1

    # Crop the rotated image by stripping array entries not defined in the below ranges.
    cropped = image[rect_start_y:rect_end_y,rect_start_x:rect_end_x]

    return cropped

def crop(image):

    if len(image) == 3:
        uncropped_image = image[0]
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        uncropped_image = image
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    conf = 0
    image_cropped = crop_(uncropped_image,conf)
    #Image.fromarray(image_cropped).save("image.jpg")
    results = pytesseract.image_to_osd(image_cropped, output_type=Output.DICT)
    print("Results:",results["orientation"])
    print("To correct -> Rotate:",results["rotate"])

    if results["orientation"] == 0:#or results["orientation"] == 180:
        return image_cropped
    else:
        i=0
        while True:
            conf += 10
            if conf > 90: conf = 90
            image = crop_(uncropped_image,conf)
            results = pytesseract.image_to_osd(image, output_type=Output.DICT)
            print("Results"+str(i)+":",results["orientation"])
            print("To correct -> Rotate:",results["rotate"])
            #Image.fromarray(image).save("image.jpg")
            (h, w) = uncropped_image.shape[:2]
            (h2, w2) = image.shape[:2]
            if results["orientation"] == 0:
                return image
                break
            if (math.isclose(h2,h,rel_tol=h2*0.01) or math.isclose(w2,w,rel_tol=w2*0.01)):
                return image
                break
            i+=1