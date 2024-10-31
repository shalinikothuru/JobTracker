-- SQL queries

-- Creating the 'JobTracker' Database
CREATE SCHEMA IF NOT EXISTS JobTracker;

-- Creating Users Table
CREATE TABLE IF NOT EXISTS Users ( 
User_id INTEGER PRIMARY KEY AUTO_INCREMENT,
Email VARCHAR(50) Unique NOT NULL,
First_Name VARCHAR(100) NOT NULL,
Last_Name VARCHAR(100) NOT NULL,
Contact_No CHAR(10) UNIQUE NOT NULL, 
Password VARCHAR(25) NOT NULL,
Gender CHAR(1) NOT NULL,
Account_Created DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Creating Jobs Table
CREATE TABLE Jobs (
Id SERIAL PRIMARY KEY AUTO_INCREMENT,
User_id INTEGER,
Job_id VARCHAR(50) NOT NULL,
Company_name VARCHAR(50) NOT NULL,
Role VARCHAR(50) NOT NULL,
Location VARCHAR(25) NOT NULL,
URL VARCHAR(255) NOT NULL,
Job_source VARCHAR(20),
Referral VARCHAR(3) DEFAULT "NO",
Application_id VARCHAR(50) UNIQUE NOT NULL,
Status VARCHAR(20) NOT NULL,
Application_date DATE NOT NULL
);

-- Adding Foreign Keys to the Jobs Table
ALTER TABLE Jobs ADD CONSTRAINT For_Key1
FOREIGN KEY (User_id) REFERENCES Users(User_id);

-- Sample Queries
	-- Insert into Users, upon Sign Up
    -- Syntax
    INSERT INTO Users (Email, First_name, Last_Name, Contact_No, Password, Gender)
    VALUES (<user_id>, <email>, <first_name>, <last_name>, <contact_no>, <password>, <gender>);
    
    -- Sample Data
    INSERT INTO users (Email, First_Name, Last_Name, Contact_No, Password, Gender)
	VALUES ('skothuru@iu.edu', 'Shalini', 'Kothuru', "1234567890", 'hellopwd', 'F');
    
    INSERT INTO Users (Email, First_name, Last_Name, Contact_No, Password, Gender)
    VALUES ("md@iu.test", "Mal", "Dhop", "0987654321", "****", "M");

	select * from Users;

	-- Inserting data into Jobs table
	-- user_id will be retrieved based on login
	-- Syntax
	INSERT INTO Jobs (user_id, Job_id, Company_name, Role, Location, URL, Job_source, Referral, Application_id, Status, Application_date)
	VALUES (<user_id>, <job_id>, <Company_Name>, <Role>, <location>, <URL>, <Job_source>, <Referral>, <Application_id>, <Status>, <Application_date>);

	-- Sample Data
	INSERT INTO Jobs (user_id, Job_id, Company_name, Role, Location, URL, Job_source, Referral, Application_id, Status, Application_date)
	VALUES (1, 'A34567', 'Alphabet Inc', 'Data Analyst', 'Remote',
	'https://www.linkedin.com/jobs/search/?currentJobId=3852948160&keywords=data%20analyst&origin=BLENDED_SEARCH_RESULT_NAVIGATION_JOB_CARD&originToLandingJobPostings=3885119004%2C3884815445%2C3887319571', 
	'LinkedIn', 'NO', 'APP001', 'Applied', '2024-04-07');

	INSERT INTO Jobs (user_id, Job_id, Company_name, Role, Location, URL, Job_source, Referral, Application_id, Status, Application_date)
	VALUES (2, 'A3567', 'Tesla', 'Database Developer', 'Hybrid',
	'https://www.linkedin.com/jobs/search/?currentJobId=3852948160&keywords=data%20analyst&origin=BLENDED_SEARCH_RESULT_NAVIGATION_JOB_CARD&originToLandingJobPostings=3885119004%2C3884815445%2C3887319571', 
	'Indeed', 'NO', 'ACP001', 'Applied', '2024-03-07');

	select * from Jobs;

-- Update Query Syntax -
-- Updating the User Info
-- Syntax to Update everything except User_id & Email & Gender
UPDATE Users
SET First_Name = <first_name>, Last_Name = <last_name>, Contact_No = <contact_no>, Password = <password>
where User_id = 1;

UPDATE Users
SET Email = "TEST@iu.test", First_Name = "Malhar Dhopate", Last_Name = "Dhopate", Contact_No = "0987654321", Password = "1234", Gender = "M" 
where User_id = 1;

-- Syntax to update only the Application Status 
UPDATE Jobs
SET status = <status> where User_id = <user_id> and Job_id = <job_id>;

-- View Queries 
-- A View to Display the User Profile
CREATE VIEW UserProfile AS(
SELECT user_id, Email, First_Name || ' ' || Last_Name AS Full_Name, Gender FROM users);
    
-- A View to display job application for a User
CREATE VIEW job_applications AS (
SELECT * FROM Jobs WHERE user_id = <user_id> -- This will be pulled from the user's log in info
ORDER BY application_date DESC
);

-- A View to Display the Number of jobs user has applied to in the last month
CREATE VIEW num_of_jobs_applied_monthly as (  
SELECT COUNT(*) AS num_of_jobs_applied_monthly FROM Jobs
WHERE User_id = <user_id>  -- This will be pulled from the user's log in info
AND 
Application_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH));

-- A View to Display the Number of jobs user has applied to in the last week
CREATE VIEW num_of_jobs_applied_weekly as (
SELECT COUNT(*) AS num_of_jobs_applied_weekly
FROM Jobs
WHERE User_id = <user_id> -- This will be pulled from the user's log in info
AND YEAR(Application_date) = YEAR(CURRENT_DATE())
AND WEEK(Application_date) = WEEK(CURRENT_DATE()));

-- Ratio of application status - This View Displays the number of applications for each Application Status
CREATE VIEW pie_chart_ratio as (
SELECT Status, COUNT(*) AS count
FROM Jobs
WHERE User_id = <user_id> -- This will be pulled from the user's log in info
AND Status IN (SELECT DISTINCT Status FROM Jobs WHERE User_id = <user_id>)
GROUP BY Status);

-- Map visualization by number of jobs by locations - This View displays the count of applications for every location
CREATE VIEW map_location_wise as (
SELECT Location, COUNT(*) AS num_of_applications
FROM Jobs
WHERE User_id = <user_id> -- This will be pulled from the user's log in info
GROUP BY Location);

-- Number of application by referrals - This View Displays the number of job applications done through each Referals.
CREATE VIEW applications_by_referrals as (
SELECT Referral, COUNT(*) AS num_of_applications
FROM Jobs
WHERE User_id = <user_id> -- This will be pulled from the user's log in info
AND Referral = 'YES'
GROUP BY Referral);

-- Number of application by job source - This view Displays the number of job applications by each Job Source.
CREATE VIEW bar_applications_by_job_source as (
SELECT Job_source, COUNT(*) AS num_of_applications
FROM Jobs
WHERE User_id = <user_id> -- This will be pulled from the user's log in info
AND Job_source IS NOT NULL
GROUP BY Job_source);

-- Creating an Index for Email 
CREATE UNIQUE INDEX Email_index ON Users (Email);

