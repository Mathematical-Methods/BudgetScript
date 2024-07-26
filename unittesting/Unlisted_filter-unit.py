import os
receipt_database = "../receipt_database"
unlisted_database = "../unlisted_database"
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

def category_function(file):
    receipt_name = file.lower().replace('.pdf','').replace('.jpg','').replace('.jpeg','').split(" ",3)
    if len(receipt_name) == 4:
        category = receipt_name[3].split('-',1)[0].split(' ',1)[0]
    return category

def unlisted_filter(file,receipt_category,dict):
    if receipt_category in dict:
        return receipt_category
    else:
        print(f"os.rename({receipt_database+'/'+file}, {unlisted_database+'/'+file})")
        #os.rename(receipt_database+'/'+file, unlisted_database+'/'+file)
        
for receipt in receipts:
    receipt_category = category_function(receipt)
    print(receipt_category)
    receipt_category = unlisted_filter(receipt,receipt_category,config)
    if receipt_category != None:
        print(receipt_category)




