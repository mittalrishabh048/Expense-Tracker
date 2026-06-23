# Expense Tracker
import json
import os

EXPENSE_FILE = "expenses.json"
BUDGET_FILE = "budget.json"
RECURRING_FILE = "recurring_templates.json"

class Expense:
    """Models a single individual expense entry."""
    def __init__(self, date: str, category: str, description: str, amount: float):
        self.date = date
        self.category = category.strip().lower()
        self.description = description if description else "No Description"
        self.amount = amount

    def to_dict(self) -> dict:
        return {
            "Date": self.date,
            "Category": self.category,
            "Description": self.description,
            "Amount": self.amount
        }


class RecurringTemplate:
    """Models a template configuration schedule for recurring costs."""
    def __init__(self, category: str, description: str, amount: float, frequency: str, last_generated_date: str):
        self.category = category.strip().lower()
        self.description = description
        self.amount = amount
        self.frequency = frequency.strip().lower()  # "weekly" or "monthly"
        self.last_generated_date = last_generated_date

    def to_dict(self) -> dict:
        return {
            "Category": self.category,
            "Description": self.description,
            "Amount": self.amount,
            "Frequency": self.frequency,
            "Last_Generated_Date": self.last_generated_date
        }


class BudgetEngine:
    """Manages budget thresholds, limit updates, and progress layouts."""
    def __init__(self, budget_file: str = BUDGET_FILE):
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
    """Core orchestration engine containing active recurring generation passes."""
    def __init__(self):
        self.expense_file = EXPENSE_FILE
        self.recurring_file = RECURRING_FILE
        self.expenses_list = []
        self.templates_list = []
        self.budget_manager = BudgetEngine()
        
        self.load_expenses()
        self.load_recurring_templates()

    def load_expenses(self):
        if os.path.exists(self.expense_file):
            try:
                with open(self.expense_file, "r") as file:
                    raw_data = json.load(file)
                    self.expenses_list = [
                        Expense(item["Date"], item["Category"], item["Description"], item["Amount"])
                        for item in raw_data
                    ]
                print(f"[Success] Loaded {len(self.expenses_list)} data records from storage.")
            except (json.JSONDecodeError, KeyError):
                self.expenses_list = []

    def save_expenses(self):
        with open(self.expense_file, "w") as file:
            serializable = [exp.to_dict() for exp in self.expenses_list]
            json.dump(serializable, file, indent=4)

    def load_recurring_templates(self):
        if os.path.exists(self.recurring_file):
            try:
                with open(self.recurring_file, "r") as file:
                    raw_data = json.load(file)
                    self.templates_list = [
                        RecurringTemplate(t["Category"], t["Description"], t["Amount"], t["Frequency"], t["Last_Generated_Date"])
                        for t in raw_data
                    ]
            except json.JSONDecodeError:
                self.templates_list = []

    def save_recurring_templates(self):
        with open(self.recurring_file, "w") as file:
            serializable = [t.to_dict() for t in self.templates_list]
            json.dump(serializable, file, indent=4)

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

    def trigger_auto_generation_check(self, runtime_date: str):
        """Scans templates and processes dynamic auto-entries if window parameters roll forward."""
        generated_count = 0
        for template in self.templates_list:
            # Simple condition check: If template has not run for this current date window yet
            if template.last_generated_date != runtime_date:
                # Spawn a newborn entry transaction link wrapper
                auto_expense = Expense(
                    date=runtime_date,
                    category=template.category,
                    description=f"[Auto-{template.frequency}] {template.description}",
                    amount=template.amount
                )
                self.expenses_list.append(auto_expense)
                template.last_generated_date = runtime_date
                generated_count += 1
                
        if generated_count > 0:
            self.save_expenses()
            self.save_recurring_templates()
            print(f"\n[Automation Engine] Processed {generated_count} pending recurring expenditures for balance date: {runtime_date}")

    def add_new_expense(self):
        print("\n--- Add New Expense ---")
        date = input("Enter The Date on which you spent (YYYY-MM-DD): ").strip()
        
        # Background check automatically sparks right here upon encountering active dates
        self.trigger_auto_generation_check(date)
        
        category = input("What Type of expense you've made: ").strip()
        description = input("Describe your spending (optional): ").strip()
        
        while True:
            raw_amount = input("How much you've spent: Rs.").strip()
            try:
                amount = float(raw_amount)
                if amount <= 0: raise ValueError
                break
            except ValueError:
                print("[Error] Invalid amount numeric expression.")

        new_expense = Expense(date, category, description, amount)
        self.expenses_list.append(new_expense)
        self.save_expenses()
        print("\n>> Expense Added Successfully! <<")

    def run_search_engine(self):
        if not self.expenses_list: return
        print("\n==================================================")
        print("1. Search By Category\n2. Search By Keyword\n3. Search By Range")
        st = input("\nSelect a pattern (1-3): ").strip()
        matches = []
        if st == "1":
            cat = input("Target category: ").strip().lower()
            matches = [i for i in self.expenses_list if i.category == cat]
        elif st == "2":
            kw = input("Keyword: ").strip().lower()
            matches = [i for i in self.expenses_list if kw in i.description.lower()]
        elif st == "3":
            try:
                mn = float(input("Min: Rs.").strip())
                mx = float(input("Max: Rs.").strip())
                matches = [i for i in self.expenses_list if mn <= i.amount <= mx]
            except ValueError: return
            
        if matches: self.print_tabular_grid(matches)

    def view_analytics_dashboard(self):
        if not self.expenses_list: return
        print("\n==================================================")
        print("                EXPENSE ANALYTICS                 ")
        print("==================================================")
        total = self.get_total_spending()
        highest = max(self.expenses_list, key=lambda x: x.amount)
        print(f" • Total Spending        : Rs.{total:.2f}")
        print(f" • Highest Single Spend  : Rs.{highest.amount:.2f} ({highest.category})")
        print("==================================================")

    def handle_budget_menu(self):
        print("\n1. View Dashboard\n2. Update Target Limit")
        if input("\nChoice: ").strip() == "1":
            self.budget_manager.display_dashboard(self.get_total_spending())

    def generate_reports(self):
        if not self.expenses_list: return
        print("\n1. Daily Report\n2. Monthly Report")
        r_type = input("Select type: ").strip()
        label = input("Target window parameter (YYYY-MM-DD or YYYY-MM): ").strip()
        filtered = [e for e in self.expenses_list if e.date == label or e.date[:7] == label]
        if filtered:
            self.print_tabular_grid(filtered)

    def handle_recurring_workspace(self):
        """New console panel workspace module to add or monitor schedules."""
        print("\n==================================================")
        print("             RECURRING SUBSCRIPTIONS              ")
        print("==================================================")
        print("1. View Active Subscription Templates")
        print("2. Register New Recurring Cost Schedule")
        sub_choice = input("\nSelect workspace operation (1-2): ").strip()
        
        if sub_choice == "1":
            if not self.templates_list:
                print("\n[Notice] No recurring profiles currently booked.")
                return
            print("\n=====================================================================")
            print(f"{'No.':<5}│ {'Category':<15}│ {'Amount':<12}│ {'Frequency':<12}│ {'Last Run':<12}")
            print("─────┼────────────────┼─────────────┼─────────────┼──────────────────")
            for idx, t in enumerate(self.templates_list, 1):
                print(f"{idx:<5}│ {t.category:<15}│ Rs.{t.amount:<9.2f}│ {t.frequency:<12}│ {t.last_generated_date:<12}")
            print("=====================================================================")
            
        elif sub_choice == "2":
            cat = input("Enter schedule category (e.g., streaming, rent): ").strip()
            desc = input("Enter profile descriptive tag title: ").strip()
            try:
                amt = float(input("Enter fixed deduction cost: Rs.").strip())
                freq = input("Enter billing schedule recurrence interval (weekly/monthly): ").strip().lower()
                if freq not in ["weekly", "monthly"]:
                    print("[Error] Frequency configuration must be 'weekly' or 'monthly'.")
                    return
            except ValueError:
                print("[Error] Cost matrix entry must be numeric.")
                return
                
            new_template = RecurringTemplate(cat, desc, amt, freq, "Never")
            self.templates_list.append(new_template)
            self.save_recurring_templates()
            print(f"\n>> Success! Scheduled automated template for '{desc}' registered onto disk. <<")

    def render_visual_charts(self):
        """NEW METHOD: Processes data and outputs proportional character bars."""
        if not self.expenses_list:
            print("\n[Notice] Visual core charts empty. Add tracking logs first.")
            return

        print("\n==================================================")
        print("               VISUAL SPENDING TRENDS             ")
        print("==================================================")
        
        grand_total = self.get_total_spending()
        
        # Aggregate category data balances
        category_totals = {}
        for exp in self.expenses_list:
            category_totals[exp.category] = category_totals.get(exp.category, 0.0) + exp.amount

        print(" Category-Wise Comparison Charts:")
        print(" ────────────────────────────────")
        
        # Max horizontal bar width allocation constraints
        max_bar_width = 20
        
        for category, amount in category_totals.items():
            percentage = (amount / grand_total) * 100 if grand_total > 0 else 0
            
            # Proportional graph block sizing computation
            filled_blocks = int((amount / grand_total) * max_bar_width) if grand_total > 0 else 0
            empty_blocks = max_bar_width - filled_blocks
            
            chart_bar = "█" * filled_blocks + "░" * empty_blocks
            print(f" ■ {category:<12} [{chart_bar}] {percentage:>6.1f}% (Rs.{amount:.2f})")
            # ADDED: This line prints a clean separator right below each category bar
            print(" ────────────────────────────────")    
        
        
        # Render a complementary quick-view budget overview status bar link
        limit = self.budget_manager.monthly_limit
        budget_pct = (grand_total / limit) * 100 if limit > 0 else 0
        budget_filled = min(int(budget_pct / 10), 10)
        budget_bar = "█" * budget_filled + "░" * (10 - budget_filled)
        
        print("\n Budget Progress Usage Bar:")
        print(" ──────────────────────────")
        print(f" • Allowance [{budget_bar}] {budget_pct:.1f}% Used")
        print("==================================================")

    def start_main_loop(self):
        while True:
            print("\n==== MENU ====")
            print("1. Add Expense\n2. View All Expenses\n3. View Total Spending\n4. Advanced Search & Filter")
            print("5. View Expense Analytics\n6. Budget Management\n7. Reporting System\n8. Recurring Subscriptions")
            print("9. Visual Spending Trends <-- [NEW]\n10. Exit")
            print("=================")
            raw_choice = input("Please Enter Your Choice: ").strip()
            if not raw_choice.isdigit(): continue
            choice = int(raw_choice)
            
            if choice == 1: self.add_new_expense()
            elif choice == 2: self.print_tabular_grid(self.expenses_list) if self.expenses_list else print("\n[Notice] No records.")
            elif choice == 3: print(f"\nTotal: Rs.{self.get_total_spending():.2f}")
            elif choice == 4: self.run_search_engine()
            elif choice == 5: self.view_analytics_dashboard()
            elif choice == 6: self.handle_budget_menu()
            elif choice == 7: self.generate_reports()
            elif choice == 8: self.handle_recurring_workspace()
            elif choice == 9: self.render_visual_charts()
            elif choice == 10:
                print("\nThank You For Using Expense Tracker. Goodbye!")
                break
            else:
                print("\n[Error] Invalid Menu Option.")

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.start_main_loop()