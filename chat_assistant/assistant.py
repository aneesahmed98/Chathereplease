import sqlite3
import re

# Connect to the SQLite database
conn = sqlite3.connect("company.db")
cursor = conn.cursor()

def get_response(user_input):
    """Convert user question into an SQL query and fetch results."""
    
    user_input = user_input.lower().strip()  # Convert input to lowercase and remove extra spaces

    # Query: Show all employees in a department
    if "show me all employees in the" in user_input and "department" in user_input:
        department = re.search(r"show me all employees in the (.+?) department", user_input)
        if department:
            department_name = department.group(1).capitalize()
            try:
                cursor.execute("SELECT Name FROM Employees WHERE Department = ?", (department_name,))
                result = cursor.fetchall()
                if result:
                    return f"Employees in the {department_name} department: {', '.join([row[0] for row in result])}"
                else:
                    return f"No employees found in the {department_name} department."
            except sqlite3.Error:
                return "Error querying the database for employees in the specified department."

    # Query: Who is the manager of a department
    if "who is the manager of the" in user_input and "department" in user_input:
        department = re.search(r"who is the manager of the (.+?) department", user_input)
        if department:
            department_name = department.group(1).capitalize()
            try:
                cursor.execute("SELECT Manager FROM Departments WHERE Name = ?", (department_name,))
                result = cursor.fetchone()
                if result:
                    return f"The manager of the {department_name} department is {result[0]}."
                else:
                    return f"No manager found for the {department_name} department."
            except sqlite3.Error:
                return "Error querying the database for the department's manager."

    # Query: List all employees hired after a specific date
    if "list all employees hired after" in user_input:
        date = re.search(r"list all employees hired after (.+)", user_input)
        if date:
            hire_date = date.group(1).strip()
            try:
                cursor.execute("SELECT Name FROM Employees WHERE Hire_Date > ?", (hire_date,))
                result = cursor.fetchall()
                if result:
                    return f"Employees hired after {hire_date}: {', '.join([row[0] for row in result])}"
                else:
                    return f"No employees found hired after {hire_date}."
            except sqlite3.Error:
                return "Error querying the database for employees hired after the specified date."

    # Query: Total salary expense for a department
    if "what is the total salary expense for the" in user_input and "department" in user_input:
        department = re.search(r"what is the total salary expense for the (.+?) department", user_input)
        if department:
            department_name = department.group(1).capitalize()
            try:
                cursor.execute("SELECT SUM(Salary) FROM Employees WHERE Department = ?", (department_name,))
                result = cursor.fetchone()
                if result and result[0] is not None:
                    return f"The total salary expense for the {department_name} department is ${result[0]:,.2f}."
                else:
                    return f"No salary data found for the {department_name} department."
            except sqlite3.Error:
                return "Error querying the database for salary expenses in the specified department."

    # Catch all for unrecognized queries
    return "Sorry, I didn't understand that. Can you please rephrase or ask something else?"

# Simple loop to interact with the assistant
print("Chat Assistant Ready! Type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = get_response(user_input)
    print("Bot:", response)

# Close connection when done
conn.close()
