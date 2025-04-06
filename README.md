# 📝 Blog Post CLI App

A command-line application built with Python and MySQL for creating, viewing, and managing blog posts with tags.

## 📦 Features

- Create new blog posts with comma-separated tags  
- View all post titles  
- View specific post content by title  
- Search posts by tag  

## 🛠 Tech Stack

- Python  
- MySQL  
- `mysql-connector-python`  

## 🧱 Database Schema

- `posts(id, title, content)`  
- `tags(id, name)`  
- `post_tags(post_id, tag_id)`  

## 🔍 Search by Tag Feature

Performs an inner join between the `tags`, `post_tags`, and `posts` tables to retrieve all posts with the given tag name.

## 🚀 How to Run

1. Clone this repo:
   ```bash
   git clone https://github.com/03Ashwini/blog_app.git
   cd blog_app
   Install MySQL connector:
pip install mysql-connector-python
Create MySQL database and tables:

CREATE DATABASE blog_app;
USE blog_app;

CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    content TEXT
);

CREATE TABLE tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE post_tags (
    post_id INT,
    tag_id INT,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);
Run the app:
python blog_app.py
