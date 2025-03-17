from datetime import datetime

class BankAccount:
    total_accounts = 0  
    account_log = []    

    def _init_(self, account_holder, initial_balance=0, account_type='Current'):
        if not account_holder.strip():
            raise ValueError("Account holder name cannot be empty.")
        
        self.account_holder = account_holder
        self.balance = initial_balance
        self.account_type = account_type
        self.transactions = []
        self.account_number = BankAccount.total_accounts + 1

        BankAccount.total_accounts += 1
        BankAccount.account_log.append(self)

        self.transactions.append(f"Account created with balance ₹{self.balance}")
        print(f" New {self.account_type} account created for {self.account_holder} (Account No: {self.account_number})")

    def deposit(self, amount):
        if amount > 50000:
            print("Deposit rejected: Amount exceeds ₹50,000 limit.")
            return
        
        self.balance += amount
        self.transactions.append(f"Deposited ₹{amount} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Deposited ₹{amount}. New balance: ₹{self.balance}")

    def withdraw(self, amount):
        if amount > 50000:
            print("Withdrawal rejected: Amount exceeds ₹50,000 limit.")
            return

        if self.balance - amount < 0:
            print(" Withdrawal rejected: Insufficient funds.")
            return
        
        self.balance -= (amount + 10)  # ₹10 transaction fee
        self.transactions.append(f"Withdrew ₹{amount} (₹10 fee applied) on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Withdrew ₹{amount}. New balance: ₹{self.balance}")

    def transfer(self, recipient, amount):
        if amount > 50000:
            print(" Transfer rejected: Amount exceeds ₹50,000 limit.")
            return

        if self.balance - amount < 0:
            print(" Transfer rejected: Insufficient funds.")
            return

        self.balance -= amount
        recipient.balance += amount
        self.transactions.append(f"Transferred ₹{amount} to {recipient.account_holder} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        recipient.transactions.append(f"Received ₹{amount} from {self.account_holder} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Transferred ₹{amount} to {recipient.account_holder}. New balance: ₹{self.balance}")

    def check_balance(self):
        print(f"Account Balance for {self.account_holder}: ₹{self.balance}")

    def get_transaction_history(self):
        print(f" Transaction History for {self.account_holder}:")
        for transaction in self.transactions:
            print(f" - {transaction}")

    @classmethod
    def get_total_accounts(cls):
        print(f"Total Bank Accounts: {cls.total_accounts}")

class SavingsAccount(BankAccount):
    MINIMUM_BALANCE = 1000  # Minimum balance requirement for Savings Account

    def _init_(self, account_holder, initial_balance=0):
        if initial_balance < self.MINIMUM_BALANCE:
            raise ValueError("Initial deposit must meet the minimum balance requirement of ₹1000.")
        super()._init_(account_holder, initial_balance, account_type='Savings')

    def withdraw(self, amount):
        if self.balance - amount < self.MINIMUM_BALANCE:
            print(f" Withdrawal rejected: Minimum balance requirement of ₹{self.MINIMUM_BALANCE} must be maintained.")
            return
        super().withdraw(amount)

    def calculate_interest(self):
        interest = self.balance * 0.05
        self.balance += interest
        self.transactions.append(f"Interest of ₹{interest} added on {datetime.now().strftime('%Y-%m-%d')}")
        print(f" Interest of ₹{interest} added. New balance: ₹{self.balance}")

class CurrentAccount(BankAccount):
    def _init_(self, account_holder, initial_balance=0):
        super()._init_(account_holder, initial_balance, account_type='Current')


def cli():
    print(" Welcome to Python Bank CLI")
    accounts = {}

    while True:
        print("\n1. Create Account\n2. Deposit Money\n3. Withdraw Money\n4. Transfer Money\n5. Check Balance\n6. View Transaction History\n7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter account holder name: ")
            acc_type = input("Account type (Savings/Current): ").strip().capitalize()
            initial_balance = float(input("Enter initial deposit amount: "))

            if acc_type == 'Savings':
                account = SavingsAccount(name, initial_balance)
            else:
                account = CurrentAccount(name, initial_balance)
            
            accounts[account.account_number] = account

        elif choice == '2':
            acc_num = int(input("Enter account number: "))
            amount = float(input("Enter deposit amount: "))
            accounts[acc_num].deposit(amount)

        elif choice == '3':
            acc_num = int(input("Enter account number: "))
            amount = float(input("Enter withdrawal amount: "))
            accounts[acc_num].withdraw(amount)

        elif choice == '4':
            sender_num = int(input("Enter your account number: "))
            receiver_num = int(input("Enter recipient's account number: "))
            amount = float(input("Enter transfer amount: "))
            accounts[sender_num].transfer(accounts[receiver_num], amount)

        elif choice == '5':
            acc_num = int(input("Enter account number: "))
            accounts[acc_num].check_balance()

        elif choice == '6':
            acc_num = int(input("Enter account number: "))
            accounts[acc_num].get_transaction_history()

        elif choice == '7':
            print(" Exiting... Thank you for using Python Bank CLI!")
            break

        else:
            print("Invalid choice. Please try again.")
   
