from pytesseract import*
import argparse 
import cv2 
from PIL import Image 
import numpy as np
import math
  
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
  
# We load the input image and then convert 
# it to RGB from BGR. We then use Tesseract 
# to localize each area of text in the input 
# image 
images = cv2.imread(args["image"]) 
rgb = cv2.cvtColor(images, cv2.COLOR_BGR2RGB) 
results = pytesseract.image_to_data(rgb, output_type=Output.DICT)

textPoints=[]

# Then loop over each of the individual text 
# localizations
for i in range(0, len(results["text"])): 

    conf = int(results["conf"][i]) 

    # filter out weak confidence text localizations 
    if conf > args["min_conf"]:

        # We can then extract the bounding box coordinates 
        # of the text region from  the current result 
        x = results["left"][i] 
        y = results["top"][i] 
        w = results["width"][i] 
        h = results["height"][i]

        # We will also extract the OCR text itself along 
        # with the confidence of the text localization 
        text = results["text"][i]

        # We will display the confidence and text to 
        # our terminal for development
        print("Confidence: {}".format(conf)) 
        print("Text: {}".format(text)) 
        print("") 
        
        # We then plot little circles on the image to denote the
        # locations of the corners of each rectangle surrounding our text.
        cv2.circle(images, (x, y), 5, (0,0,255), -1) # Draw a circle
        textPoints.append([x, y]) # Append point coordinates to list of points.
    
        cv2.circle(images, (x + w, y), 5, (0,0,255), -1) # Draw a circle
        textPoints.append([x + w, y])
        
        cv2.circle(images, (x, y + h), 5, (0,0,255), -1) # Draw a circle
        textPoints.append([x, y + h])
    
        cv2.circle(images, (x + w, y + h), 5, (0,0,255), -1) # Draw a circle
        textPoints.append([x + w, y + h])

# Take the full list of point coordinates and convert to a numpy array.
textPoints = np.array(textPoints)

# Calculate the minimum area rectangle which can surround the points in textPoints
rectangle = cv2.minAreaRect(textPoints)

rectcenter_x=int(rectangle[0][0])
rectcenter_y=int(rectangle[0][1])
rect_w=int(rectangle[1][0]) + int(rectangle[1][0])*0.1
rect_h=int(rectangle[1][1]) + int(rectangle[1][1])*0.1

# Takes the coordinates of the center, the height and width and
# returns the coordinates of the corners of the box.
box = cv2.boxPoints([[rectcenter_x,rectcenter_y],[rect_w,rect_h],rectangle[2]])
box = np.int64(box)  # Convert to integer type

# Draws the outline of the rectangle given the
# four corners of the rectangle
cv2.drawContours(images, [box], -1, (0, 0, 255), 2)

## I assume that the rectangle when the angle = 0
#  is vertically oriented perfectly.
angle = int(rectangle[2])
print(angle)
if angle < 90 and angle > 45:
    angle = angle-90
else:
    angle = angle
print(angle)


# Rotate the Image
(h, w) = images.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(images, M, (w, h),
	flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

## To crop the image after rotation at the edge of the rectangle,
#  I must know the coordinates of the rectangle center.
#  To do this, I must assume that the center of the image is still the center 
#  after rotation. Which then means that the distance from the image center to rectangle center is constant. 
#  1. Calculate the angle between the Horizontal and the line
#     between the image center and the rectangle center before rotation.
x_diff1 = rectcenter_x-center[0]
y_diff1 = rectcenter_y-center[1]


dist_rectCtoC = math.sqrt(((x_diff1)**2)+((y_diff1)**2))
theta1 = math.atan(y_diff1/x_diff1)*180/math.pi
#  2. Use that angle to calculate the x and y coordinate offset
#     for rectangle center.
print(theta1)
print(angle)
theta2 = theta1-angle
print(theta2)
(h, w) = rotated.shape[:2]
rotatedcenter = (w // 2, h // 2)
rectcenter2_x = rotatedcenter[0] - math.cos(theta2)*dist_rectCtoC
rectcenter2_y = rotatedcenter[1] + math.sin(theta2)*dist_rectCtoC

#  3. Plot the newly calculated rectangle position for a sanity check.
box2 = cv2.boxPoints([[rectcenter2_x,rectcenter2_y],[rect_w,rect_h],0])
box2 = np.int64(box2)  # Convert to integer type
cv2.drawContours(rotated, [box2], -1, (255, 0,0), 10)

# Crop the image
#cropped = rotated[]



image = Image.fromarray(images).save("image.jpg")
rotated = Image.fromarray(rotated).save("rotated.jpg")