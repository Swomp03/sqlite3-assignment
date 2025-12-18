import sqlite3
import sys
import os
import pandas as pd
from pathlib import Path

# Default values
# DB_FILE = "users.db"
# SQL_FILE = "createUsersTable.sql"
# USERS_CSV = "useraccounts.csv"
# PASSWORDS_CSV = "passwords.csv"
#
# EMAIL_SUFFIX = "@clearcable.ca"
# ACCOUNT_PREFIX = "001-"

def main():

    # Checks the length of the arguments to see if all of the files are provided correctly
    if len(sys.argv) < 7:
        print("Usage: python main.py <DB_FILE> <SQL_FILE> <USERS_CSV> <PASSWORDS_CSV> <EMAIL_SUFFIX> <ACCOUNT_PREFIX>")
        sys.exit(1)

    # print(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

    DB_FILE = sys.argv[1]
    SQL_FILE = sys.argv[2]
    USERS_CSV = sys.argv[3]
    PASSWORDS_CSV = sys.argv[4]
    EMAIL_SUFFIX = sys.argv[5]
    ACCOUNT_PREFIX = sys.argv[6]

    # print("EMAIL_SUFFIX =", EMAIL_SUFFIX[0:1])

    if(EMAIL_SUFFIX != EMAIL_SUFFIX[0:1]):
        EMAIL_SUFFIX = "@" + EMAIL_SUFFIX
        # print("New EMAIL_SUFFIX =", EMAIL_SUFFIX)


    # Check required files
    for file in [SQL_FILE, USERS_CSV, PASSWORDS_CSV]:
        if not os.path.exists(file):
            print(f"Error: missing required file '{file}'")
            sys.exit(1)

    # Deletes the original DB file if it exists
    db_path = Path(DB_FILE)
    if db_path.exists():
        db_path.unlink()

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

    # print("Passwords Columns:", df_passwords.columns.tolist())
    # print("Users Columns:", df_users.columns.tolist())

    # Make sure the files have the correct columns
    required_passwords = {'Username', 'Password'}
    required_users = {'accountNumber', 'Username', 'phonenumber', 'address'}

    # Check if the sets are subsets of the actual columns
    passwords_ok = required_passwords.issubset(df_passwords.columns)
    users_ok = required_users.issubset(df_users.columns)

    # If they are not in the correct format, print the missing columns and exit the program
    if not passwords_ok or not users_ok:
        print("Error: CSV files are missing required columns.")
        if not passwords_ok:
            missing = required_passwords - set(df_passwords.columns)
            print(f"Missing in Passwords CSV: {missing}")
        if not users_ok:
            missing = required_users - set(df_users.columns)
            print(f"Missing in Users CSV: {missing}")
        sys.exit(1)

    # print("Column validation successful!")

    # Create the insert query with the user account values to insert into the database
    insert_query = """
    INSERT INTO Users (accountnumber, username, emailaccount, phonenumber, address)
    VALUES (?, ?, ?, ?, ?)
    """

    contained_insert_error = False

    # For loop to insert each row into the database
    for i, row in df_users.iterrows():
        try:

            # Creates the parameters for each value
            params = (
                str(ACCOUNT_PREFIX) + str(row["accountNumber"]),
                row["Username"],
                row["Username"] + str(EMAIL_SUFFIX),
                row["phonenumber"],
                row["address"]
            )

            # Executes the insert and commits it to the database
            cursor.execute(insert_query, params)
            conn.commit()

        except KeyError as e:
            print("Error:", e)
            contained_insert_error = True


    contained_update_error = False

    # Create the update query to update the user account passwords
    update_query = """
    UPDATE Users
    SET password = ?
    WHERE username = ?
    """

    for i, row in df_passwords.iterrows():
        try:
            params = (
                row["Password"],
                row["Username"]
            )
            cursor.execute(update_query, params)
            conn.commit()

        except KeyError as e:
            print("Error:", e)
            contained_update_error = True


    conn.commit()
    conn.close()

    # If there were insert or update errors in the DB, tell the user
    if contained_update_error and contained_insert_error:
        print("Unable to insert or update table.")
        sys.exit(1)

    elif contained_insert_error:
        print("Unable to insert table.")
        sys.exit(1)

    elif contained_update_error:
        print("Unable to update table.")
        sys.exit(1)

    else:
        print("Database insert completed successfully.")


if __name__ == "__main__":
    main()