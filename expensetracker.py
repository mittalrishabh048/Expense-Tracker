# Expense Tracker

import datetime  # For automatically creating transaction timeline markers
import json      # For loading/saving our global multi-profile master dictionary
import os        # For checking if storage files already exist on your computer

# Global config variables defining our live database and safety insurance files
MASTER_FILE = "multi_user_tracker.json"
BACKUP_FILE = "multi_user_tracker_backup.json"

class Expense:
    """Models a single individual expense entry."""
    def __init__(self, date: str, category: str, description: str, amount: float):
        self.date = date
        self.category = category.strip().lower()
        self.description = description if description else "No Description"
        self.amount = amount

    def to_dict(self) -> dict:
        """Flattens object parameters into a standard dictionary map for JSON entries."""
        return {
            "Date": self.date,
            "Category": self.category,
            "Description": self.description,
            "Amount": self.amount
        }


class RecurringTemplate:
    """Models an automated template configuration profile for monthly bills."""
    def __init__(self, category: str, description: str, amount: float, frequency: str, last_generated_date: str):
        self.category = category.strip().lower()
        self.description = description
        self.amount = amount
        self.frequency = frequency.strip().lower()
        self.last_generated_date = last_generated_date

    def to_dict(self) -> dict:
        """Translates object properties into serializable dictionary pairs."""
        return {
            "Category": self.category,
            "Description": self.description,
            "Amount": self.amount,
            "Frequency": self.frequency,
            "Last_Generated_Date": self.last_generated_date
        }


