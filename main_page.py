import sqlite3
import re
from datetime import datetime
# con=sqlite3.connect("Employee Management.db")
# cursor=con.cursor()
# cursor.execute("""
#                CREATE TABLE IF NOT EXISTS Users(
#                id INTEGER PRIMARY KEY,
#                username VARCHAR ,
#                userpassword VARCHAR,
#                role VARCHAR
#                );
#                """)

class EmployeeManagement:

    #TABLE CREATION
    def __init__(self):
        self.con=sqlite3.connect("Employee Management.db")
        self.c=self.con.cursor()
        self.c.execute(""" 
                       CREATE TABLE IF NOT EXISTS Users(
                       id INTEGER PRIMARY KEY,
                       username VARCHAR UNIQUE,
                       password VARCHAR,
                       role VARCHAR
                       );
                      """ )
        self.con.commit()

        self.c.execute("""
        CREATE TABLE IF NOT EXISTS Leaves(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            leave_type VARCHAR,
            from_date VARCHAR,
            to_date VARCHAR,
            reason VARCHAR,
            status VARCHAR DEFAULT 'Pending',
            FOREIGN KEY(user_id) REFERENCES Users(id)
        )
        """)

        self.con.commit()

    def admin_signup(self):
        self.c.execute("""
        SELECT * FROM Users
        WHERE username = ? AND role = ?
         """, ("admin", "admin"))
        admin = self.c.fetchone()
        if admin is None:
            self.c.execute("""
            INSERT INTO Users (username, password, role)
            VALUES (?, ?, ?)
            """, ("admin", "Admin@123", "admin"))

            self.con.commit()
            print("Default admin created successfully.")
            print()
            self.login("admin")
            print("Opening Admin page.........")
            
        else:
            print()
            print("Admin already exists.")
            self.login("admin")
            print()
            print("Opening Admin Login page.......")
            # print()
            # print("*************************************************************************************************")
            # print("         WELCOME TO ADMIN DASHBOARD.........")


    def signup(self):

        username = input("Enter your username: ")

        # Check duplicate username
        self.c.execute("""
        SELECT id FROM Users
        WHERE username = ?
        """, (username,))

        existing_user = self.c.fetchone()

        if existing_user:
            print("Username already exists.")
            print()
            print("Please choose another username.")
            print()
            # return None

        pattern = r"^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%&*])[A-Za-z\d!@#$%&*]{8,}$"

        while True:
            password = input("Enter your password: ")

            if re.match(pattern, password):
                break
            else:
                print(
                "Your password must contain at least one digit, "
                "one uppercase, one lowercase, special character "
                "and minimum 8 characters."
                 )
        role = "Employee"

        self.c.execute("""
        INSERT INTO Users(username, password, role)
        VALUES (?, ?, ?)
        """, (username, password, role))

        self.con.commit()

        user_id = self.c.lastrowid

        print()
        print("SIGNUP SUCCESSFUL")
        print()
        print("Your User ID is:", user_id)

        return user_id
       

    def login(self, role):

        while True:
            username = input("Enter username: ")
            password = input("Enter password: ")

            self.c.execute("""
            SELECT id, username, password, role
            FROM Users
            WHERE username = ? AND password = ?
            """, (username, password))

            user = self.c.fetchone()

            if user:
                print("Login successful")
                print()

                user_id = user[0]
                username = user[1]
                user_role = user[3]

                return user_id, username, user_role

            else:
                print("Invalid username or password")

                if role == "Employee":
                    print("Are you a new joinee?")
                else:
                    print("Are you a new admin?")

                choice = int(input("Enter 1 for SIGNUP or 2 for LOGIN: "))

                if choice == 1:
                    if role == "Employee":
                        return self.signup()
                    else:
                        self.admin_signup()

                elif choice == 2:
                    continue   
        


