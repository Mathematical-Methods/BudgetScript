import os # os is a library for interacting with the file system.

workingdir = os.getcwd(); # get the working directory

# file name retrieval: os.listdir returns a list of files within the spec'd directory
receipts = os.listdir(workingdir);

# Create a dictionary of all variables names
# "" is a placeholder for the names of the receipts. It is (believed) to be equiv. to Income = []. 
# 0 is a placeholder for the initial amount of the receipts. It is to be equiv. to Income = [].
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

totalEarned = 0;
totalspent = 0;

for receipt in receipts:
    # print("Lowercasing receipt name, removing the '.pdf' characters.");
    receipt = receipt.lower().replace('.pdf',''); # Lowercasing receipt name, removing the '.pdf' characters.

    # print("Splitting receipt name into a list of 4 words(3 splits).");
    fields = receipt.split(" ",3); # Splitting receipt name into a list of 4 words(3 splits).
    
    # print("Filtering the files by whether they have 4 words in the name list.");
    if len(fields) == 4: # Filtering the files by whether they have 4 words in the name list.

        # print("Checking the dictionary for", fields[3].split('-',1)[0]);
        Category = config.get(fields[3].split('-',1)[0]); # Checking the dictionary for the Category.
        # print(Category);

        # print("Filtering the incoming receipt category by datatype.");
        if type(Category).__name__ != 'NoneType': # Filtering the incoming receipt category by datatype.

            # print("Appending the receipt name to the end of the list defined by the variable Category[0].");
            Category[0].append(receipt); # Appending the receipt name to the end of the list defined by the variable Category[0].
            # print(Category);
            # print(Category[0]);

            # print("Adding the receipt total to the Category total defined by the variable Category[1][0].");
            Category[1][0] = Category[1][0] + float(fields[1].strip("+$")); # Adding the receipt total to the Category total defined by the variable Category[1][0].
            # print(Category[1][0]);
            
            if fields[1].strip(".$1234567890abcdefghijklmnopqrstuvwxyz[]") == "+":
                totalEarned = totalEarned + float(fields[1].strip("+$"));
            else:
                totalspent = totalspent + float(fields[1].strip("+$"));  

# print("Opening report.txt.");
with open("report.txt", "w") as f: # Opening report.txt.
    
#     print("Iterating over the dictionary's key entries.");
    for category in [*config]: # Iterating over the dictionary's key entries.

#         print("Check if the dictionary category has any amount spent / earned.");
#         print(category);
#         print(config.get(category)[1][0]); # Check if the dictionary category has any amount spent / earned.
        
        if config.get(category)[1][0] > 0:
#            print("Writing in report.txt.");

#            print("Writing all of the receipt names in order.");
            print(config.get(category)[0][0], file=f);
            iteration = 0;
            for receipt in config.get(category)[0]:
                if iteration > 0:
                    print("     ", receipt, file=f);
                iteration = iteration + 1;                
            print("  ",config.get(category)[0][0],"total: $",config.get(category)[1][0], file=f);
    print("Total earned:",totalEarned ,file=f);
    print("Total spent:",totalspent ,file=f);