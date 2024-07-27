
from pytesseract import*
import argparse 
import cv2 
from PIL import Image 
import numpy as np
  
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
#print (results) 
#print("*********************************")
#osdresults = pytesseract.image_to_osd(rgb) 
#print (osdresults)
# Then loop over each of the individual text 
# localizations 

textPoints=[]

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
        # our terminal 
        print("Confidence: {}".format(conf)) 
        print("Text: {}".format(text)) 
        print("") 
          
        # We then strip out non-ASCII text so we can 
        # draw the text on the image We will be using 
        # OpenCV, then draw a bounding box around the 
        # text along with the text itself 
        text = "".join(text).strip() 
        
        '''
        cv2.rectangle(images, 
                      (x, y), 
                      (x + w, y + h), 
                      (0, 0, 255), 2) 
        '''
        cv2.circle(images, (x, y), 5, (0,0,255), -1) # Draw a circle
        textPoints.append([x, y])
        
        cv2.circle(images, (x + w, y), 5, (0,0,255), -1) # Draw a circle
        textPoints.append([x + w, y])
        
        
        cv2.circle(images, (x, y + h), 5, (0,0,255), -1) # Draw a circle
        textPoints.append([x, y + h])
        

        cv2.circle(images, (x + w, y + h), 5, (0,0,255), -1) # Draw a circle
        textPoints.append([x + w, y + h])
        

        '''
        cv2.putText(images, 
                    text, 
                    (x, y - 10),  
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1.2, (0, 255, 255), 3)
        ''' 

textPoints = np.array(textPoints)
rectangle = cv2.minAreaRect(textPoints)
box = cv2.boxPoints(rectangle)
box = np.int64(box)  # Convert to integer type
print(rectangle)
print(box)
cv2.drawContours(images, [box], -1, (0, 0, 255), 2)
##########################################################
#Currently here



# After all, we will show the output image 
image = Image.fromarray(images).save("image.jpg")

