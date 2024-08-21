import sqlite3

def check_table_structure(db_name='analytics.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # List all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if not tables:
        print("No tables found in the database.")
    else:
        print("Tables in the database:")
        for table in tables:
            print(f"- {table[0]}")
            # Show table schema
            cursor.execute(f"PRAGMA table_info({table[0]});")
            columns = cursor.fetchall()
            print("Columns:")
            for column in columns:
                print(f"  - {column[1]} ({column[2]})")

    conn.close()

# Check the structure
check_table_structure()
