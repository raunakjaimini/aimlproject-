import sqlite3
import pandas as pd

# Function to load data from a CSV file into a SQLite database
def load_csv_to_db(csv_file, db_name='analytics.db', table_name='tablee'):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Connecting to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Creating a table based on the DataFrame columns
    # Assuming the first row of the CSV contains column headers
    columns = ', '.join([f'[{col}] VARCHAR(255)' for col in df.columns])
    create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns});'
    cursor.execute(create_table_query)
    
    # Insert the DataFrame data into the SQLite table
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    
    # Display data inserted
    print(f"Data Inserted in the table {table_name}: ")
    data = cursor.execute(f'SELECT * FROM {table_name}')
    for row in data:
        print(row)
    
    # Commit your changes in the database
    conn.commit()
    
    # Closing the connection
    conn.close()

# Example usage
if __name__ == "__main__":
    # Replace 'analytics_data.csv' with your actual CSV file path
    load_csv_to_db('reportexcel.csv')
