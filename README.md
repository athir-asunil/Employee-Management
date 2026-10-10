# Employee Management System Using Python and SQLite

## Project Overview

The **Employee Management System** is a menu-driven, console-based application developed using Python and SQLite. It helps manage employee records, user authentication, and employee leave requests through a simple and organized interface.

The project follows Object-Oriented Programming (OOP) principles and uses database validation to maintain data integrity and prevent duplicate records.

## Features

### 1. User Registration and Authentication
- User registration and login functionality.
- Separate access for Admin and Employee roles.
- Authentication using credentials stored in the SQLite database.
- Password validation using Python Regular Expressions.

### 2. Password Validation
- Minimum length of 8 characters.
- At least one uppercase letter.
- At least one lowercase letter.
- At least one digit.
- At least one special character from the allowed set.

### 3. Employee Management
The Admin can:
- Add new employee records.
- View all employee details.
- Search for employees by name.
- Update employee information.
- Delete employee records.

### 4. Duplicate Record Prevention
- Uses SQL `UNIQUE` constraints to prevent duplicate usernames, email addresses, and phone numbers.
- Prevents the same user ID from being assigned to multiple employee records.
- Checks whether a user ID exists before linking it to an employee record.

### 5. Email and Phone Validation
- Validates email addresses using Regular Expressions.
- Ensures phone numbers contain only digits and exactly 10 digits.

### 6. Employee Profile
- Employees can view their personal profile.
- Employee records are linked to user accounts through user IDs.

### 7. Leave Management
- Employees can apply for leave by entering the leave type, start date, end date, and reason.
- Leave dates are validated using Python's `datetime` module.
- Prevents leave applications with a past start date.
- Ensures the end date is not earlier than the start date.
- New leave requests are saved with a `Pending` status.

### 8. Leave Approval System
- Admin can view employee leave requests.
- Admin can approve or reject requests.
- Employees can check their leave request status.

### 9. Database Management
- Uses SQLite for persistent data storage.
- Uses primary keys and foreign keys to establish relationships between tables.
- Uses parameterized SQL queries for database operations.

### 10. Object-Oriented Programming
- Uses classes, objects, methods, and inheritance.
- Separates common functionality, employee operations, and administrative operations.

## Technologies Used

- **Programming Language:** Python
- **Database:** SQLite
- **Libraries:** `sqlite3`, `re`, `datetime`
- **Code Editor:** Visual Studio Code

## Project Structure

```text
Employee-Management-System/
│
├── main.py
├── Employee Management.db
└── README.md
```

*Note: Replace `main.py` with your actual Python filename if it is different. The SQLite database file may be created automatically when the application runs.*

## How to Run the Project

### Prerequisites
- Python 3 installed.
- Visual Studio Code or another Python-compatible editor.

### Steps

1. Clone or download this repository.
2. Open the project folder in Visual Studio Code.
3. Open the terminal.
4. Run the Python file:

```bash
python main.py
```

5. Follow the on-screen menu to register, log in, and access the available features.

## Database Tables

### Users
Stores user account details, including:
- User ID
- Username
- Password
- Role

### Employees
Stores employee information, including:
- Employee ID
- User ID
- Name
- Email
- Phone number
- Department
- Designation
- Salary

### Leaves
Stores employee leave requests, including:
- Leave ID
- User ID
- Leave type
- Start date
- End date
- Reason
- Leave status

## Learning Outcomes

This project helped me practise:

- Python fundamentals and Object-Oriented Programming.
- SQLite database connectivity and CRUD operations.
- User authentication and role-based access.
- Input validation using Regular Expressions.
- Date validation using the `datetime` module.
- Database relationships and duplicate prevention.
- Exception handling and menu-driven application development.

## Future Enhancements

- Secure password hashing.
- Attendance tracking.
- Salary payment and payroll management.
- Monthly reports and leave summaries.
- Graphical user interface (GUI).

## Author

**Athira Sunil**

GitHub: [athir-asunil](https://github.com/athir-asunil)
```

### Before uploading to GitHub

- Make sure `main.py` matches your actual Python filename.
- Avoid uploading a database containing real employee information or passwords.
- For a public repository, consider excluding the database file and adding it to `.gitignore`.
- Your current project stores passwords in plain text, so password hashing is a recommended future improvement.

**How to add it:** In VS Code, create a new file named `README.md` in your project folder, paste the content above, save it, and commit and push it to GitHub.
