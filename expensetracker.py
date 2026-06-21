# Expense Tracker
import os
import json

FILE_NAME = "expenses.json"
ExpensesList=[]
print("=======================================================================")
print("                      Welcome to Expense Tracker                       ")
print("=======================================================================")

# --- STARTUP PERSISTENCE ENGINE ---
# Check if the data file exists on disk
if not os.path.exists(FILE_NAME):
    print(f"[Notice] No data file found. Creating a fresh storage workspace.")
    ExpensesList = []
else:
    # Try loading the existing data, protecting against file corruption
    try:
        with open(FILE_NAME, "r") as file:
            ExpensesList = json.load(file)
        print(f"[Success] Loaded {len(ExpensesList)} data records from storage.")
    except json.JSONDecodeError:
        print("\n===============================================================")
        print("[CRITICAL WARNING] 'expenses.json' is corrupted or unreadable!")
        print("To protect the session, the program will load an empty tracker.")
        print("===============================================================")
        ExpensesList = []

# --- MAIN APPLICATION LOOP ---
while True:
    print("====MENU====")
    print("1.Add Expense")
    print("2.View All Expenses")
    print("3.View Total Spending")
    print("4. View Expense Analytics  <-- [NEW]")
    print("5.Exit")
    print("===============")
    
    # Secure Choice Validation
    raw_choice = input("Please Enter Your Choice: ").strip()
    
    if not raw_choice.isdigit():
        print("\n[Error] Invalid Input! Please enter a number (1-4).")
        continue
        
    choice = int(raw_choice)

# ADD EXPENSE:
    if choice == 1:
        print("\n--- Add New Expense ---")
        Date = input("Enter The Date on which you spent (YYYY-MM-DD): ").strip()
        Category = input("What Type of expense you've made (food, travel, shopping, etc.): ").strip().lower()
        
        # Smart Default for Description
        Description = input("Describe your spending (optional): ").strip()
        if not Description:
            Description = "No Description"
            
        # Secure Amount Validation Loop
        while True:
            raw_amount = input("How much you've spent: Rs.").strip()
            try:
                Amount = float(raw_amount)
                if Amount <= 0:
                    print("[Error] Amount must be greater than zero. Please try again.")
                    continue
                break  # Valid amount received, break validation loop
            except ValueError:
                print("[Error] Invalid amount! Please enter a valid decimal number.")

        expense = {
            "Date": Date,
            "Category": Category,
            "Description": Description,
            "Amount": Amount
        }
        ExpensesList.append(expense)
        # --- AUTOMATIC AUTO-SAVE HOOK ---
        with open(FILE_NAME, "w") as file:
            json.dump(ExpensesList, file, indent=4)
            
        print("\n>> Expense Added & Saved Successfully to Disk! <<")

# VIEW YOUR EXPENSES (Tabular Grid System)
    elif choice == 2:
        if len(ExpensesList) == 0:
            print("\n[Notice] No Expenses recorded yet.")
        else:
            print("\n=======================================================================")
            print("                            YOUR EXPENSES                              ")
            print("=======================================================================")
            
            # Print Table Header
            header_str = f"{'No.':<5}│ {'Date':<12}│ {'Category':<15}│ {'Description':<25}│ {'Amount':>12}"
            print(header_str)
            print("─────┼─────────────┼────────────────┼──────────────────────────┼────────────")
            
            # Print Table Rows
            count = 1
            for EachExpense in ExpensesList:
                # Clip description string if it's too long to prevent text wrapping breaks
                desc = EachExpense['Description']
                if len(desc) > 23:
                    desc = desc[:20] + "..."
                    
                print(f"{count:<5}│ {EachExpense['Date']:<12}│ {EachExpense['Category']:<15}│ {desc:<25}│ Rs.{EachExpense['Amount']:>9.2f}")
                count += 1
                
            print("=======================================================================")
   

#  VIEW TOTAL SPENDINGS
    elif choice == 3:
        if len(ExpensesList) == 0:
            print("\n[Notice] Zero Spendings.")
        else:
            total = 0.0
            for EachExpenses in ExpensesList:
                total += EachExpenses["Amount"]
            print("\n========================================")
            print(f" Total Spendings: Rs.{total:.2f}")
            print("========================================")


# 4. VIEW EXPENSE ANALYTICS:
    elif choice == 4:
        # Edge-case check to prevent math crashes on empty data sets
        if len(ExpensesList) == 0:
            print("\n[Notice] No data available to calculate analytics. Try adding an expense first!")
            continue
            
        print("\n==================================================")
        print("                EXPENSE ANALYTICS                   ")
        print("====================================================")
        
        # --- PHASE 1: BASIC REDUCTIONS & EXTREMUMS ---
        total_spending = 0.0
        total_count = len(ExpensesList)
        
        # Initializing trackers with the very first item to begin relative scanning
        highest_expense = ExpensesList[0]
        lowest_expense = ExpensesList[0]
        
        # Temporary dictionary for category grouping logic
        category_totals = {}
        
        for item in ExpensesList:
            amount = item["Amount"]
            category = item["Category"]
            
            # Accumulate total spending
            total_spending += amount
            
            # Check for absolute maximum spend
            if amount > highest_expense["Amount"]:
                highest_expense = item
                
            # Check for absolute minimum spend
            if amount < lowest_expense["Amount"]:
                lowest_expense = item
                
            # --- PHASE 2: DYNAMIC ADVANCED GROUPING ---
            if category in category_totals:
                category_totals[category] += amount
            else:
                category_totals[category] = amount
                
        # Calculate derived average metric
        average_expense = total_spending / total_count
        
        # --- PHASE 3: PRESENTATION RENDER ---
        print(" Metrics Summary:")
        print(" ────────────────")
        print(f" • Total Spending        : Rs.{total_spending:.2f}")
        print(f" • Total No. of Expenses : {total_count} records")
        print(f" • Average Expense Cost  : Rs.{average_expense:.2f}")
        
        print("\n Extremes:")
        print(" ─────────")
        print(f" • Highest Single Spend  : Rs.{highest_expense['Amount']:.2f} ({highest_expense['Category']})")
        print(f" • Lowest Single Spend   : Rs.{lowest_expense['Amount']:.2f} ({lowest_expense['Category']})")
        
        print("\n Category-Wise Breakdown:")
        print(" ────────────────────────")
        for cat_name, cat_total in category_totals.items():
            print(f" ■ {cat_name:<21} : Rs.{cat_total:>9.2f}")
            
        print("==================================================")

#  EXIT
    elif choice == 5:
        print("\nThank You For Using Expense Tracker. Goodbye!")
        break
        
    else:
        print("\n[Error] Invalid Choice!! Please select an option between 1 and 4.")