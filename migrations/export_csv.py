import sqlite3
import pandas as pd

# Connect to your SQLite database
conn = sqlite3.connect('db/problems_db.sqlite')

# Example for two tables
table1 = pd.read_sql_query("SELECT * FROM LOGS", conn)

# Convert tables to CSV
table1.to_csv('LOGS.csv', index=False)
