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


    conn.commit()
    conn.close()
    print("Import completed successfully.")


if __name__ == "__main__":
    main()