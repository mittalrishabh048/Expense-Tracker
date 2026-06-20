# Expense Tracker

ExpensesList=[]
print("Welcome to Expense Tracker:")
while True:
    print("====MENU====")
    print("1.Add Expense")
    print("2.View All Expenses")
    print("3.View Total Spending")
    print("4.Exit")

    choice=int(input("Please Enter Your Choice:"))

# ADD EXPENSE:
    if(choice==1):
        Date=input("Enter The Date On which you spent:")
        Category=input("What Type Of expense you've made(food,travel,shopping,etc.):")
        Description=input("Describe your spending(optional):")
        Amount=float(input("How much you've spent:Rs."))

        expense={
            "Date":Date,
            "Category":Category,
            "Description":Description,
            "Amount":Amount
        }
        ExpensesList.append(expense)
        print("\nExpense Added Successfully.\n")

# VIEW YOUR EXPENSES:
    elif(choice==2):
        if(len(ExpensesList)==0):
            print("No Expenses.")
        else:
            print("\n====YOUR EXPENSES====")
            count=1
            for EachExpense in ExpensesList:
                print(f"Expense Number {count}=>{EachExpense["Date"]},{EachExpense["Category"]},{EachExpense["Description"]},{EachExpense["Amount"]}\n")
                count+=1
    
# VIEW TOTAL SPENDINGS:
    elif(choice==3):
        if(len(ExpensesList)==0):
            print("Zero Spendings.")
        else:
            total=0
            for EachExpenses in ExpensesList:
                total=total+EachExpenses["Amount"]

            print("Total Spendings:",total)

# EXIT
    elif(choice==4):
        print("Thank You For Using Expense Tracker.")
        break
    else:
        print("Invalid Choice!! Try Again.")