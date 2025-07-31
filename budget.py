from db import get_connection
from datetime import datetime
from tabulate import tabulate

def set_budget(user_id):
    print("\n Set Monthly Budget")

    category = input("Enter Category (e.g: Food,Rent,Transport): ").strip()
    try:
        amount = float(input("Enter budget amount for this month category: "))

    except ValueError:
        print("Invald Amount.")
        return
    
    month = input("Enter month (YYYY-MM) [leave blank for current Month]: ").strip()

    try:
        budget_month = month if month else datetime.today().strftime('%Y-%m')
        datetime.strptime(budget_month, '%Y-%m')

    except ValueError:
        print("Invalid month format")
        return 

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM budgets WHERE user_id = %s AND category = %s AND month = %s""", (user_id, category, budget_month))
                       
        existing = cursor.fetchone()

        if existing:
            cursor.execute("""
                           UPDATE budgets SET amount = %s
                WHERE user_id = %s AND category = %s AND month = %s""",(amount, user_id, category, budget_month))
            print("Budget Updated.")

        else:
            cursor.execute("""
                           INSERT INTO budgets (user_id, category, amount, month)
                VALUES (%s, %s, %s, %s)""",(user_id, category, amount, budget_month))
            print("Budget is set.")

        conn.commit()

    except Exception as e:
        print("Error: ",e)
    finally:
        if conn:
            conn.close()


def view_budgets(user_id):
    print("\n Your Budgets") 

    month = input("Enter month (YYYY-MM) [Leave Blank for Current Month]: ").strip()

    try:
        budget_month = month if month else datetime.today().strftime('%Y-%m')
        datetime.strptime(budget_month, '%Y-%m')

    except ValueError:
        print("Invalid month format.")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT b.category, b.amount AS budget_amount,
                IFNULL(SUM(t.amount), 0) AS spent
            FROM budgets b
            LEFT JOIN transactions t
                ON b.user_id = t.user_id AND b.category = t.category
                AND DATE_FORMAT(t.date, '%Y-%m') = b.month AND t.type = 'expense'
            WHERE b.user_id = %s AND b.month = %s
            GROUP BY b.category, b.amount
        """, (user_id, budget_month))

        results = cursor.fetchall()

        if results:
            headers = ['Category', 'Budget (₹)', 'Spent (₹)', 'Remaining (₹)']
            table = []
            for row in results:
                category, budget_amount, spent = row
                remaining = float(budget_amount) - float(spent)
                table.append([category, f"{budget_amount:.2f}", f"{spent:.2f}", f"{remaining:.2f}"])
            print(tabulate(table, headers=headers, tablefmt='grid'))
        else:
            print("No budgets found for this month.")

    except Exception as e:
        print("Error:", e)
    finally:
        if conn:
            conn.close()

                       
                       


     
     
            
            
                           
