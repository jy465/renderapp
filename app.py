import os
from flask import Flask, render_template, request, redirect
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL,
            priority VARCHAR(10) DEFAULT 'medium',
            done BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def index():
    app_name = os.environ.get("APP_NAME", "FocusFlow")
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM todos ORDER BY created_at DESC")
    todos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", todos=todos, app_name=app_name)

@app.route("/add", methods=["POST"])
def add():
    item = request.form.get("item", "").strip()
    priority = request.form.get("priority", "medium")
    if item:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO todos (task, priority) VALUES (%s, %s)", (item, priority))
        conn.commit()
        cur.close()
        conn.close()
    return redirect("/")

@app.route("/toggle/<int:todo_id>")
def toggle(todo_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE todos SET done = NOT done WHERE id = %s", (todo_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))