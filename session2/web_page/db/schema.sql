-- schema.sql
-- This file defines the database schema for our Flask application.

-- Drop tables if they already exist to allow for clean re-initialization.
-- In a production environment, you would typically use migrations instead of dropping tables.
DROP TABLE IF EXISTS chat_history;
DROP TABLE IF EXISTS chats;
DROP TABLE IF EXISTS users;

-- Create the 'users' table (unchanged).
-- 'id' is an auto-incrementing primary key for unique user identification.
-- 'username' stores the user's unique username, ensuring no duplicates.
-- 'password' stores the hashed password for security.
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

-- Create the 'chats' table.
-- Each row represents a unique conversation.
-- 'id' is the primary key for the chat.
-- 'user_id' is a foreign key linking to the 'users' table, indicating which user owns this chat.
-- 'bot_id' will store an identifier for the chatbot persona (e.g., 'default', 'friendly_ai').
-- 'message_count' stores the total number of messages in this chat.
-- 'last_message_at' stores the timestamp of the last message in this chat, for sorting/display.
-- 'is_archived' is a boolean flag to mark chats as archived (0 for false, 1 for true).
CREATE TABLE chats (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  bot_id TEXT NOT NULL DEFAULT 'default',
  message_count INTEGER NOT NULL DEFAULT 0,
  last_message_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_archived BOOLEAN NOT NULL DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create the 'chat_history' table.
-- Each row represents a single message within a conversation.
-- 'id' is the primary key for the message.
-- 'chat_id' is a foreign key linking to the 'chats' table.
-- 'message_index' provides an ordering for messages within a chat.
-- 'role' indicates who sent the message ('user' or 'assistant').
-- 'content' stores the actual text of the message.
-- 'timestamp' records when the message was sent.
CREATE TABLE chat_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  chat_id INTEGER NOT NULL,
  message_index INTEGER NOT NULL,
  role TEXT NOT NULL, -- 'user' or 'assistant'
  content TEXT NOT NULL,
  timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (chat_id) REFERENCES chats (id),
  UNIQUE (chat_id, message_index) -- Ensure unique message order within a chat
);
