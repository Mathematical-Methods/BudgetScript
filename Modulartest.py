import os

# get the working directory
workingdir = os.getcwd();
# file name retrieval: os.listdir returns a list of files within the spec'd directory
receipts = os.listdir('/home/unknown/Downloads/05. May/');
#receipts = os.listdir(workingdir);

# Create a dictionary of all variables names
# "" is a placeholder for the names of the receipts. It is (believed) to be equiv. to Income = []. 
# 0 is a placeholder for the initial amount of the receipts. It is to be equiv. to Income = [].
config = {"Income"  : [["Income"],[0]],
          "Return"  : [["Income"],[0]],
          "Payroll" : [["Income"],[0]],
          "Bill"    : [["Bill"],[0]]};

#totalSpent = 0;
#totalEarned = 0;

for receipt in receipts:
    receipt = receipt.lower().replace('.pdf','');
    fields = receipt.split(" ",3);
    if len(fields) == 4:
        Category = config.get(fields[3].split('-',1)[0])
        if type(Category).__name__ != 'NoneType':
            Category[0].append(receipt);
            Category[1][0] = Category[1][0] + float(fields[1].strip("+$"));
## Total spent.
            #if Category[0][0] != 'Income':
            #    totalSpent = totalSpent + Category[1][0];
            #else 
            #    totalEarned = totalEarned + Category[1][0];
