from db import get_connection
from tabulate import tabulate

def monthly_report(user_id):
    conn = get_connection()
    if not conn:
        print("Unable to connect to database.")
        return 

    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                DATE_FORMAT(date, '%Y-%m') AS month,
                SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) AS total_income,
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS total_expense,
                SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) -
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS balance
            FROM transactions
            WHERE user_id = %s
            GROUP BY month
            ORDER BY month DESC;
        """
        cursor.execute(query, (user_id,))
        records = cursor.fetchall()

        if not records:
            print("No transactions found for the user.")
        else:
            print("\nMonthly Financial Report\n")
            print(tabulate(records, headers="keys", tablefmt="fancy_grid"))

    except Exception as e:
        print(f"Error generating report: {e}")
    finally:
        cursor.close()
        conn.close()
      
