from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
)
from getraenkeabrechnung.backend.main import (
    get_families,
    get_image_for_user,
    get_drinks,
    get_image_for_drink,
    return_drink,
    get_price_for_drink,
    get_AdultTag
)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    return render_template(
        "index.html",
        families=get_families(),
        get_image_for_user=get_image_for_user,
        name=None
    )

@app.route("/user/<name>", methods=["GET"])
def user(name):
    drinks: list[dict] = []
    for drink in get_drinks(restriction=not get_AdultTag(name)):
        drinks.append({
            "name": drink,
            "img_url": get_image_for_drink(drink),
            "price": get_price_for_drink(drink)
        })
    return render_template("user.html", name=name, drinks=drinks, restriction=get_AdultTag(name))

@app.route("/user/<name>/drink/<drink>", methods=["POST"])
def return_drink_route(name, drink):
    return_drink(name, drink)
    return redirect(url_for("user", name=name))

@app.route("/api/<name>/restriction", methods=["POST"])
def change_restriction(name):
    print(request.form.get("toggle"))
    return 200

if __name__ == "__main__":
    app.run("0.0.0.0", port=8000, debug=True)
