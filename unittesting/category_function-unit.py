import os

receipts = os.listdir("./receipt_database")
print(receipts[0])
def category_function(file):
    receipt_name = file.lower().replace('.pdf','').replace('.jpg','').replace('.jpeg','').split(" ",3)
    if len(receipt_name) == 4:
        category = receipt_name[3].split('-',1)[0].split(' ',1)[0]
    return category

for receipt in receipts:
    receipt_category = category_function(receipt)
    print(receipt_category)