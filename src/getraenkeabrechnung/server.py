from flask import (
    Flask,
    render_template,
    request,
    jsonify
)
from getraenkeabrechnung.backend.main import get_image_for_user

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    families = ["Jung", "JungJunior", "Schuimer"]
    return render_template(
        "index.html",
        families=families,
        get_image_for_user=get_image_for_user,
    )

@app.route("/user/", methods=["GET"])
def user():
    return render_template("user.html")

if __name__ == "__main__":
    app.run("0.0.0.0", port=8000, debug=True)
