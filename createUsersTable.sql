CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    accountnumber VARCHAR(20),
    username VARCHAR(5) UNIQUE,
    emailaccount VARCHAR(15),
    phonenumber INTEGER,
    address VARCHAR(255),
    password VARCHAR(128)
);
