-- schema.sql
-- This file defines the database schema for our Flask application.

-- Drop the 'users' table if it already exists to allow for clean re-initialization.
-- In a production environment, you would typically use migrations instead of dropping tables.
DROP TABLE IF EXISTS users;

-- Create the 'users' table.
-- 'id' is an auto-incrementing primary key for unique user identification.
-- 'username' stores the user's unique username, ensuring no duplicates.
-- 'password' stores the hashed password for security.
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);
