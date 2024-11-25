from flask import Flask, render_template, request, redirect, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key for session management

# Database connection configuration
db_config = {
    "host": "mysql-db",  # This is the hostname of the MySQL service in Docker Compose
    "user": "root",
    "password": "password",
    "database": "test_db"
}

# Function to establish a database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user:
                return "Login Successful"
            else:
                flash("Invalid username or password", "error")
                return redirect("/")
        else:
            flash("Database connection failed", "error")
            return redirect("/")

    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

