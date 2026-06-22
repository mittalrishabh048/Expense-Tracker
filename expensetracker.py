# Expense Tracker
import os
import json

EXPENSES_FILE = "expenses.json"
BUDGET_FILE = "budget.json"

ExpensesList=[]
monthly_budget = 0.0

print("=======================================================================")
print("                      Welcome to Expense Tracker                       ")
print("=======================================================================")

# --- STARTUP PERSISTENCE ENGINE ---
# Check if the data file exists on disk
if not os.path.exists(EXPENSES_FILE):
    print(f"[Notice] No data file found. Creating a fresh storage workspace.")
    ExpensesList = []
else:
    # Try loading the existing data, protecting against file corruption
    try:
        with open(EXPENSES_FILE, "r") as file:
            ExpensesList = json.load(file)
        print(f"[Success] Loaded {len(ExpensesList)} data records from storage.")
    except json.JSONDecodeError:
        print("\n===============================================================")
        print("[CRITICAL WARNING] 'expenses.json' is corrupted or unreadable!")
        print("To protect the session, the program will load an empty tracker.")
        print("===============================================================")
        ExpensesList = []

# Load Budget Configuration (Companion Storage)
if not os.path.exists(BUDGET_FILE):
    # Set a default starting budget of Rs. 5000.00 if no file exists yet
    monthly_budget = 5000.0
    with open(BUDGET_FILE, "w") as file:
        json.dump({"monthly_budget": monthly_budget}, file)
else:
    try:
        with open(BUDGET_FILE, "r") as file:
            config = json.load(file)
            monthly_budget = config.get("monthly_budget", 5000.0)
    except json.JSONDecodeError:
        monthly_budget = 5000.0

# --- MAIN APPLICATION LOOP ---
while True:
    print("====MENU====")
    print("1.Add Expense")
    print("2.View All Expenses")
    print("3.View Total Spending")
    print("4.View Expense Analytics")
    print("5.Budget Management")
    print("6.Reporting System        <-- [NEW]")
    print("7.Exit")
    print("===============")
    
    # Secure Choice Validation
    raw_choice = input("Please Enter Your Choice: ").strip()
    
    if not raw_choice.isdigit():
        print("\n[Error] Invalid Input! Please enter a number (1-7).")
        continue
        
    choice = int(raw_choice)

# ADD EXPENSE (With Proactive Budget Warnings)
    if choice == 1:
        print("\n--- Add New Expense ---")
        Date = input("Enter The Date on which you spent (YYYY-MM-DD): ").strip()
        Category = input("What Type of expense you've made: ").strip().lower()
        
        Description = input("Describe your spending (optional): ").strip()
        if not Description:
            Description = "No Description"
            
        while True:
            raw_amount = input("How much you've spent: Rs.").strip()
            try:
                Amount = float(raw_amount)
                if Amount <= 0:
                    print("[Error] Amount must be greater than zero. Please try again.")
                    continue
                break
            except ValueError:
                print("[Error] Invalid amount! Please enter a valid decimal number.")

        expense = {
            "Date": Date,
            "Category": Category,
            "Description": Description,
            "Amount": Amount
        }
        ExpensesList.append(expense)
        
        # Save updated data list
        with open(EXPENSES_FILE, "w") as file:
            json.dump(ExpensesList, file, indent=4)
            
        print("\n>> Expense Added Successfully! <<")
        
        # Proactive Alert Evaluation Immediately Upon Entry Creation
        total_spent = sum(item["Amount"] for item in ExpensesList)
        if total_spent >= monthly_budget:
            print(f"\n[⚠️ CRITICAL ALERT] You have officially OVERSPENT! Total: Rs.{total_spent:.2f} / Limit: Rs.{monthly_budget:.2f}")
        elif total_spent >= (monthly_budget * 0.8):
            print(f"\n[⚠️ BUDGET WARNING] Caution! You have used over 80% of your allowance. Spent: Rs.{total_spent:.2f}")


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
        total = sum(item["Amount"] for item in ExpensesList)
        print(f"\n========================================\n Total Spendings: Rs.{total:.2f}\n========================================")