class Employee(EmployeeManagement):
    def view_personal_profile(self, user_id):
        self.c.execute("""
            SELECT id,name, email, phone, department, designation,salary
            FROM Employees
            WHERE user_id = ?
        """, (user_id,))

        employee = self.c.fetchone()

        if employee:
            print()
            print("=" * 120)
            print("              WELCOME  ",employee[1].upper())
            print("=" * 120)
            print()
            print("           PERSONAL PROFILE")
            print()
            print("-" * 120)
                    
            print(
            f"{'id':<5}"
            f"{'Name':<20}"
            f"{'Email':<30}"
            f"{'Phone':<15}"
            f"{'Department':<20}"
            f"{'Designation':<20}"
            f"{'Salary':<10}"
                                )
            print("-" * 120)
            print(
            f"{employee[0]:<5}"
            f"{employee[1]:<20}"
            f"{employee[2]:<30}"
            f"{employee[3]:<15}"
            f"{employee[4]:<20}"
            f"{employee[5]:<20}"
            f"{employee[6]:<10}"
                                )
                        
            print("-" * 120)

            # print("=" * 60)
        else:
            print("Employee profile not found.")

    from datetime import datetime


    def apply_leave(self, user_id):

        print()
        print("=" * 50)
        print("              APPLY LEAVE")
        print("=" * 50)

        leave_type = input("Enter leave type: ")

    # FROM DATE VALIDATION
        while True:
            from_date = input("Enter from date (YYYY-MM-DD): ")
            print()

            try:
                from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()

                if from_date_obj < datetime.today().date():
                    print("From date cannot be a past date.")
                    print()
                    continue

                break

            except ValueError:
                print("Invalid date.")
                print()
                print("Please enter date in YYYY-MM-DD format.")
                print()
                print("Example: 2026-10-15")
                print()


    # TO DATE VALIDATION
        while True:
            to_date = input("Enter to date (YYYY-MM-DD): ")
            print()

            try:
                to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()

                if to_date_obj < from_date_obj:
                    print("To date cannot be before the from date.")
                    print()
                    continue

                break

            except ValueError:
                print("Invalid date.")
                print()
                print("Please enter date in YYYY-MM-DD format.")
                print()
                print("Example: 2026-10-17")
                print()


        reason = input("Enter reason: ")


        self.c.execute("""
        INSERT INTO Leaves(
        user_id,
        leave_type,
        from_date,
        to_date,
        reason,
        status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
        user_id,
        leave_type,
        from_date,
        to_date,
        reason,
        "Pending"
        ))

        self.con.commit()

        print()
        print("Leave application submitted successfully.")
        print("Status: Pending")

    def view_leave_status(self, user_id):

        self.c.execute("""
        SELECT
        id,
        leave_type,
        from_date,
        to_date,
        reason,
        status
        FROM Leaves
        WHERE user_id = ?
        """, (user_id,))

        leaves = self.c.fetchall()

        if not leaves:
            print()
            print("You have not applied for any leave.")
            return

        print()
        print("=" * 100)
        print(" " * 35, "MY LEAVE DETAILS")
        print("=" * 100)

        print(
        f"{'ID':<5}"
        f"{'Leave Type':<20}"
        f"{'From Date':<15}"
        f"{'To Date':<15}"
        f"{'Reason':<25}"
        f"{'Status':<15}"
        )

        print("-" * 100)

        for leave in leaves:
            print(
            f"{leave[0]:<5}"
            f"{leave[1]:<20}"
            f"{leave[2]:<15}"
            f"{leave[3]:<15}"
            f"{leave[4]:<25}"
            f"{leave[5]:<15}"
            )

            print("-" * 100)          
class Admin(EmployeeManagement):
    def add_employee(self):

        self.c.execute("""
        CREATE TABLE IF NOT EXISTS Employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        name VARCHAR,
        email VARCHAR UNIQUE,
        phone VARCHAR UNIQUE,
        department VARCHAR,
        designation VARCHAR,
        salary REAL,
        FOREIGN KEY(user_id) REFERENCES Users(id)
        )
        """)

        self.con.commit()

        user_id = int(input("Enter User ID: "))

    # Check whether User ID exists
        self.c.execute("""
        SELECT id FROM Users
        WHERE id = ?
        """, (user_id,))

        user = self.c.fetchone()

        if user is None:
            print()
            print("User ID does not exist.")
            return

    # Check whether employee already exists
        self.c.execute("""
        SELECT id FROM Employees
        WHERE user_id = ?
        """, (user_id,))

        existing_employee = self.c.fetchone()

        if existing_employee:
            print()
            print("Employee already exists for this User ID.")
            return

        name = input("Enter Employee name: ")

    # EMAIL VALIDATION
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        while True:
            email = input("Enter Email: ")

            if not re.match(email_pattern, email):
                print("Invalid email format.")
                print("Example: athira@gmail.com")
                continue

        # Check duplicate email
            self.c.execute("""
            SELECT id FROM Employees
            WHERE email = ?
            """, (email,))

            existing_email = self.c.fetchone()

            if existing_email:
                print("Email already exists.")
                continue
            break

    # PHONE VALIDATION
        while True:
            phone = input("Enter phone number: ")

            if not phone.isdigit():
                print("Phone number must contain only digits.")
                continue

            if len(phone) != 10:
                print("Phone number must contain exactly 10 digits.")
                continue

            self.c.execute("""
            SELECT id FROM Employees
            WHERE phone = ?
            """, (phone,))

            existing_phone = self.c.fetchone()

            if existing_phone:
                print("Phone number already exists.")
                continue
            break

        department = input("Enter Department: ")
        designation = input("Enter Designation: ")
        salary = float(input("Enter Salary: "))

        self.c.execute("""
        INSERT INTO Employees(
        user_id,
        name,
        email,
        phone,
        department,
        designation,
        salary
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
        user_id,
        name,
        email,
        phone,
        department,
        designation,
        salary
        ))

        self.con.commit()

        print()
        print("Employee added successfully.")

    def view_all_employees(self):

        self.c.execute("""
        SELECT id, name,email,phone, department, designation, salary
        FROM Employees
        """)

        rows = self.c.fetchall()
        print("-" * 120)
        
        print(
        f"{'ID':<5}"
        f"{'Name':<20}"
        f"{'Email':<30}"
        f"{'Phone':<15}"
        f"{'Department':<20}"
        f"{'Designation':<20}"
        f"{'Salary':<10}"
                    )
        
        print("-" * 120)

        for row in rows:
            print(
                f"{row[0]:<5}"
                f"{row[1]:<20}"
                f"{row[2]:<30}"
                f"{row[3]:<15}"
                f"{row[4]:<20}"
                f"{row[5]:<20}"
                f"{row[6]:<10}"
                    )
            
            print("-" * 120)
    def search_employee(self):
        choice="yes"
        while(choice!="no"):
            print()
            name = input("Enter employee name to search: ")

            self.c.execute(
            "SELECT * FROM Employees WHERE name = ?",
             (name,))
      
            result = self.c.fetchone()

            if result:
                print("Employee found!")
                print()
                
                print("-" * 120)

                print(
                f"{'ID':<5}"
                f"{'Name':<20}"
                f"{'Email':<30}"
                f"{'Phone':<15}"
                f"{'Department':<20}"
                f"{'Designation':<20}"
                f"{'Salary':<10}"
                )

                print("-" * 120)

                print(
                f"{result[0]:<5}"
                f"{result[2]:<20}"
                f"{result[3]:<30}"
                f"{result[4]:<15}"
                f"{result[5]:<20}"
                f"{result[6]:<20}"
                f"{result[7]:<10}"
                )

                print("-" * 120)
                print()
                choice=input("Are you want to continue search (yes/no)  ")

            else:
                print("Employee not found")
                print()
                choice=input("Are you want to continue search (yes/no)  ")

    def update_employee(self):
            print()
            employee_id = int(input("Enter employee ID to update: "))
    
            self.c.execute("""
            SELECT * FROM Employees
            WHERE id = ?
            """, (employee_id,))
    
            employee = self.c.fetchone()
    
            if employee:
                print("Employee found!")
                print("Current Details:")
                print("-" * 120)
                
                print(
                f"{'ID':<5}"
                f"{'Name':<20}"
                f"{'Email':<30}"
                f"{'Phone':<15}"
                f"{'Department':<20}"
                f"{'Designation':<20}"
                f"{'Salary':<10}"
                 )
                
                print("-" * 120)
                
                print(
                f"{employee[0]:<5}"
                f"{employee[2]:<20}"
                f"{employee[3]:<30}"
                f"{employee[4]:<15}"
                f"{employee[5]:<20}"
                f"{employee[6]:<20}"
                f"{employee[7]:<10}"
                        )
                
                          
                print()
                print("Enter new details")
    
                name = input("Enter Name: ")
                email = input("Enter Email: ")
                phone = input("Enter Phone: ")
                department = input("Enter Department: ")
                designation = input("Enter Designation: ")
                salary = float(input("Enter Salary: "))
    
                self.c.execute("""
                UPDATE Employees
                SET name = ?,
                    email = ?,
                    phone = ?,
                    department = ?,
                    designation = ?,
                    salary = ?
                WHERE id = ?
            """, (name, email, phone, department,
                  designation, salary, employee_id))
    
                self.con.commit()
                print()
                print("Employee details updated successfully.")
                print()
    
            else:
                print("Employee not found.")    

    def delete_employee(self):
        print()
        employee_id = int(input("Enter employee ID to delete: "))
        print()

        self.c.execute("""
        SELECT * FROM Employees
        WHERE id = ?
        """, (employee_id,))

        employee = self.c.fetchone()

        if employee:
            print("Employee found!")
        
            print("-" * 120)
                           
            print(
            f"{'ID':<5}"
            # f"{'user_id':<10}"
            f"{'Name':<20}"
            f"{'Email':<30}"
            f"{'Phone':<15}"
            f"{'Department':<20}"
            f"{'Designation':<20}"
            f"{'Salary':<10}"
            )
                           
            print("-" * 120)
            print(
            f"{employee[0]:<5}"
            f"{employee[2]:<20}"
            f"{employee[3]:<30}"
            f"{employee[4]:<15}"
            f"{employee[5]:<20}"
            f"{employee[6]:<20}"
            f"{employee[7]:<10}"
                                    )
                            
            print()

            confirm = input("Are you sure you want to delete this employee? (yes/no): ")

            if confirm.lower() == "yes":
                self.c.execute("""
                DELETE FROM Employees
                WHERE id = ?
                """, (employee_id,))

                self.con.commit()

                print("Employee deleted successfully.")
                print()

            else:
                print("Deletion cancelled.")
                print()

        else:
            print("Employee not found.")
            print()                   
    
    
    def view_leave_requests(self):

        self.c.execute("""
        SELECT
        Leaves.id,
        Employees.name,
        Leaves.leave_type,
        Leaves.from_date,
        Leaves.to_date,
        Leaves.reason,
        Leaves.status
        FROM Leaves
        JOIN Employees
        ON Leaves.user_id = Employees.user_id
        """)

        leaves = self.c.fetchall()

        if not leaves:
            print()
            print("No leave requests available.")
            return 

        print()
        print("=" * 120)
        print("                         LEAVE REQUESTS")
        print("=" * 120)

        print(
        f"{'ID':<5}"
        f"{'Employee Name':<20}"
        f"{'Leave Type':<20}"
        f"{'From Date':<15}"
        f"{'To Date':<15}"
        f"{'Reason':<25}"
        f"{'Status':<15}"
        )

        print("-" * 120)

        for leave in leaves:

            print(
            f"{leave[0]:<5}"
            f"{leave[1]:<20}"
            f"{leave[2]:<20}"
            f"{leave[3]:<15}"
            f"{leave[4]:<15}"
            f"{leave[5]:<25}"
            f"{leave[6]:<15}"
            )

            print("-" * 120)
    def change_leave_status(self):

        print()
        leave_id = int(input("Enter Leave ID: "))

    # Check whether leave exists
        self.c.execute("""
        SELECT Leaves.id, Employees.name, Leaves.leave_type,
           Leaves.from_date, Leaves.to_date,
           Leaves.reason, Leaves.status
        FROM Leaves
        JOIN Employees
        ON Leaves.user_id = Employees.user_id
        WHERE Leaves.id = ?
        """, (leave_id,))

        leave = self.c.fetchone()

        if leave is None:
            print("Leave request not found.")
            return

    # Show leave details
        print()
        print("-" * 100)
        print("Leave ID     :", leave[0])
        print("Employee     :", leave[1])
        print("Leave Type   :", leave[2])
        print("From Date    :", leave[3])
        print("To Date      :", leave[4])
        print("Reason       :", leave[5])
        print("Current Status:", leave[6])
        print("-" * 100)

        print()
        print("1. Approve")
        print("2. Reject")

        choice = input("Enter your choice (1/2): ")

        if choice == "1":
            status = "Approved"

        elif choice == "2":
            status = "Rejected"

        else:
            print("Invalid choice.")
            return

    
        self.c.execute("""
                      UPDATE Leaves
                      SET status = ?
                       WHERE id = ?
                       """, (status, leave_id))

        self.con.commit()

        print()
        print("Leave status changed successfully.")
        print("New Status:", status) 
           
