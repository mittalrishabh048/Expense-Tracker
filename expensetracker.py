# Expense Tracker
import json
import os

class Expense:
    """Models a single individual expense entry."""
    def __init__(self, date: str, category: str, description: str, amount: float):
        self.date = date
        self.category = category.strip().lower()
        self.description = description if description else "No Description"
        self.amount = amount

    def to_dict(self) -> dict:
        """Converts object instance data back to dictionary format for JSON saving."""
        return {
            "Date": self.date,
            "Category": self.category,
            "Description": self.description,
            "Amount": self.amount
        }


class BudgetEngine:
    """Manages budget thresholds, limit updates, and progress layouts."""
    def __init__(self, budget_file: str = "budget.json"):
        self.budget_file = budget_file
        self.monthly_limit = 5000.0
        self.load_budget()

    def load_budget(self):
        if not os.path.exists(self.budget_file):
            self.save_budget()
        else:
            try:
                with open(self.budget_file, "r") as file:
                    config = json.load(file)
                    self.monthly_limit = config.get("monthly_budget", 5000.0)
            except json.JSONDecodeError:
                self.monthly_limit = 5000.0

    def save_budget(self):
        with open(self.budget_file, "w") as file:
            json.dump({"monthly_budget": self.monthly_limit}, file)

    def update_limit(self, new_limit: float):
        self.monthly_limit = new_limit
        self.save_budget()

    def display_dashboard(self, total_spent: float):
        remaining = self.monthly_limit - total_spent
        usage_pct = (total_spent / self.monthly_limit) * 100 if self.monthly_limit > 0 else 0
        bar_blocks = min(int(usage_pct // 10), 10)
        progress_bar = "█" * bar_blocks + "░" * (10 - bar_blocks)
        
        if total_spent >= self.monthly_limit:
            alert_status = "[⚠️ CRITICAL OVERSPEND] Lower your costs immediately!"
        elif total_spent >= (self.monthly_limit * 0.8):
            alert_status = "[⚠️ SYSTEM WARNING] You are nearing your allowance threshold."
        else:
            alert_status = "[✅ SAFE STATUS] Your spending patterns are stable."

        print("\n Current Configuration:")
        print(" ──────────────────────")
        print(f" • Monthly Budget Limit  : Rs.{self.monthly_limit:.2f}")
        print(f" • Total Amount Spent    : Rs.{total_spent:.2f}")
        print(f" • Remaining Allowance   : Rs.{remaining:.2f}")
        print("\n Usage Analysis:")
        print(" ───────────────")
        print(f" • Budget Usage Progress : [{progress_bar}] {usage_pct:.2f}%")
        print(f" • System Alert Status   : {alert_status}")


class ExpenseTrackerApp:
    """Core orchestration engine matching your original operational feature requirements."""
    def __init__(self, expense_file: str = "expenses.json"):
        self.expense_file = expense_file
        self.expenses_list = []
        self.budget_manager = BudgetEngine()
        self.load_expenses()

    def load_expenses(self):
        if os.path.exists(self.expense_file):
            try:
                with open(self.expense_file, "r") as file:
                    raw_data = json.load(file)
                    # Hydrate dictionaries out of flat list back into Expense Objects
                    self.expenses_list = [
                        Expense(item["Date"], item["Category"], item["Description"], item["Amount"])
                        for item in raw_data
                    ]
                print(f"[Success] Loaded {len(self.expenses_list)} data records from storage.")
            except (json.JSONDecodeError, KeyError):
                print("\n[CRITICAL WARNING] 'expenses.json' data is corrupted! Starting fresh.")
                self.expenses_list = []

    def save_expenses(self):
        with open(self.expense_file, "w") as file:
            # Flatten Expense objects into serializable standard dictionary maps
            serializable_list = [exp.to_dict() for exp in self.expenses_list]
            json.dump(serializable_list, file, indent=4)

    def get_total_spending(self) -> float:
        return sum(exp.amount for exp in self.expenses_list)

    def print_tabular_grid(self, target_list: list):
        print("\n=======================================================================")
        header_str = f"{'No.':<5}│ {'Date':<12}│ {'Category':<15}│ {'Description':<25}│ {'Amount':>12}"
        print(header_str)
        print("─────┼─────────────┼────────────────┼──────────────────────────┼────────────")
        count = 1
        for exp in target_list:
            desc = exp.description
            if len(desc) > 23: desc = desc[:20] + "..."
            print(f"{count:<5}│ {exp.date:<12}│ {exp.category:<15}│ {desc:<25}│ Rs.{exp.amount:>9.2f}")
            count += 1
        print("=======================================================================")

    def add_new_expense(self):
        print("\n--- Add New Expense ---")
        date = input("Enter The Date on which you spent (YYYY-MM-DD): ").strip()
        category = input("What Type of expense you've made: ").strip()
        description = input("Describe your spending (optional): ").strip()
        
        while True:
            raw_amount = input("How much you've spent: Rs.").strip()
            try:
                amount = float(raw_amount)
                if amount <= 0:
                    print("[Error] Amount must be greater than zero.")
                    continue
                break
            except ValueError:
                print("[Error] Invalid amount! Please enter a valid decimal number.")

        # Create our new instance entry object wrapper
        new_expense = Expense(date, category, description, amount)
        self.expenses_list.append(new_expense)
        self.save_expenses()
        print("\n>> Expense Added Successfully! <<")
        
        total = self.get_total_spending()
        if total >= self.budget_manager.monthly_limit:
            print(f"\n[⚠️ CRITICAL ALERT] You have OVERSPENT! Total: Rs.{total:.2f} / Limit: Rs.{self.budget_manager.monthly_limit:.2f}")
        elif total >= (self.budget_manager.monthly_limit * 0.8):
            print(f"\n[⚠️ BUDGET WARNING] Caution! You have used over 80% of your allowance. Spent: Rs.{total:.2f}")

    def run_search_engine(self):
        if not self.expenses_list:
            print("\n[Notice] Tracker is empty. Add entries first before filtering.")
            return
        print("\n==================================================")
        print("            ADVANCED SEARCH ENGINE                ")
        print("==================================================")
        print("1. Search By Specific Category\n2. Search By Description Keyword\n3. Search By Custom Amount Range")
        search_type = input("\nSelect a search query pattern (1-3): ").strip()
        matches = []

        if search_type == "1":
            target_cat = input("Enter target category: ").strip().lower()
            matches = [exp for exp in self.expenses_list if exp.category == target_cat]
        elif search_type == "2":
            keyword = input("Enter keyword phrase: ").strip().lower()
            matches = [exp for exp in self.expenses_list if keyword in exp.description.lower()]
        elif search_type == "3":
            try:
                min_amt = float(input("Enter minimum: Rs.").strip())
                max_amt = float(input("Enter maximum: Rs.").strip())
                if min_amt > max_amt: min_amt, max_amt = max_amt, min_amt
                matches = [exp for exp in self.expenses_list if min_amt <= exp.amount <= max_amt]
            except ValueError:
                print("[Error] Invalid entry! Inputs must be numeric values.")
                return
        else:
            print("[Error] Unknown query strategy selection.")
            return

        if not matches:
            print("\n[Notice] Zero search matches identified for that query.")
        else:
            self.print_tabular_grid(matches)

    def view_analytics_dashboard(self):
        if not self.expenses_list:
            print("\n[Notice] No data available to calculate analytics.")
            return
        print("\n==================================================")
        print("                EXPENSE ANALYTICS                 ")
        print("==================================================")
        total_spending = self.get_total_spending()
        total_count = len(self.expenses_list)
        highest = max(self.expenses_list, key=lambda x: x.amount)
        lowest = min(self.expenses_list, key=lambda x: x.amount)
        
        category_totals = {}
        for exp in self.expenses_list:
            category_totals[exp.category] = category_totals.get(exp.category, 0.0) + exp.amount

        print(f" • Total Spending        : Rs.{total_spending:.2f}")
        print(f" • Total No. of Expenses : {total_count} records")
        print(f" • Average Expense Cost  : Rs.{(total_spending / total_count):.2f}")
        print(f"\n Highest Single Spend  : Rs.{highest.amount:.2f} ({highest.category})")
        print(f" Lowest Single Spend   : Rs.{lowest.amount:.2f} ({lowest.category})")
        print("\n Category-Wise Breakdown:")
        for cat, amt in category_totals.items():
            print(f" ■ {cat:<21} : Rs.{amt:>9.2f}")
        print("==================================================")

    def handle_budget_menu(self):
        print("\n==================================================")
        print("                BUDGET MANAGEMENT                 ")
        print("==================================================")
        print("1. View Budget Status Dashboard\n2. Update Monthly Limit Target")
        sub = input("\nSelect an option (1-2): ").strip()
        if sub == "1":
            self.budget_manager.display_dashboard(self.get_total_spending())
        elif sub == "2":
            try:
                new_limit = float(input("Enter new limit: Rs.").strip())
                if new_limit <= 0: raise ValueError
                self.budget_manager.update_limit(new_limit)
                print(f">> Success! Budget updated to Rs.{new_limit:.2f} <<")
            except ValueError:
                print("[Error] Invalid configuration input value.")

    def generate_reports(self):
        if not self.expenses_list:
            print("\n[Notice] No data logs found.")
            return
        print("\n1. Generate Daily Report\n2. Generate Monthly Report")
        report_type = input("\nSelect report type (1-2): ").strip()
        filtered, label, title = [], "", ""

        if report_type == "1":
            label = input("Enter date (YYYY-MM-DD): ").strip()
            title = "DAILY EXPENSE REPORT"
            filtered = [exp for exp in self.expenses_list if exp.date == label]
        elif report_type == "2":
            label = input("Enter month (YYYY-MM): ").strip()
            title = "MONTHLY EXPENSE REPORT"
            filtered = [exp for exp in self.expenses_list if exp.date[:7] == label]
        else:
            return

        if not filtered:
            print(f"\n[Notice] Zero entries found matching: {label}")
            return

        report_output = [
            "==================================================",
            f"              {title}               ",
            "==================================================",
            f" Target Window        : {label}",
            f" Total Items Matched  : {len(filtered)} records",
            "──────────────────────────────────────────────────"
        ]
        period_total = 0.0
        cat_breakdown = {}
        for exp in filtered:
            period_total += exp.amount
            cat_breakdown[exp.category] = cat_breakdown.get(exp.category, 0.0) + exp.amount
            report_output.append(f" • [{exp.date}] {exp.category:<10} : Rs.{exp.amount:>8.2f}")
            
        report_output.append("──────────────────────────────────────────────────")
        for cat, amt in cat_breakdown.items():
            report_output.append(f"   ■ {cat:<15} : Rs.{amt:>8.2f}")
        report_output.append("──────────────────────────────────────────────────")
        report_output.append(f" TOTAL PERIOD SPEND   : Rs.{period_total:.2f}")
        report_output.append("==================================================\n")
        
        final_text = "\n".join(report_output)
        print(final_text)
        
        if input("Export report to a text file? (y/n): ").strip().lower() == "y":
            filename = f"report_{label.replace('-', '_')}.txt"
            with open(filename, "w", encoding="utf-8") as file:
                file.write(final_text)
            print(f"[Export Success] Saved as '{filename}'!")

    def start_main_loop(self):
        while True:
            print("\n==== MENU ====")
            print("1. Add Expense\n2. View All Expenses\n3. View Total Spending\n4. Advanced Search & Filter")
            print("5. View Expense Analytics\n6. Budget Management\n7. Reporting System\n8. Exit")
            print("===============")
            raw_choice = input("Please Enter Your Choice: ").strip()
            if not raw_choice.isdigit():
                print("\n[Error] Invalid choice! Input a number (1-8).")
                continue
            choice = int(raw_choice)
            
            if choice == 1: self.add_new_expense()
            elif choice == 2: 
                if not self.expenses_list: print("\n[Notice] No records yet.")
                else: self.print_tabular_grid(self.expenses_list)
            elif choice == 3: print(f"\n========================================\n Total Spendings: Rs.{self.get_total_spending():.2f}\n========================================")
            elif choice == 4: self.run_search_engine()
            elif choice == 5: self.view_analytics_dashboard()
            elif choice == 6: self.handle_budget_menu()
            elif choice == 7: self.generate_reports()
            elif choice == 8:
                print("\nThank You For Using Expense Tracker. Goodbye!")
                break
            else:
                print("\n[Error] Unknown menu navigation option selection.")

# --- APPLICATION ENTRY POINT EXECUTION ---
if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.start_main_loop()