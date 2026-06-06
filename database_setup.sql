-- Create database for ParkEasy
CREATE DATABASE IF NOT EXISTS parkeasy_db;
USE parkeasy_db;

-- Create contacts table
CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    parking_type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Create an index on email for faster lookups
CREATE INDEX idx_email ON contacts(email);
CREATE INDEX idx_created_at ON contacts(created_at);
