import os
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
import cv2
import numpy as np

options= '--psm 6'

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


def erosion_dilation(image):
    image = np.asarray(image)
    # Creating kernel
    kernelhoriz = np.array([[0,0,0,0,0],
                            [0,0,0,0,0],
                            [1,1,1,1,1],
                            [0,0,0,0,0],
                            [0,0,0,0,0]], np.uint8) 
    kernelvert = np.array([[0,0,1,0,0],
                           [0,0,1,0,0],
                           [0,0,1,0,0],
                           [0,0,1,0,0],
                           [0,0,1,0,0]], np.uint8) 
    kernele = np.ones((3, 3), np.uint8)
    # Using cv2.erode() method
    image = cv2.erode(image, kernelhoriz)
    image = cv2.erode(image,kernelvert)
    image = cv2.dilate(image, kernele)
    image = Image.fromarray(image, 'RGB')
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
        #print(f"os.rename({receipt_database+file}, {unlisted_database+file})")
        os.rename(receipt_database+'/'+file, unlisted_database+'/'+file)

# define OCR function-> input: individual file name; output: text in the file.
def OCR(file):
    file.lower()
    if ".pdf" in file:
        receipt_pages = convert_from_path(receipt_database+file);
        receipt_text_pages = ""
        for page in receipt_pages:
            page = erosion_dilation(page)
            receipt_text_page=pytesseract.image_to_string(page, config=options).replace('\n', ' ')
            receipt_text_pages+=receipt_text_page
        page.save('output_image.jpg')
        return receipt_text_pages
    else:
        image = receipt_database+'/'+file
        image = erosion_dilation(image)
        receipt_text=pytesseract.image_to_string(image, config=options).replace('\n', ' ')
        image.save('output_image.jpg')
        return receipt_text 
    #### Currently here. Writing the filter that will handle .pdf files.
    #### the pytesseract will be called after this filter is set up.   

i=0
i_csv=0
csv_file = open("train.csv","r+")
csv_file.write(", receipt text, receipt category\n")

for receipt in receipts:
    receipt_category = category_function(receipt)
    receipt_category = unlisted_filter(receipt,receipt_category,config)
    
    if type(receipt_category).__name__ != 'NoneType':
        print("Handling "+receipt)
        text = OCR(receipt)
        csv_file.write(str(i_csv)+','+receipt_category+','+text+'\n')
        i_csv+=1