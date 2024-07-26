from PIL import Image
from pdf2image import convert_from_path
import pytesseract

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
pdf_file = "/home/unknown/Documents/00.Repositories/BudgetScript/pdftests/07-03-2024 $404.47 Dad Food-9218.pdf";
im = convert_from_path(pdf_file);

for page in im:
    receipt_text=pytesseract.image_to_string(page)
    print(receipt_text)
    

