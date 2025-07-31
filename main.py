from auth import register_user, login_user
from transactions import add_transactions, view_transactions   #thses are the functions that will be imported from other folders
from budget import set_budget, view_budgets
from reports import monthly_report
from export import export_to_csv

def main_menu(user_id):
    while True:
        print("\n========Personal Finance Manager========")
        print("1. Add Income/Expense")
        print("2. View Transactions")
        print("3. Set Monthly Budget")
        print("4. View Budgets")
        print("5. View Monthly Report")
        print("6. Export Transaction to CSV")
        print("7. LOGOUT")
        choice = input("Select an Option: ")

        if choice == "1":
            add_transactions(user_id)
        elif choice == "2":
            view_transactions(user_id)
        elif choice == "3":
            set_budget(user_id)
        elif choice ==  "4":
            view_budgets(user_id)
        elif choice == "5":
            monthly_report(user_id)
        elif choice == "6":
            export_to_csv(user_id)
        elif choice == "7":
            print("Logged out Successfully.\n")
            break
        else:
            print("Invalid choice. Please choose a valid option.\n")


def start():
    while True:
        print("\n========Welcome toPersonal Finance Manager========")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Select an Option: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            user_id = login_user()
            if user_id:
                main_menu(user_id)

        elif choice == "3":
            print("Exiting.....")
            break
        else:
            print("Invalid Option. Try Again")



#if we want to run a program from the same file we will use this. in this case we will run start() function. if the code is to imported from another file we will write the name of file in place of main
if __name__ == "__main__":
    start()                    






