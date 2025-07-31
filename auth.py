from db import get_connection
import getpass       # this is a module that will not show the password if we typr it it will keep it confidentially

def register_user():
    print("\n Register New Account")
    username = input("Enter username: ").strip()
    password = getpass.getpass("Enter password: ").strip()

    if not username or not password:
        print("Please enter both username and password")
        return 
    
    try:
        conn = get_connection()
        cursor = conn.cursor()

#so read the sql query properly that it will return the id of the user if it is present in db. if at all any output comes. the output will come because of cursor.fetchone()
        cursor.execute("Select id From users WHERE username = %s",(username,))                       
        if cursor.fetchone():
            print("Username already exists")
            return
        
        cursor.execute("INSERT INTO users(username,password) VALUES (%s,%s)", (username,password))
        conn.commit()

        print("Resgistration is successful! Now you can Login.")

    except Exception as e:
        print("Error during registration: ",e)
    finally:
        conn.close()


def login_user():
    print("\n🔐 Login")
    username = input("Enter username: ").strip()
    password = getpass.getpass("Enter password: ").strip()

    if not username or not password:
        print("❌ Username and password cannot be empty.")
        return None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        if result:
            print(f"✅ Welcome back, {username}!")
            return result[0]  # return user_id
        else:
            print("❌ Invalid credentials. Please try again.")
            return None
    except Exception as e:
        print("❌ Error during login:", e)
        return None
    finally:
        conn.close()










