from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
import time

app = Flask(__name__)

def get_db():
    retries = 5
    while retries:
        try:
            conn = mysql.connector.connect(
                host=os.environ.get("DB_HOST", "db"),
                user=os.environ.get("DB_USER", "hassan"),
                password=os.environ.get("DB_PASSWORD", "hasni123"),
                database=os.environ.get("DB_NAME", "taskboard")
            )
            return conn
        except mysql.connector.Error:
            retries -= 1
            time.sleep(3)
    raise Exception("Could not connect to database")

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status ENUM('pending', 'done') DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/")
def index():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    description = request.form.get("description")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("index"))

@app.route("/toggle/<int:task_id>")
def toggle_task(task_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = IF(status='pending','done','pending') WHERE id=%s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