def start_first():
    print()
    print()
    print("*"*120)
    print()
    print()
    print(" "*40,"EMPLOYEE MANAGEMENT SYSTEM")
    print()
    print()
    print("*"*120)
    print()
    print()
    print()
    print("1.ADMIN")
    print("2.EMPLOYEE")
    print("3.EXIT")
    print()
    n=int(input("Enter Your Role "))
    print()
    print("-"*120)
    return n

    
def start(n):

    employee_object = EmployeeManagement()
    # print("-"*120)
    print(" "*50,"MAIN MENU")
    print("-"*120)

    print("1.SIGN UP")
    print("2.LOGIN")
    print("3.EXIT")

    role_choose = int(input("Enter your choice: "))

    if role_choose == 1:

        if n == 1:
            user_id=employee_object.admin_signup()
            admin_menu()

        elif n == 2:
            user_id = employee_object.signup()

            print("Employee signup successful")

            employee_menu(user_id)

    elif role_choose == 2:

        user_id, username, role = employee_object.login("")

        # print("User ID:", user_id)
        # print("Username:", username)
        # print("Role:", role)

        if role.lower() == "admin":
            admin_menu()

        elif role.lower() == "employee":
            employee_menu(user_id)

    elif role_choose == 3:
        n=start_first()
        start(n)

