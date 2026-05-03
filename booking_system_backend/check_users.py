import sqlite3

conn = sqlite3.connect('../booking.db')
cursor = conn.cursor()

# First, check what tables exist
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in database:")
for table in tables:
    print(f"  - {table[0]}")

print("\n" + "="*50 + "\n")

# Try to query users table
try:
    cursor.execute("SELECT user_id, name, email FROM users")
    users = cursor.fetchall()
    
    print(f"Found {len(users)} users in the database:\n")
    
    john_found = False
    for user in users:
        user_id, name, email = user
        print(f"ID: {user_id}, Name: '{name}', Email: {email}")
        if name and 'john' in name.lower():
            john_found = True
            print("  ^ Contains 'john'")
    
    print("\n" + "="*50)
    if john_found:
        print("✓ User(s) with 'John' in name found!")
    else:
        print("✗ No user named 'John' found in database")
        
except sqlite3.OperationalError as e:
    print(f"Error querying users table: {e}")

conn.close()

# Made with Bob
