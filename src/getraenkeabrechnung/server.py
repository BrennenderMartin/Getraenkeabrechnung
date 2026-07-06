from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")

app.run("0.0.0.0", port=5000, debug=True)

"""
INSERT INTO user(userID, Name) values (0, "Jung");
INSERT INTO user(userID, Name) values (1, "Schuimer");
"""