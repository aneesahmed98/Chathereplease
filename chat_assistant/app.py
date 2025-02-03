from flask import Flask, request, render_template
import sqlite3
import re

app = Flask(__name__)

def get_response(user_input):
    """Convert user question into an SQL query and fetch results."""
    conn = sqlite3.connect("company.db")
    cursor = conn.cursor()

    user_input = user_input.lower().strip()  # Clean up the input

    # Query: Show all employees in a department
    if "show me all employees in the" in user_input and "department" in user_input:
        department = re.search(r"show me all employees in the (.+?) department", user_input)
        if department:
            department_name = department.group(1).capitalize()
            cursor.execute("SELECT Name FROM Employees WHERE Department = ?", (department_name,))
            result = cursor.fetchall()
            response = f"Employees in the {department_name} department: {', '.join([row[0] for row in result])}" if result else f"No employees found in the {department_name} department."

    # Query: Who is the manager of a department
    elif "who is the manager of the" in user_input and "department" in user_input:
        department = re.search(r"who is the manager of the (.+?) department", user_input)
        if department:
            department_name = department.group(1).capitalize()
            cursor.execute("SELECT Manager FROM Departments WHERE Name = ?", (department_name,))
            result = cursor.fetchone()
            response = f"The manager of the {department_name} department is {result[0]}." if result else f"No manager found for the {department_name} department."

    # Query: List all employees hired after a specific date
    elif "list all employees hired after" in user_input:
        date = re.search(r"list all employees hired after (.+)", user_input)
        if date:
            hire_date = date.group(1).strip()
            cursor.execute("SELECT Name FROM Employees WHERE Hire_Date > ?", (hire_date,))
            result = cursor.fetchall()
            response = f"Employees hired after {hire_date}: {', '.join([row[0] for row in result])}" if result else f"No employees found hired after {hire_date}."

    # Query: Total salary expense for a department
    elif "what is the total salary expense for the" in user_input and "department" in user_input:
        department = re.search(r"what is the total salary expense for the (.+?) department", user_input)
        if department:
            department_name = department.group(1).capitalize()
            cursor.execute("SELECT SUM(Salary) FROM Employees WHERE Department = ?", (department_name,))
            result = cursor.fetchone()
            response = f"The total salary expense for the {department_name} department is ${result[0]:,.2f}." if result and result[0] is not None else f"No salary data found for the {department_name} department."

    else:
        response = "Sorry, I didn't understand that. Can you please rephrase or ask something else?"

    conn.close()
    return response

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form["query"]
        response = get_response(user_input)
        return render_template("index.html", user_input=user_input, response=response)
    return render_template("index.html", user_input="", response="")

if __name__ == "__main__":
    app.run(debug=True)
