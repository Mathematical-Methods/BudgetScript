import os

# get the working directory
workingdir = os.getcwd();
# file name retrieval: os.listdir returns a list of files within the spec'd directory
receipts = os.listdir(workingdir);

# Create a list of all variable names
Income = [[""],[0]]; 
# "" is a placeholder for the names of the receipts. It is (believed) to be equiv. to Income = []. 
Bills = [[""],[0]];
# 0 is a placeholder for the initial amount of the receipts. It is to be equiv. to Income = [].
Debts = [[""],[0]];
Housing = [[""],[0]];

variable_list = [Income,Bills,Debts,Housing];

for receipt in receipts:
    receipt = receipt.replace('.pdf','')
    receipt = receipt.replace('.PDF','')
    fields = receipt.split(" ",3)
    if len(fields) == 4:
            if fields[3].split('-',1)[0] == "Income" or fields[3].split('-',1)[0] == "Return" or fields[3].split('-',1)[0] == "Payroll":
                variable[0][0].append(receipt);
                variable[1][0] = variable[1][0] + float(fields[1].strip("+$"));
