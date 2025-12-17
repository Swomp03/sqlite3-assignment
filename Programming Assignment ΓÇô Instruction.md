# **Programming Assignment – Instructions**

## **Objective**

Create a script that imports user account information from two CSV files into a SQLite3 database using a provided SQL schema. The script should modify certain fields before insertion and associate passwords with the correct users.

---

## **Assignment Steps**

Intro: Write a script in Perl or Python to do the following.

1. **Review the Provided Files**

   - **SQL Schema:** `Users.sql` — defines the `Users` table.
   - **CSV Files:**

     - `useraccounts.csv` (or `UserBasic.csv`) — contains account details.
     - `passwords.csv` — contains usernames and passwords.

2. **Create a SQLite3 Database**

   - Use the provided `Users.sql` schema to create the database and the `Users` table.

3. **Read and Process the CSV Files**

   - Load data from the two CSV files.
   - Add an email suffix (e.g., `@clearcable.ca`) to the username and save it in the `emailaccount` column.
   - Add a prefix (e.g., `001-`) to all account numbers before saving.

4. **Insert Data into the Database**

   - Insert the modified data from the user accounts CSV into the `Users` table.
   - Match and insert passwords from `passwords.csv` based on the username.

5. **Command-Line Arguments**

   - The script should accept the filenames, email suffix, and account number prefix as command-line arguments.

6. **Error Handling**

   - Handle missing files, invalid data, and database errors gracefully.

7. **Documentation**

   - Include a README explaining:
     - How to install and run the script.
     - Any assumptions made.

8. **Implementation Requirements**

- Use Local libraries i.e. carton for perl or UV for python
- Use git tracking to commit during development (Use semantic git commits)
- Include README with how to install and run the script
- Include Error handling in the code
- Include comments in the code
- Use any tools at your disposal
- Use command line arguments for the filenames and the emailsuffix and accountprefix variables
- Make adjustments to the database if required
- Make sure the import can run multiple times, as if the source files could change

---
