# Expense Tracker App

## Overview

Expense Tracker is a Python-based console application that helps users manage and analyze their personal expenses. The application supports multiple user profiles, persistent data storage using JSON files, budget tracking, recurring expense templates, spending analytics, and automatic backup recovery.

This project was built as part of my Python learning journey to practice software development concepts such as Object-Oriented Programming (OOP), file handling, JSON data persistence, data analysis, state management, error handling, and project structuring.

---

## Features

### User Profile Management

* Create and access multiple user profiles
* Automatically load saved user data
* Maintain separate expense records for each user

### Expense Management

* Add new expenses
* Store expense date, category, description, and amount
* View expenses in a formatted tabular layout

### Data Persistence

* Save all user data in JSON format
* Automatically load data when the application starts
* Preserve data across program restarts

### Backup & Recovery System

* Automatic backup file generation
* Recovery mechanism for corrupted database files
* Restore data from backup when possible

### Budget Tracking

* Set a monthly budget limit
* Store budget settings for each user profile

### Recurring Expense Templates

* Create recurring monthly expense templates
* Automatically generate recurring expenses when triggered
* Useful for subscriptions and fixed monthly bills

### Spending Analytics

* Calculate total spending
* Category-wise expense analysis
* Visual spending comparison using text-based charts

### Settings System

* Switch between user profiles
* Update monthly budget limits
* Create manual database backup snapshots

---

## Technologies Used

* Python
* Object-Oriented Programming (OOP)
* JSON
* File Handling
* Exception Handling
* Data Structures (Lists, Dictionaries)
* Modular Application Design

---

## Project Structure

```text
Expense
 ├── date
 ├── category
 ├── description
 └── amount

RecurringTemplate
 ├── category
 ├── description
 ├── amount
 ├── frequency
 └── last_generated_date

ExpenseTrackerApp
 ├── User Profile Management
 ├── Expense Management
 ├── Budget Management
 ├── Analytics
 ├── Backup & Recovery
 ├── Data Persistence
 └── Settings System
```

---

## Learning Outcomes

Through this project, I explored and gained exposure to:

* Designing classes and objects
* Converting objects into dictionaries for JSON storage
* Rebuilding objects from JSON data
* Managing application state
* Working with multiple user profiles
* Building backup and recovery mechanisms
* Organizing larger Python programs
* Understanding how software features interact within a larger application

---

## AI Contribution

This project was developed as a learning project with the assistance of AI tools. AI was used to:

* Explore feature ideas and project architecture
* Understand software design concepts
* Generate implementation approaches for different features
* Review and improve code structure
* Learn about OOP, JSON persistence, analytics, and project organization

The project was built incrementally level-by-level, and AI served as a learning assistant throughout the development process. The primary goal of this project was educational—to understand how larger Python applications are structured and how different software engineering concepts work together.

---

## Author

Rishabh Mittal

Built as part of my Python learning journey while developing software development skills before moving toward AI/ML.
