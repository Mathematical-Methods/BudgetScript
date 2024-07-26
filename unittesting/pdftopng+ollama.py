from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import ollama

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
pdf_file = "/home/unknown/Documents/00.Repositories/BudgetScript/pdftests/07-03-2024 $404.47 Dad Food-9218.pdf";
im = convert_from_path(pdf_file);

for page in im:
    receipt_text=pytesseract.image_to_string(page)
    print(receipt_text)
    
    


response = ollama.chat(model='wizard-vicuna-uncensored', messages=[
  {
    'role': 'user',
    'content': '''Review the following receipt text. Determine the category out of: "income", "return", 
                "payroll", "debt", "debts", "housing", "insurance",
                "investment", "savings", "saving", "medical", "misc",
                "personal", "transportation", "gas", "utilities",
                "food", "donation" receipt text:        ''' + receipt_text,
  },
])
print(response['message']['content'])