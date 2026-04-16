import os
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

todos = []

@app.route("/")
def index():
    app_name = os.environ.get("APP_NAME", "Focus")
    return render_template("index.html", todos=todos, app_name=app_name)

@app.route("/add", methods=["POST"])
def add():
    item = request.form.get("item")
    priority = request.form.get("priority", "medium")
    if item:
        todos.append({"task": item, "priority": priority, "done": False})
    return redirect("/")

@app.route("/toggle/<int:index>")
def toggle(index):
    if 0 <= index < len(todos):
        todos[index]["done"] = not todos[index]["done"]
    return redirect("/")

@app.route("/delete/<int:index>")
def delete(index):
    if 0 <= index < len(todos):
        todos.pop(index)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))