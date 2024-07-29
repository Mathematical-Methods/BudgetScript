from pytesseract import*
import argparse 
import cv2 
from PIL import Image 
import numpy as np
import math
  
def deskew_crop(image,reqconf):
  
    # inputs: 
    # 1. image -> image file, can be a .png, .jpg, or a .ppm file. Anything readable by cv2.imread
    # 2. reqconf -> required minimum confidence needed to acknowledge the existence of a character or word. 
    # ############# Influences the rectangle that tells us how much the image needs rotation.

    # output: 
    # 1. Cropped image file in PIL image format.

    # We load the input image and then convert it to RGB from BGR. We then use Tesseract
    # to localize each area of text in the input image 
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
    results = pytesseract.image_to_data(rgb, output_type=Output.DICT)

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

############################################################################
# deskew ends


# 1. Calculate the angle between the Horizontal and the line
# between the image center and the rectangle center before rotation.
    # Find the difference between the receipt center and the image center.
    x_diff1 = center[0]-rectcenter_x
    y_diff1 = center[1]-rectcenter_y

    dist_rectCtoC = math.sqrt(((x_diff1)**2)+((y_diff1)**2))

    if x_diff1 == 0:
        theta1 = 90    
    else:
        theta1 = math.atan(y_diff1/x_diff1)*180/math.pi

# 2. Use that angle (theta1) to calculate the x and y coordinate offset
# for rectangle center.
    theta2 = theta1-angle

# 3. Calculate the post rotation rectangle position.
    # Find the height and width of the rotated image.
    (hR, wR) = rotated.shape[:2]

    # Calculate the center coords of the rotated image.
    Rcenter = (wR // 2, hR // 2)

    # Calculate and store the coordinates of the receipt after rotation.
    rectcenter2_x = int(Rcenter[0] - math.cos(theta2*(math.pi/180))*dist_rectCtoC)
    rectcenter2_y = int(Rcenter[1] - math.sin(theta2*(math.pi/180))*dist_rectCtoC)

# 4. Crop the image
    # Calculate and store the starting position and end position of the receipt edges.
    rect_start_x=int(rectcenter2_x-(rect_h/2))
    rect_end_x=int(rectcenter2_x+(rect_h/2))
    rect_start_y=int(rectcenter2_y-(rect_w/2))
    rect_end_y=int(rectcenter2_y+(rect_w/2))

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
    cropped = rotated[rect_start_y:rect_end_y,rect_start_x:rect_end_x]

    return cropped

if __name__ == "__main__":
    # We construct the argument parser 
    # and parse the arguments 
    ap = argparse.ArgumentParser() 
  
    ap.add_argument("-i", "--image", 
                required=True, 
                help="path to input image to be OCR'd") 
    ap.add_argument("-c", "--min-conf", 
                type=int, default=0, 
                help="minimum confidence value to filter weak text detection") 
    args = vars(ap.parse_args()) 
  
    receipt = deskew_crop(args["image"],args["min_conf"])
    Image.fromarray(receipt).save("cropped.jpg")