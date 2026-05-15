CREATE DATABASE talentedo;
USE talentedo;

CREATE TABLE enquiries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    phone INT(20),
    course VARCHAR(100),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE gallery (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100)
);

INSERT INTO courses (course_name) VALUES
("Python Fullstack"),
("Data Science"),
("Data Analytics"),
("MySQL"),
("Cloud Computing"),
("Basic Computer Course"),
("Advanced Computer Course"),
("Tally Accounting"),
("Software Testing Selenium"),
("Software Testing Tosca"),
("System Design");

CREATE TABLE admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(255)   -- hashed password
);