#  VIEW EXPENSE ANALYTICS:
    elif choice == 4:
        # Edge-case check to prevent math crashes on empty data sets
        if len(ExpensesList) == 0:
            print("\n[Notice] No data available to calculate analytics. Try adding an expense first!")
            continue
            
        print("\n==================================================")
        print("                EXPENSE ANALYTICS                   ")
        print("====================================================")
        total_spending = sum(item["Amount"] for item in ExpensesList)
        total_count = len(ExpensesList)
        highest_expense = max(ExpensesList, key=lambda x: x["Amount"])
        lowest_expense = min(ExpensesList, key=lambda x: x["Amount"])
        
        category_totals = {}
        
        for item in ExpensesList:
            category_totals[item["Category"]] = category_totals.get(item["Category"], 0.0) + item["Amount"]
        
        
        # --- PRESENTATION RENDER ---
        print(" Metrics Summary:")
        print(" ────────────────")
        print(f" • Total Spending        : Rs.{total_spending:.2f}")
        print(f" • Total No. of Expenses : {total_count} records")
        print(f" • Average Expense Cost  : Rs.{(total_spending / total_count):.2f}")
        
        print("\n Extremes:")
        print(" ─────────")
        print(f" • Highest Single Spend  : Rs.{highest_expense['Amount']:.2f} ({highest_expense['Category']})")
        print(f" • Lowest Single Spend   : Rs.{lowest_expense['Amount']:.2f} ({lowest_expense['Category']})")
        
        print("\n Category-Wise Breakdown:")
        print(" ────────────────────────")
        for cat_name, cat_total in category_totals.items():
            print(f" ■ {cat_name:<21} : Rs.{cat_total:>9.2f}")
            
        print("==================================================")

