from db import get_connection
from datetime import datetime
from tabulate import tabulate

def add_transactions(user_id):
    print("\n Add new Transaction")

    tx_type = input("Enter type (income/expense) : ").lower()
    if tx_type not in ["income", "expense"]:
        print("Invalid type Must be 'income' or 'expense'.")
        return 
    
    try:
        amount = float(input("Enter Amount: "))
    except ValueError:
        print("Amount must be a Number.")
        return 

    category = input("Enter category (e.g: Food,Rent): ").strip()
    date_input = input("Enter date (YYYY-MM-DD) [Leave blank for today]: ").strip()
    try:
        tx_date = date_input if date_input else datetime.today().strftime('%Y-%m-%d')    
        datetime.strptime(tx_date, '%Y-%m-%d')

    except ValueError:
        print(" Invalid date format.")
        return

    description = input("Enter description (Optional): ").strip()

    try:
        conn = get_connection()
        if conn is None:
            print("Could not connect to database.")
            return 

        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO transactions (user_id, amount, category, type, date, description) VALUES (%s,%s,%s,%s,%s,%s)""", (user_id, amount, category, tx_type, tx_date, description))
        conn.commit()
        print("Transaction added Successfully!")

    except Exception as e:
        print("Error:",e)

    finally:
        if conn:
            conn.close()        

def view_transactions(user_id):
    print("\n Recent Transactions")

    try:
        conn = get_connection()
        if conn is None:
            print("Could not connect to database")
            return

        cursor = conn.cursor()
        cursor.execute("""
                       SELECT id, type, amount, category, date, description
            FROM transactions
            WHERE user_id = %s
            ORDER BY date DESC, id DESC
            LIMIT 10
            """,(user_id,))
        records = cursor.fetchall()

        if records:
            headers = [ 'ID', 'TYPE', 'AMOUNT', 'CATEGORY', 'DATE', 'DESCRIPTION']
            print(tabulate(records, headers = headers, tablefmt="grid"))

        else:
            print("No Transactions Found.") 


    except Exception as e:
        print("Error:",e)
    finally:
        if conn:
            conn.close()               






