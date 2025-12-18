import sqlite3
import csv
import sys
import os
import pandas as pd

DB_FILE = "users.db"
SQL_FILE = "createUsersTable.sql"
USERS_CSV = "useraccounts.csv"
PASSWORDS_CSV = "passwords.csv"

EMAIL_SUFFIX = "@clearcable.ca"
ACCOUNT_PREFIX = "001-"

def main():
    # Check required files
    for file in [SQL_FILE, USERS_CSV, PASSWORDS_CSV]:
        if not os.path.exists(file):
            print(f"Error: missing required file '{file}'")
            sys.exit(1)

    # Connect to DB
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Run the SQL File to create a table
    try:
        with open(SQL_FILE, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
    except sqlite3.OperationalError as e:
        if "already exists" not in str(e):
            raise

    # Using pandas, read the passwords and the user .csvs
    df_passwords = pd.read_csv(PASSWORDS_CSV)
    df_users = pd.read_csv(USERS_CSV)

    # Remove the whitespace in front of the column headers
    df_passwords.columns = df_passwords.columns.str.strip()
    df_users.columns = df_users.columns.str.strip()

    # Remove the whitespace in from of the column values
    df_passwords = df_passwords.map(lambda x: x.strip() if isinstance(x, str) else x)
    df_users = df_users.map(lambda x: x.strip() if isinstance(x, str) else x)

    print("Passwords Columns:", df_passwords.columns.tolist())
    print("Users Columns:", df_users.columns.tolist())

    # Combine the data on the Username column
    combined_data = pd.merge(df_passwords, df_users, on="Username")

    print(combined_data.to_dict(orient='records'))



    conn.commit()
    conn.close()
    print("Import completed successfully.")


if __name__ == "__main__":
    main()