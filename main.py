import os
import datetime

class BankAccount:
    
    def __init__(self, account_number, password, starting_balance=0.00):
        self.account_number = account_number
        self.password = password
        self.balance = starting_balance
        self.transaction_history = []
        
    def balance_enquery(self):
        return f"Your current balance: {self.balance}"

    def deposit(self, amount):
        self.balance += amount
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.transaction_history.append(f"On {timestamp}: Deposited {amount:.2f}")

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Transaction declined. Insufficient funds.")
        self.balance -= amount
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.transaction_history.append(f"On {timestamp}: Withdrew {amount:.2f}")

    def transfer(self, amount, recipient):
        if amount > self.balance:
            raise ValueError("Transaction declined. Insufficient funds.")
        self.balance -= amount
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.transaction_history.append(f"On {timestamp}: Transferred {amount:.2f} to {recipient}")

    def get_transaction_history(self):
        return "\n".join(self.transaction_history)

    def save_to_file(self):
        with open(f"account_{self.account_number}.txt", "w") as f:
            f.write(f"{self.account_number},{self.password},{self.balance}\n")
            for transaction in self.transaction_history:
                f.write(f"{transaction}\n")

    @classmethod
    def load_from_file(cls, account_number):
        if os.path.exists(f"account_{account_number}.txt"):
            with open(f"account_{account_number}.txt", "r") as f:
                lines = f.readlines()
                _, password, balance = lines[0].strip().split(",")
                account = cls(account_number, password, float(balance))
                for line in lines[1:]:
                    account.transaction_history.append(line.strip())
                return account
        else:
            return None

def main():
    accounts = {}

    while True:
        print("Welcome to ATM: ")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            account_number = input("Enter account number: ")
            password = input("Enter your pin: ")
            starting_balance = float(input("Enter starting balance: "))
            account = BankAccount(account_number, password, starting_balance)
            account.save_to_file()
            accounts[account_number] = account
            print("Account created successfully!")

        elif choice == "2":
            account_number = input("Enter account number: ")
            account = BankAccount.load_from_file(account_number)
            if account: 
                password = input("Enter your pin: ")
                if password == account.password:
                    while True:
                        print("Account Menu:")
                        print("1. Deposit")
                        print("2. Withdraw")
                        print("3. Transfer")
                        print("4. Transaction History")
                        print("5. Check Balance")
                        print("6. Logout")
                        choice = input("Enter your choice: ")

                        if choice == "1":
                            amount = float(input("Enter amount to deposit: "))
                            account.deposit(amount)
                            account.save_to_file()

                        elif choice == "2":
                            amount = float(input("Enter amount to withdraw: "))
                            try:
                                account.withdraw(amount)
                                account.save_to_file()
                            except ValueError as e:
                                print(e)

                        elif choice == "3":
                            amount = float(input("Enter amount to transfer: "))
                            recipient = input("Enter recipient's name: ")
                            try:
                                account.transfer(amount, recipient)
                                account.save_to_file()
                            except ValueError as e:
                                print(e)

                        elif choice == "4":
                            print(account.get_transaction_history())
                            
                        elif choice == "5":
                            print(account.balance_enquery())

                        elif choice == "6":
                            break

                        else:
                            print("Invalid choice. Please try again.")
                else:
                    print("Incorrect pin. Please try again !!!")
                    continue

            else:
                print("Account not found. Please try again.")

        elif choice == "3":
            print("Exiting ATM system.\nThank you")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()