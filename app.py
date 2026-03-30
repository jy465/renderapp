from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello from Render!</h1><p>My first Render deployment by Jia Yi</p>"

if __name__ == "__main__":
    app.run()