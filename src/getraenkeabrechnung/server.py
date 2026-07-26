from flask import (
    Flask,
    render_template,
    request,
    jsonify
)
from getraenkeabrechnung.backend.main import *

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    return render_template(
        "index.html",
        families=get_families(),
        get_image_for_user=get_image_for_user,
    )

@app.route("/user/<name>", methods=["GET"])
def user(name):
    return render_template(
        "user.html",
        name=name,
        drinks=get_drinks(),
        get_image_for_drink=get_image_for_drink,
    )

if __name__ == "__main__":
    app.run("0.0.0.0", port=8000, debug=True)
