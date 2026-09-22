from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
)
from json import dumps
from flask_socketio import SocketIO, join_room, emit 
from getraenkeabrechnung.backend.main import (
    get_families,
    get_image_for_user,
    get_drinks,
    get_image_for_drink,
    return_drink,
    get_price_for_drink,
    get_AdultTag,
    set_AdultTag
)

app = Flask(__name__)
socketio = SocketIO(app)

EVENT_NAME: str = "Info Linden"

@app.route("/", methods=["GET"])
def main():
    return render_template(
        "index.html",
        families=get_families(),
        get_image_for_user=get_image_for_user,
        name=None,
        event_name = EVENT_NAME
    )

@app.route("/user/<name>", methods=["GET"])
def get_user_page(name):
    return render_template("user.html", name=name, restriction=get_AdultTag(name), event_name=EVENT_NAME)

@app.route("/drinks/get/<name>", methods=["GET"])
def drinks(name):
    drinks: list[dict] = []
    for drink in get_drinks(restriction=not get_AdultTag(name)):
        drinks.append({
            "name": drink,
            "img_url": get_image_for_drink(drink),
            "price": get_price_for_drink(drink)
        })
    return render_template("components/drink_card.html", name=name, drinks=drinks, restriction=get_AdultTag(name), event_name=EVENT_NAME)

@socketio.on("connect")
def connect(auth=None):
    if auth and auth.get("name"):
        join_room(auth["name"])

@socketio.on("change_restriction")
def change_restriction(data):
    set_AdultTag(data["name"])
    emit("restriction_change", {"name": data["name"], "restriction": get_AdultTag(data["name"])}, to=data["name"])

@socketio.on("buy_drink")
def buy_drink(data):
    print(data)
    return_drink(data["name"], data["drink"])
    emit("buy_successful", {}, to=data["name"])

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
