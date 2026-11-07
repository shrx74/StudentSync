from flask import Flask, request, jsonify
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


# Database connection function
def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


# Create the database table
def create_table():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL
                )
            """)

        connection.commit()

    finally:
        connection.close()


# Insert a student
@app.route("/students", methods=["POST"])
def add_student():

    data = request.get_json()

    if not data or not isinstance(data.get("name"), str) or not data["name"].strip():
        return jsonify({"error": "A valid name is required"}), 400

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                "INSERT INTO students (name) VALUES (%s) RETURNING id, name",
                (data["name"].strip(),)
            )

            student = cursor.fetchone()

        connection.commit()

        return jsonify({
            "message": "Student added successfully",
            "student": {
                "id": student[0],
                "name": student[1]
            }
        }), 201

    finally:
        connection.close()


# Retrieve all students
@app.route("/students", methods=["GET"])
def get_students():

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute("SELECT id, name FROM students ORDER BY id")

            students = cursor.fetchall()

        return jsonify([
            {"id": student[0], "name": student[1]}
            for student in students
        ])

    finally:
        connection.close()


# Start the application
if __name__ == "__main__":

    create_table()

    app.run(debug=True)
