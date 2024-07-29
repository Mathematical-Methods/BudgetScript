import os
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
import cv2
import numpy as np
import crop
import deskew
import csv


tesseract_config = "--oem 3 --dpi 300 --psm 3 -c load_system_dawg=false load_freq_dawg=false -l eng+osd"
receipt_database = "/home/unknown/Documents/00.Repositories/BudgetScript/receipt_database/"
unlisted_database = "/home/unknown/Documents/00.Repositories/BudgetScript/unlisted_database/"
receipts = os.listdir(receipt_database)
config = {"income"              : [["Income"],[0]],
          "return"              : [["Income"],[0]],
          "payroll"             : [["Income"],[0]],
          "debt"                : [["Debt"],[0]],
          "debts"               : [["Debt"],[0]],
          "housing"             : [["Housing"],[0]],
          "insurance"           : [["Insurance"],[0]],
          "investment"          : [["Investment"],[0]],
          "savings"             : [["Investment"],[0]],
          "saving"              : [["Investment"],[0]],
          "medical"             : [["Medical"],[0]],
          "misc"                : [["Miscellaneous"],[0]],
          "personal"            : [["Personal"],[0]],
          "transportation"      : [["Transportation"],[0]],
          "gas"                 : [["Transportation"],[0]],
          "utilities"           : [["Utilities"],[0]],
          "food"                : [["Food"],[0]],
          "donation"            : [["Donation"],[0]],
          };

def preprocess(image):
# GreyScale Method
    image = image.convert('L')
# Turn image into array
    image = np.asarray(image)
# Deskew and Crop image
    image = deskew.deskew(image)
    image = crop.crop(image)
# Resizing the image method
    up_size=(2*image.shape[1],2*image.shape[0])
    image = cv2.resize(image,up_size,interpolation= cv2.INTER_LINEAR)
# Using cv2.erode() & dilate method to remove noise
    # Creating Kernel
    kernele = np.ones((3, 3), np.uint8)
    image = cv2.erode(image, kernele)
    image = cv2.dilate(image, kernele)
# Turn array back into PIL Image    
    image = Image.fromarray(image, 'L')
    return image


def category_function(file):
    receipt_name = file.lower().replace('.pdf','').replace('.jpg','').replace('.jpeg','').split(" ",3)
    if len(receipt_name) == 4:
        category = receipt_name[3].split('-',1)[0].split(' ',1)[0]
    return category

def unlisted_filter(file,receipt_category,dict):
    if receipt_category in dict:
        return receipt_category
    else:
        print(f"os.rename({receipt_database+file}, {unlisted_database+file})")
        #os.rename(receipt_database+'/'+file, unlisted_database+'/'+file)

# define OCR function-> input: individual file name; output: text in the file.
def OCR(file,inc):
    ind = ""
    if ".pdf" in file:
        receipt_pages = convert_from_path(receipt_database+file);
        ind = ".pdf"
        receipt_text_pages = ''
        inc_2=0
        for page in receipt_pages:
            page = preprocess(page)
            receipt_text_page=pytesseract.image_to_string(page, config=tesseract_config)
            receipt_text_pages+=receipt_text_page
            page.save('./tesseractoutput/output_image'+str(inc)+str(inc_2)+'.jpg')
            inc_2+=1
        #print(receipt_text_pages)
        return receipt_text_pages
    else:
        image = receipt_database+'/'+file
        image = preprocess(image)
        receipt_text = ''
        receipt_text = pytesseract.image_to_string(image, config=tesseract_config)
        #print(receipt_text)
        image.save('./tesseractoutput/output_image'+str(inc)+'.jpg')
        return receipt_text 

def append_to_csv(file_path, new_data):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(new_data) 
        

if os.path.isfile("./train.csv"):
    os.remove("./train.csv")

i=0
for receipt in receipts:
    receipt_category = category_function(receipt)
    print("The category is: ", receipt_category)
    receipt_category = unlisted_filter(receipt,receipt_category,config)
    if receipt_category != None:
        print("For redundancy, the category is: ", receipt_category)
        receipt_text = OCR(receipt,i).replace("\n"," ")
        append_to_csv("./train.csv",[receipt_category,receipt_text])

    i+=1
    if i == 10: 
        break
