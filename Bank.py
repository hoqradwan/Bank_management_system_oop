class Bank:
    __capital = 100000
    __accounts = []
    __loan_amount = 0
    __isLoan = True

    @classmethod
    def create_account(cls, name, email, address, account_type):
        account = Account(name, email, address, account_type)
        cls.__accounts.append(account)
        return account

    @classmethod
    def get_account(cls, email):
        for account in cls.__accounts:
            if account.email == email:
                return account
        return None

    @classmethod
    def delete_account(cls, email):
        account = cls.get_account(email)
        if account:
            cls.__accounts.remove(account)
            return f"Account with email {email} deleted."
        return f"Account with email {email} not found."

    @classmethod
    def total_balance(cls):
        return cls.__capital

    @classmethod
    def total_loan_amount(cls):
        return cls.__loan_amount

    @classmethod
    def toggle_loan_feature(cls, is_on):
        cls.__isLoan = is_on


class Account:
    count = 100

    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type

        self.balance = 0
        self.loan_taken = 0
        self.account_number = Account.count
        Account.count += 1
        self.transaction_history = []

    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
            Bank._Bank__capital += amount
            self.transaction_history.append(f"Deposited {amount} TK.")
            return f"Deposited {amount} TK to account {self.account_number}."
        else:
            return "Invalid Input."

    def withdraw(self, amount):
        if amount >= 0 and amount <= self.balance:
            self.balance -= amount
            Bank._Bank__capital -= amount
            self.transaction_history.append(f"Withdrew {amount} TK.")
            return f"Withdrew {amount} TK from account {self.account_number}."
        else:
            self.transaction_history.append("Withdrawal amount exceeded.")
            return "Withdrawal amount exceeded."

    def check_balance(self):
        return f"Account {self.account_number} balance: {self.balance} TK."

    def get_transaction_history(self):
        return self.transaction_history

    def take_loan(self, amount):
        if Bank._Bank__isLoan and amount > 0:
            if self.loan_taken < 2:
                self.loan_taken += 1
                self.balance += amount
                Bank._Bank__capital -= amount
                Bank._Bank__loan_amount += amount
                self.transaction_history.append(f"Loan of {amount} TK taken.")
                return f"Loan of {amount} TK taken from account {self.account_number}."
            else:
                return "You have already taken the maximum number of loans."
        else:
            return "Loan facility is currently unavailable."

    def transfer(self, to_account_email, amount):
        to_account = Bank.get_account(to_account_email)
        if to_account:
            if self.balance >= amount:
                self.balance -= amount
                to_account.balance += amount
                self.transaction_history.append(
                    f"Transferred {amount} TK to account {to_account.account_number}.")
                return f"Transferred {amount} TK from account {self.account_number} to account {to_account.account_number}."
            else:
                self.transaction_history.append(
                    "Insufficient balance for the transfer.")
                return "Insufficient balance for the transfer."
        else:
            self.transaction_history.append("Account does not exist.")
            return "Account does not exist."

    def show_info(self):
        return f"Name: {self.name}\nEmail: {self.email}\nAddress: {self.address}\nAccount Type: {self.account_type}\nAccount Number: {self.account_number}"


class Admin(Account):
    def __init__(self, name, email, address):
        super().__init__(name, email, address, "admin")

    def create_account(self, name, email, address, account_type):
        return Bank.create_account(name, email, address, account_type)

    def delete_account(self, email):
        return Bank.delete_account(email)

    def all_accounts(self):
        account_info = []
        for account in Bank._Bank__accounts:
            account_info.append(account.show_info())
        return account_info

admin = Admin("Admin", "admin@gmail.com", "Dhaka")
current_user = None

while True:
    print("\n No user logged in!")
    print("1. Register")
    print("2. Login as Admin")
    print("3. Login as User")
    print("4. Exit")
    ch = input("Choose an option: ")

    if ch == "1":
        name = input("Name: ")
        email = input("Email:  ")
        address = input("Address:  ")
        account_type = input("Account Type (sv/cr):  ")

        if account_type in ["sv", "cr"]:
            account = Bank.create_account(name, email, address, account_type)
            current_user = account
            print(
                f"Account created successfully. Account Number: {account.account_number}")
        else:
            print("Invalid account type.")

    elif ch == "2":
        admin_email = input("Admin email: ")
        if admin_email == admin.email:
            print("Admin logged in.")
            while True:
                print("1. Create account")
                print("2. Delete account")
                print("3. List of all accounts")
                print("4. Check Bank Capital")
                print("5. Check total loan amount")
                print("6. Toggle loan feature")
                print("7. Logout")
                admin_ch = input("Choose an option: ")

                if admin_ch == "1":
                    name = input("Name: ")
                    email = input("Email: ")
                    address = input("Address: ")
                    account_type = input("Account Type (sv/cr): ")

                    if account_type in ["sv", "cr"]:
                        account = admin.create_account(
                            name, email, address, account_type)
                        print(
                            f"Account created successfully. Account Number: {account.account_number}")
                    else:
                        print("Invalid account type.")

                elif admin_ch == "2":
                    email = input("Email of the account to be deleted: ")
                    result = admin.delete_account(email)
                    print(result)

                elif admin_ch == "3":
                    accounts = admin.all_accounts()
                    if accounts:
                        for account in accounts:
                            print(account)
                    else:
                        print("No accounts to display.")

                elif admin_ch == "4":
                    total_balance = Bank.total_balance()
                    print(f"Total bank capital: {total_balance} TK")

                elif admin_ch == "5":
                    total_loan_amount = Bank.total_loan_amount()
                    print(f"Total Loan Amount: {total_loan_amount} TK")

                elif admin_ch == "6":
                    loan_feature = input("Toggle Loan Feature (on/off): ")
                    if loan_feature in ["on", "off"]:
                        Bank.toggle_loan_feature(loan_feature == "on")
                        print(f"Loan feature is now {loan_feature}.")
                    else:
                        print("Invalid choice.")

                elif admin_ch == "7":
                    print("Admin logged out.")
                    break
                else:
                    print("Invalid choice.")
        else:
            print("Invalid admin email.")
    elif ch == "3":
        user_email = input("User email: ")
        for account in Bank._Bank__accounts:
            if user_email == account.email:
                current_user = account
                print(f"User {current_user.name} logged in!")
                while True:
                    print("1. Withdraw")
                    print("2. Deposit")
                    print("3. Check balance")
                    print("4. Transaction history")
                    print("5. Take loan")
                    print("6. Transfer money")
                    print("7. Logout\n")
                    user_ch = input("Choose an option: ")
                    if user_ch == "1":
                        amount = int(input("Enter withdraw amount:"))
                        result = current_user.withdraw(amount)
                        print(result)
                    elif user_ch == "2":
                        amount = int(input("Enter deposit amount:"))
                        result = current_user.deposit(amount)
                        print(result)
                    elif user_ch == "3":
                        result = current_user.check_balance()
                        print(result)
                    elif user_ch == "4":
                        history = current_user.get_transaction_history()
                        if history:
                            for transaction in history:
                                print(transaction)
                        else:
                            print("No transaction history available.")
                    elif user_ch == "5":
                        amount = int(input("Enter loan amount:"))
                        result = current_user.take_loan(amount)
                        print(result)
                    elif user_ch == "6":
                        receiver_email = input("Enter receiver email: ")
                        amount = int(input("Enter transfer amount: "))
                        result = current_user.transfer(receiver_email, amount)
                        print(result)
                    elif user_ch == "7":
                        current_user = None
                        break
    elif ch == "4":
        print("Exiting the system.")
        break
    else:
        print("Invalid choice.")

