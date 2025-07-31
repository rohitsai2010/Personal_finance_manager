import csv
from db import get_connection

def export_to_csv(user_id):
    conn = get_connection()
    if not conn:
        print("Unable to connect to database")
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
            print("No records found to export.")
            return 
        
        filename =  f"monthly_report_{user_id}.csv"
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)

        print(f"Monthly report exported successfully to '{filename}'.")

    except Exception as e:
        print(f"Error exporting to CSV: {e}")
    finally:
        cursor.close()
        conn.close()