class ExpenseTrackerApp:
    """Core multi-user system matching your original ATM persistence logic."""
    def __init__(self):
        # self.users matches self.accounts from your ATM project!
        self.users = {}
        self.current_user = None  # Global active session profile identifier
        
        # Session cache lists to store active user objects
        self.expenses_list = []
        self.templates_list = []
        self.monthly_budget = 5000.0
        
        # Initialize engine layers
        self.load_master_database()

    # ───────────────────────────────────────────────────────────────────────
    # LEVEL 10 CORE REFACTOR: DATA REDUNDANCY & RECOVERY LAYER
    # ───────────────────────────────────────────────────────────────────────
    
    def load_master_database(self):
        """Initializes system data, using a backup copy if files are broken."""
        if os.path.exists(MASTER_FILE):
            try:
                with open(MASTER_FILE, "r") as file:
                    self.users = json.load(file)
            except json.JSONDecodeError:
                print("\n[⚠️ DATABASE CORRUPTION DETECTED] Attempting automated restore...")
                self.trigger_restore_routine()
        else:
            self.users = {}
            self.save_master_database()

    def save_master_database(self):
        """Saves session states to the main file and makes a backup script copy."""
        # Sync the active user's current session state back to the master dictionary
        if self.current_user:
            self.users[self.current_user] = {
                "monthly_budget": self.monthly_budget,
                "expenses": [exp.to_dict() for exp in self.expenses_list],
                "recurring_templates": [t.to_dict() for t in self.templates_list]
            }
            
        # Write 1: Main database file update
        with open(MASTER_FILE, "w") as file:
            json.dump(self.users, file, indent=4)
            
        # Write 2: Duplicate mirror file update (Insurance copy)
        with open(BACKUP_FILE, "w") as file:
            json.dump(self.users, file, indent=4)

    def trigger_restore_routine(self):
        """Restores data files using your backup checkpoint copy."""
        if os.path.exists(BACKUP_FILE):
            try:
                with open(BACKUP_FILE, "r") as file:
                    self.users = json.load(file)
                with open(MASTER_FILE, "w") as file:
                    json.dump(self.users, file, indent=4)
                print("[Recovery Success] System database files restored from backup snapshot.")
            except json.JSONDecodeError:
                print("[Critical Error] Backup file also corrupted. Initializing clean repository.")
                self.users = {}
        else:
            print("[Notice] No backup logs found on disk. Initializing fresh workspace.")
            self.users = {}

    # ───────────────────────────────────────────────────────────────────────
    # AUTHENTICATION ENGINE
    # ───────────────────────────────────────────────────────────────────────

    def authenticate_profile(self) -> bool:
        """Asks for a profile name, creating a new workspace if it's new."""
        print("\n===== USER PROFILE SIGN-IN =====")
        username = input("Enter Profile Username: ").strip().lower()
        
        if not username:
            print("[Error] Username cannot be left blank.")
            return False
            
        self.current_user = username
        
        # Checking if profile exists in our Master Dictionary map
        if username in self.users:
            print(f"\n[Welcome Back] Profile loaded successfully: '{username}'")
            profile = self.users[username]
            
            # Extract configurations and re-hydrate lists with functional class objects
            self.monthly_budget = profile.get("monthly_budget", 5000.0)
            self.expenses_list = [
                Expense(i["Date"], i["Category"], i["Description"], i["Amount"])
                for i in profile.get("expenses", [])
            ]
            self.templates_list = [
                RecurringTemplate(t["Category"], t["Description"], t["Amount"], t["Frequency"], t["Last_Generated_Date"])
                for t in profile.get("recurring_templates", [])
            ]
        else:
            # If username doesn't exist, build a brand new profile structure
            print(f"\n[New Profile Initialized] Welcome '{username}'! Creating a clean workspace.")
            self.monthly_budget = 5000.0
            self.expenses_list = []
            self.templates_list = []
            self.save_master_database()
            
        return True

    # ───────────────────────────────────────────────────────────────────────
    # CORE TRACKER ENGINE METHODS
    # ───────────────────────────────────────────────────────────────────────

    def get_total_spending(self) -> float:
        return sum(exp.amount for exp in self.expenses_list)

    def print_tabular_grid(self, target_list: list):
        print("\n=======================================================================")
        header_str = f"{'No.':<5}│ {'Date':<12}│ {'Category':<15}│ {'Description':<25}│ {'Amount':>12}"
        print(header_str)
        print("─────┼─────────────┼────────────────┼──────────────────────────┼────────────")
        for idx, exp in enumerate(target_list, 1):
            desc = exp.description
            if len(desc) > 23: desc = desc[:20] + "..."
            print(f"{idx:<5}│ {exp.date:<12}│ {exp.category:<15}│ {desc:<25}│ Rs.{exp.amount:>9.2f}")
        print("=======================================================================")

    def trigger_auto_generation_check(self, runtime_date: str):
        """Scans templates and runs auto-generation updates if parameters roll forward."""
        generated_count = 0
        for template in self.templates_list:
            if template.last_generated_date != runtime_date:
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
            self.save_master_database()
            print(f"\n[Automation Engine] Logged {generated_count} monthly bills for date: {runtime_date}")

    def add_new_expense(self):
        print("\n--- Add New Expense ---")
        date = input("Enter Date (YYYY-MM-DD): ").strip()
        
        # Dynamic check auto-sparks matching templates
        self.trigger_auto_generation_check(date)
        
        category = input("Enter Category: ").strip()
        description = input("Enter Description: ").strip()
        
        # --- DATETIME TIMESTAMPER INTERACTION LAYER ---
        # Captures the live system clock time right now (e.g., 15:24:07)
        live_time = datetime.datetime.now().strftime("%H:%M:%S")
        # Appends the timestamp seamlessly onto the end of your description string
        stamped_description = f"{description} (Logged at {live_time})"

        while True:
            try:
                amount = float(input("Enter Amount: Rs.").strip())
                if amount <= 0: raise ValueError
                break
            except ValueError:
                print("[Error] Amount entry must be a positive number.")

        self.expenses_list.append(Expense(date, category, description, amount,stamped_description))
        self.save_master_database()
        print("\n>> Expense Registered & Master Configuration updated! <<")

    def render_visual_charts(self):
        """Builds scaling comparison graph charts with row dividers."""
        if not self.expenses_list:
            print("\n[Notice] No active transaction metrics logged yet.")
            return
            
        print("\n==================================================")
        print("               VISUAL SPENDING TRENDS             ")
        print("==================================================")
        grand_total = self.get_total_spending()
        
        category_totals = {}
        for exp in self.expenses_list:
            category_totals[exp.category] = category_totals.get(exp.category, 0.0) + exp.amount

        print(" Category-Wise Comparison Charts:")
        print(" ────────────────────────────────")
        for cat, amt in category_totals.items():
            pct = (amt / grand_total) * 100 if grand_total > 0 else 0
            blocks = int((amt / grand_total) * 20) if grand_total > 0 else 0
            
            # Displays bars separated by lines
            print(f" ■ {cat:<12} [{'█'*blocks + '░'*(20-blocks)}] {pct:>6.1f}% (Rs.{amt:.2f})")
            print(" ────────────────────────────────")
        print("==================================================")

    # ───────────────────────────────────────────────────────────────────────
    # SETTINGS PROFILE MANAGEMENT CORE
    # ───────────────────────────────────────────────────────────────────────

    def handle_settings_system(self):
        """Settings workspace to adjust budgets or quickly swap active profile users."""
        print("\n==================================================")
        print("                 SETTINGS SYSTEM                  ")
        print("==================================================")
        print("1. Switch Active Profile Account")
        print("2. Reconfigure Monthly Budget Target Limit")
        print("3. Trigger Manual Master Database Backup Snapshot")
        sub_choice = input("\nSelect custom settings option (1-3): ").strip()
        
        if sub_choice == "1":
            # Save the current state before switching profile contexts
            self.save_master_database()
            print(f"\n[Logging Out] Closing active session workspace for profile '{self.current_user}'...")
            self.authenticate_profile()
        elif sub_choice == "2":
            try:
                new_limit = float(input(f"Current budget limit is Rs.{self.monthly_budget:.2f}. Enter new limit: Rs.").strip())
                if new_limit <= 0: raise ValueError
                self.monthly_budget = new_limit
                self.save_master_database()
                print(">> Success! Target allowance reconfigured dynamically. <<")
            except ValueError:
                print("[Error] Invalid budget limit entry configuration parameter.")
        elif sub_choice == "3":
            self.save_master_database()
            print("\n>> Snapshot Success! Database files synchronized completely into backup ledger. <<")

    def start_main_loop(self):
        """Primary console workspace dashboard selection routing loop."""
        while True:
            print(f"\n==== ACTIVE SESSION PROFILE: [{self.current_user.upper()}] ====")
            print("1. Add New Expense Entry")
            print("2. View Tabular Transaction Spreadsheet")
            print("3. View Graphical Spending Progress Charts")
            print("4. Register Monthly Subscription Bill Template")
            print("5. Open Advanced Settings Profile Panel")
            print("6. Exit Application completely")
            print("================================─────────────────────────")
            raw_choice = input("Select operation index option (1-6): ").strip()
            if not raw_choice.isdigit(): continue
            choice = int(raw_choice)
            
            if choice == 1: self.add_new_expense()
            elif choice == 2: self.print_tabular_grid(self.expenses_list) if self.expenses_list else print("\n[Notice] Workspace empty.")
            elif choice == 3: self.render_visual_charts()
            elif choice == 4:
                cat = input("Enter schedule category profile tag: ").strip()
                desc = input("Enter billing account name text descriptor: ").strip()
                try:
                    amt = float(input("Enter fixed monthly cost parameter: Rs.").strip())
                    self.templates_list.append(RecurringTemplate(cat, desc, amt, "monthly", "Never"))
                    self.save_master_database()
                    print("\n>> Automated Subscription Registered! <<")
                except ValueError: print("[Error] Value input error.")
            elif choice == 5: self.handle_settings_system()
            elif choice == 6:
                self.save_master_database()
                print(f"\nSession terminated for profile '{self.current_user}'. Goodbye!")
                break


# --- SYSTEM RUNTIME INITIALIZATION ENTRY POINT ---
if __name__ == "__main__":
    app = ExpenseTrackerApp()
    # Pull profile authorization authentication gate before unleashing core dashboard loops
    if app.authenticate_profile():
        app.start_main_loop()