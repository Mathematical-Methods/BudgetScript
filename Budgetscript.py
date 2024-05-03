import os

# get the working directory
workingdir = os.getcwd();
# file name retrieval: os.listdir returns a list of files within the spec'd directory
receipts = os.listdir(workingdir);

# Gain/Expense Category Arrays
# These arrays will contain the stripped file names of each receipt that belongs in it according to expense type.
Income = [];
Bills = [];
Debts = [];
Housing = [];
Insurance = [];
Investment = [];
Medical = [];
MISC = [];
Personal = [];
Saving = [];
Transportation = [];
Utilities = [];
Food = [];
Donation = [];

#  Income/Cost Variables
Income_amount = [0]; # Income will only be tracked into a single account (the checking account) for now. A better script would account for earnings growth of an investment account.
Bill_amount = [0,0,0,0]; # Each element in the vector is meant to track an individual spending account.
Debt_amount = [0,0,0,0];
Housing_amount = [0,0,0,0];
Insurance_amount = [0,0,0,0];
Investment_amount = [0,0,0,0];
Medical_amount = [0,0,0,0];
MISC_amount = [0,0,0,0];
Personal_amount = [0,0,0,0];
Saving_amount = [0,0,0,0];
Transportation_amount = [0,0,0,0];
Utilities_amount = [0,0,0,0];
Food_amount = [0,0,0,0];
Donation_amount = [0,0,0,0];

# This vector contains the last four numbers of each card currently held.
last4cardNo = [9218,1781,4972,3772]

for receipt in receipts:
    receipt = receipt.replace('.pdf','')
    receipt = receipt.replace('.PDF','')
    fields = receipt.split(" ",3)
    if len(fields) == 4:
        if fields[3].split('-',1)[0] == "Income" or fields[3].split('-',1)[0] == "Return" or fields[3].split('-',1)[0] == "Payroll":
            Income.append(receipt);
            Income_amount[0] = Income_amount[0] + float(fields[1].strip("+$"));
        if fields[3].split('-',1)[0] == "Bill":
            Bills.append(receipt);
            Bill_amount[0] = Bill_amount[0] + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Debt":
            Debts.append(receipt);
            Debt_amount[0] = Debt_amount[0] + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Housing":
            Housing.append(receipt);
            Housing_amount[0] = Housing_amount[0] + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Insurance":
            Insurance.append(receipt);
            Insurance_amount[0] = Insurance_amount[0] + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Investment":
            Investment.append(receipt);
            Investment_amount[0] = Investment_amount[0] + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Medical" or fields[3].split('-',1)[0] == "MEDICAL":
            Medical.append(receipt);
            Medical_amount[0] = Medical_amount[0] + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "MISC":
            MISC.append(receipt);
            MISC_amount[0] = MISC_amount[0] + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Personal":
            Personal.append(receipt);
            Personal_amount[0] = Personal_amount[0] + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Saving":
            Saving.append(receipt);
            Saving_amount[0] = Saving_amount[0] + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Transportation":
            Transportation.append(receipt);
            Transportation_amount[0] = Transportation_amount[0] + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Utilities":
            Utilities.append(receipt);
            Utilities_amount[0] = Utilities_amount[0] + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Food" or fields[3].split('-',1)[0] == "Groceries":
            Food.append(receipt);
            Food_amount[0] = Food_amount[0] + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Donation":
            Donation.append(receipt);
            Donation_amount[0] = Donation_amount[0] + float(fields[1].strip("$"));

Total = Bill_amount[0] + Debt_amount[0] + Housing_amount[0] + Insurance_amount[0] + Investment_amount[0] + Medical_amount[0] + MISC_amount[0] + Personal_amount[0] + Saving_amount[0] + Transportation_amount[0] + Utilities_amount[0] + Food_amount[0] + Donation_amount[0];

with open("report.txt", "w") as f:
    if Income_amount[0] > 0:
        print("Income", file=f)
        for receipt in Income:
            print("     ", receipt, file=f);
        print("    Income:",Income_amount[0], file=f);
    if Bill_amount[0] > 0:
        print("Bills", file=f)
        for receipt in Bills:
            print("     ", receipt, file=f);
        print("    Bills Cost:",Bill_amount[0], file=f)
    if Debt_amount[0] > 0:
        print("Debts", file=f)
        for receipt in Debts:
            print("     ", receipt, file=f);
        print("    Debts Cost:",Debt_amount[0], file=f);
    if Housing_amount[0] > 0:
        print("Housing", file=f)
        for receipt in Housing:
            print("     ", receipt, file=f);
        print("    Housing Cost:",Housing_amount[0], file=f);
    if Insurance_amount[0] > 0:
        print("Insurance", file=f)
        for receipt in Insurance:
            print("     ", receipt, file=f);
        print("    Insurance Cost:",Insurance_amount[0], file=f);
    if Investment_amount[0] > 0:
        print("Investment", file=f)
        for receipt in Investment:
            print("     ", receipt, file=f);
        print("    Investment Cost:",Investment_amount[0], file=f);
    if Medical_amount[0] > 0:
        print("Medical", file=f)
        for receipt in Medical:
            print("     ", receipt, file=f);
        print("    Medical Cost:",Medical_amount[0], file=f);
    if MISC_amount[0] > 0:
        print("MISC", file=f)
        for receipt in MISC:
            print("     ", receipt, file=f);
        print("    MISC Cost:",MISC_amount[0], file=f);
    if Personal_amount[0] > 0:
        print("Personal", file=f)
        for receipt in Personal:
            print("     ", receipt, file=f);
        print("    Personal Cost:",Personal_amount[0], file=f);
    if Saving_amount[0] > 0:
        print("Saving", file=f)
        for receipt in Saving:
            print("     ", receipt, file=f);
        print("    Saving Cost:",Saving_amount[0], file=f);
    if Transportation_amount[0] > 0:
        print("Transportation", file=f)
        for receipt in Transportation:
            print("     ", receipt, file=f);
        print("    Transportation Cost:",Transportation_amount[0], file=f);
    if Utilities_amount[0] > 0:
        print("Utilities", file=f)
        for receipt in Utilities:
            print("     ", receipt, file=f);
        print("    Utilities Cost:",Utilities_amount[0], file=f);
    if Food_amount[0] > 0:
        print("Food", file=f)
        for receipt in Food:
            print("     ", receipt, file=f);
        print("    Food Cost:",Food_amount[0], file=f);
    if Donation_amount[0] > 0:
        print("Donations", file=f)
        for receipt in Donation:
            print("     ", receipt, file=f);
        print("    Food Cost:",Donation_amount[0], file=f);

    print('You earned $',Income_amount[0],'this month.', file=f);
    print('You spent $',Total,'this month.', file=f);