def admin_menu():

    admin = Admin()
    choice = 0

    while choice != 10:

        print("=" * 120)
        print(" "*45,"ADMIN MENU")
        print("=" * 120)

        print("1. Add new employees")
        print("2. View all employees")
        print("3. Search employees")
        print("4. Update employee details")
        print("5. Delete employees")
        print("6. View employee attendance/leave")
        print("7. Logout")
        print()

        choice = int(input("Enter your choice: "))

        if choice == 1:
            admin.add_employee()

        elif choice == 2:
            admin.view_all_employees()

        elif choice == 3:
            admin.search_employee()

        elif choice == 4:
            admin.update_employee()

        elif choice == 5:
            admin.delete_employee()
        elif choice==6:
            while True:

                print()
                print("=" * 60)
                print("              LEAVE MANAGEMENT")
                print("=" * 60)

                print("1. View Leave Requests")
                print("2. Approve / Reject Leave")
                print("3. Back to Admin Menu")
                print()

                leave_choice = int(input("Enter your choice: "))

                if leave_choice == 1:
                    admin.view_leave_requests()

                elif leave_choice == 2:
                    admin.change_leave_status()

                elif leave_choice == 3:
                    break

                else:
                    print("Invalid choice.")

        elif choice == 7:
            print()
            print("Admin logged out.")
            print()
            start(n)
def employee_menu(user_id):

    employee = Employee()
    choice = 0

    while choice != 6:

        print("=" * 120)
        print(" "*50,"EMPLOYEE MENU")
        print("=" * 120)

        print("1. View personal profile")
        # print("2. View salary/pay details")
        print("2. Apply for leave")
        print("3. view leave_status")
        # print("5. View announcements")
        
        print("4. Logout")
        print()

        choice = int(input("Enter your choice: "))

        if choice == 1:
            employee.view_personal_profile(user_id)
        elif choice==2:
            employee.apply_leave(user_id) 
        elif choice==3:
            employee.view_leave_status(user_id)     

        elif choice == 4:
            print()
            print("Employee logged out.")
            print()
            start(n)

        else:
            print()
            print("This option is not implemented yet.")            
    


n=start_first()   
start(n)
         


