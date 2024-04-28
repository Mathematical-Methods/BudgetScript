import os

# get the working directory
workingdir = os.getcwd();
# file name retrieval: os.listdir returns a list of files within the speced directory
receipts = os.listdir(workingdir);

# Gain/Expense Category Arrays
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

#  Income/Cost Variables
Income_amount = 0;
Bill_amount = 0;
Debt_amount = 0;
Housing_amount = 0;
Insurance_amount = 0;
Investment_amount = 0;
Medical_amount = 0;
MISC_amount = 0;
Personal_amount = 0;
Saving_amount = 0;
Transportation_amount = 0;
Utilities_amount = 0;
Food_amount = 0;

for receipt in receipts:
    receipt = receipt.replace('.pdf','')
    fields = receipt.split(" ",3)
    if len(fields) == 4:
        if fields[3].split('-',1)[0] == "Income" or fields[3].split('-',1)[0] == "Return" or fields[3].split('-',1)[0] == "Payroll":
            Income.append(receipt);
            Income_amount = Income_amount + float(fields[1].strip("+$"));
        if fields[3].split('-',1)[0] == "Bill":
            Bills.append(receipt);
            Bill_amount = Bill_amount + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Debt":
            Debts.append(receipt);
            Debt_amount = Debt_amount + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Housing":
            Housing.append(receipt);
            Housing_amount = Housing_amount + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Insurance":
            Insurance.append(receipt);
            Insurance_amount = Insurance_amount + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Investment":
            Investment.append(receipt);
            Investment_amount = Investment_amount + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Medical" or fields[3].split('-',1)[0] == "MEDICAL":
            Medical.append(receipt);
            Medical_amount = Medical_amount + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "MISC":
            MISC.append(receipt);
            MISC_amount = MISC_amount + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Personal":
            Personal.append(receipt);
            Personal_amount = Personal_amount + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Saving":
            Saving.append(receipt);
            Saving_amount = Saving_amount + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Transportation":
            Transportation.append(receipt);
            Transportation_amount = Transportation_amount + float(fields[1].strip("$"));
        if fields[3].split('-',1)[0] == "Utilities":
            Utilities.append(receipt);
            Utilities_amount = Utilities_amount + float(fields[1].strip("$"));
        if fields[3] == "Food" or fields[3] == "Groceries":
            Food.append(receipt);
            Food_amount = Food_amount + float(fields[1].strip("$"));

Total = Bill_amount + Debt_amount + Housing_amount + Insurance_amount + Investment_amount + Medical_amount + MISC_amount + Personal_amount + Saving_amount + Transportation_amount + Utilities_amount + Food_amount;

with open("report.txt", "w") as f:
    if Income_amount > 0:
        print("Income", file=f)
        for reciept in Income:
            print("     ", reciept, file=f);
        print("    Income:",Income_amount, file=f);
    if Bill_amount > 0:
        print("Bills", file=f)
        for reciept in Bills:
            print("     ", reciept, file=f);
        print("    Bills Cost:",Bill_amount, file=f)
    if Debt_amount > 0:
        print("Debts", file=f)
        for reciept in Debts:
            print("     ", reciept, file=f);
        print("    Debts Cost:",Debt_amount, file=f);
    if Housing_amount > 0:
        print("Housing", file=f)
        for reciept in Housing:
            print("     ", reciept, file=f);
        print("    Housing Cost:",Housing_amount, file=f);
    if Insurance_amount > 0:
        print("Insurance", file=f)
        for reciept in Insurance:
            print("     ", reciept, file=f);
        print("    Insurance Cost:",Insurance_amount, file=f);
    if Investment_amount > 0:
        print("Investment", file=f)
        for reciept in Investment:
            print("     ", reciept, file=f);
        print("    Investment Cost:",Investment_amount, file=f);
    if Medical_amount > 0:
        print("Medical", file=f)
        for reciept in Medical:
            print("     ", reciept, file=f);
        print("    Medical Cost:",Medical_amount, file=f);
    if MISC_amount > 0:
        print("MISC", file=f)
        for reciept in MISC:
            print("     ", reciept, file=f);
        print("    MISC Cost:",MISC_amount, file=f);
    if Personal_amount > 0:
        print("Personal", file=f)
        for reciept in Personal:
            print("     ", reciept, file=f);
        print("    Personal Cost:",Personal_amount, file=f);
    if Saving_amount > 0:
        print("Saving", file=f)
        for reciept in Saving:
            print("     ", reciept, file=f);
        print("    Saving Cost:",Saving_amount, file=f);
    if Transportation_amount > 0:
        print("Transportation", file=f)
        for reciept in Transportation:
            print("     ", reciept, file=f);
        print("    Transportation Cost:",Transportation_amount, file=f);
    if Utilities_amount > 0:
        print("Utilities", file=f)
        for reciept in Utilities:
            print("     ", reciept, file=f);
        print("    Utilities Cost:",Utilities_amount, file=f);
    if Food_amount > 0:
        print("Food", file=f)
        for reciept in Food:
            print("     ", reciept, file=f);
        print("    Food Cost:",Food_amount, file=f);

    print('You earned $',Income_amount,'this month.', file=f);
    print('You spent $',Total,'this month.', file=f);
