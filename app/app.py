from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "DevSecOps boyss daa  Application is Running!Hello from devsecops v2"

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
