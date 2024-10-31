CREATE TABLE users (
user_id INTEGER PRIMARY KEY,
email TEXT UNIQUE NOT NULL,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
password TEXT NOT NULL,
gender TEXT NOT NULL,
account_created DATETIME DEFAULT CURRENT_TIMESTAMP,
contact_no TEXT NOT NULL
);

CREATE TABLE jobs (
id INTEGER PRIMARY KEY,
job_id TEXT NOT NULL,
user_id INTEGER NOT NULL,
company_name TEXT NOT NULL,
role TEXT NOT NULL,
location TEXT NOT NULL,
url TEXT NOT NULL,
job_source TEXT NOT NULL,
referral BOOLEAN NOT NULL,
application_id TEXT NOT NULL,
status INTEGER NOT NULL,
application_date DATE NOT NULL,
FOREIGN KEY(user_id) REFERENCES users(user_id));