# BUDGET MANAGEMENT WORKSPACE
    elif choice == 5:
        print("\n==================================================")
        print("                BUDGET MANAGEMENT                 ")
        print("==================================================")
        print(f" 1. View Budget Status Dashboard")
        print(f" 2. Update Monthly Limit Target")
        sub_choice = input("\nSelect a budget operation sub-choice (1-2): ").strip()
        
        # Sub-Option 1: View Progress Bar and Threshold Status
        if sub_choice == "1":
            total_spent = sum(item["Amount"] for item in ExpensesList)
            remaining_allowance = monthly_budget - total_spent
            
            # Calculate metrics safely
            usage_pct = (total_spent / monthly_budget) * 100 if monthly_budget > 0 else 0
            
            # Dynamic text progress bar logic (scaled down to 10 block increments)
            bar_blocks = min(int(usage_pct // 10), 10)
            progress_bar = "█" * bar_blocks + "░" * (10 - bar_blocks)
            
            # Determine alert flags
            if total_spent >= monthly_budget:
                alert_status = "[⚠️ CRITICAL OVERSPEND] Lower your costs immediately!"
            elif total_spent >= (monthly_budget * 0.8):
                alert_status = "[⚠️ SYSTEM WARNING] You are nearing your allowance threshold."
            else:
                alert_status = "[✅ SAFE STATUS] Your spending patterns are stable."
                
            print("\n Current Configuration:")
            print(" ──────────────────────")
            print(f" • Monthly Budget Limit  : Rs.{monthly_budget:.2f}")
            print(f" • Total Amount Spent    : Rs.{total_spent:.2f}")
            print(f" • Remaining Allowance   : Rs.{remaining_allowance:.2f}")
            print("\n Usage Analysis:")
            print(" ───────────────")
            print(f" • Budget Usage Progress : [{progress_bar}] {usage_pct:.2f}%")
            print(f" • System Alert Status   : {alert_status}")
            print("==================================================")
            
        # Sub-Option 2: Dynamically re-configure limits
        elif sub_choice == "2":
            while True:
                raw_new_budget = input(f"Current limit is Rs.{monthly_budget:.2f}. Enter new limit: Rs.").strip()
                try:
                    new_budget = float(raw_new_budget)
                    if new_budget <= 0:
                        print("[Error] Target limit must be greater than zero.")
                        continue
                    monthly_budget = new_budget
                    
                    # Update local state file record
                    with open(BUDGET_FILE, "w") as file:
                        json.dump({"monthly_budget": monthly_budget}, file)
                        
                    print(f"\n>> Success! Monthly budget updated to Rs.{monthly_budget:.2f} <<")
                    break
                except ValueError:
                    print("[Error] Please enter a valid decimal number.")
        else:
            print("[Error] Invalid option selected. Returning to menu.")

# REPORTING SYSTEM WORKSPACE (Filter & File Export Layout)
    elif choice == 6:
        if len(ExpensesList) == 0:
            print("\n[Notice] No data logs found. Add an expense first to build a report.")
            continue
            
        print("\n==================================================")
        print("                 REPORTING SYSTEM                 ")
        print("==================================================")
        print("1. Generate Daily Report")
        print("2. Generate Monthly Report")
        report_type = input("\nSelect report filter type (1-2): ").strip()
        
        filtered_expenses = []
        target_label = ""
        report_title = ""
        
        # Choice 6.1: Daily Extraction Slicer
        if report_type == "1":
            target_label = input("Enter target date to filter (YYYY-MM-DD): ").strip()
            report_title = "DAILY EXPENSE REPORT"
            for item in ExpensesList:
                if item["Date"] == target_label:
                    filtered_expenses.append(item)
                    
        # Choice 6.2: Monthly Extraction Slicer (Grabs first 7 chars: "YYYY-MM")
        elif report_type == "2":
            target_label = input("Enter target month to filter (YYYY-MM): ").strip()
            report_title = "MONTHLY EXPENSE REPORT"
            for item in ExpensesList:
                if item["Date"][:7] == target_label:
                    filtered_expenses.append(item)
        else:
            print("[Error] Invalid option. Returning to core menu loop.")
            continue

        # Process filtered results
        if len(filtered_expenses) == 0:
            print(f"\n[Notice] No database matches found for target window: {target_label}")
            continue
            
        # Compile Report Text Layout using a text lines buffer string
        report_output = []
        report_output.append("==================================================")
        report_output.append(f"              {report_title}               ")
        report_output.append("==================================================")
        report_output.append(f" Target Window        : {target_label}")
        report_output.append(f" Total Items Matched  : {len(filtered_expenses)} records")
        report_output.append("──────────────────────────────────────────────────")
        
        period_total = 0.0
        cat_breakdown = {}
        
        # Aggregate the period metrics
        for item in filtered_expenses:
            period_total += item["Amount"]
            cat_breakdown[item["Category"]] = cat_breakdown.get(item["Category"], 0.0) + item["Amount"]
            report_output.append(f" • [{item['Date']}] {item['Category']:<10} | {item['Description']:<15} : Rs.{item['Amount']:>8.2f}")
            
        report_output.append("──────────────────────────────────────────────────")
        report_output.append(" Category Summary Breakdown:")
        for cat, total_amt in cat_breakdown.items():
            report_output.append(f"   ■ {cat:<15} : Rs.{total_amt:>8.2f}")
        report_output.append("──────────────────────────────────────────────────")
        report_output.append(f" TOTAL PERIOD SPEND   : Rs.{period_total:.2f}")
        report_output.append("==================================================\n")
        
        # Render Compiled Text Report straight to the screen terminal layout
        final_report_text = "\n".join(report_output)
        print(final_report_text)
        
        # --- THE EXPORT HOOK ---
        export_choice = input("Would you like to export this report to a text file? (y/n): ").strip().lower()
        if export_choice == "y":
            # Sanitize a safe clean filename string based on user filter parameters
            safe_filename = f"report_{target_label.replace('-', '_')}.txt"
            try:
                with open(safe_filename, "w", encoding="utf-8") as file:
                    file.write(final_report_text)
                print(f"\n[Export Success] Report successfully written onto disk as '{safe_filename}'!")
            except IOError:
                print("\n[Error] System disk block error! Unable to write external file.")

#  EXIT
    elif choice == 7:
        print("\nThank You For Using Expense Tracker. Goodbye!")
        break
        
    else:
        print("\n[Error] Invalid Choice!! Please select an option between 1 and 4.")