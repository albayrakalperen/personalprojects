from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

print(db.engine.table_names())

##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


class Auth(db.Model):
    key = db.Column(db.String(50), primary_key=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    all_cafes = db.session.query(Cafe).all()
    random_cafe = choice(all_cafes)
    # print(random_cafe.to_dict())
    return jsonify(cafe={
        "name": random_cafe.name,
        "map_url": random_cafe.map_url,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,
        "seats": random_cafe.seats,
        "has_toilet": random_cafe.has_toilet,
        "has_wifi": random_cafe.has_wifi,
        "has_sockets": random_cafe.has_sockets,
        "can_take_calls": random_cafe.can_take_calls,
        "coffee_price": random_cafe.coffee_price
    })


@app.route("/all")
def get_all_cafes():
    all_cafes = db.session.query(Cafe).all()
    return jsonify(cafe=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def get_searched_cafe():
    cafe_location = request.args.get("loc", type=str)
    cafes_in_location = Cafe.query.filter_by(location=cafe_location)
    print(type(Cafe.query.filter_by(location=cafe_location)))
    if cafes_in_location.first():
        return jsonify(cafe=[cafe.to_dict() for cafe in cafes_in_location])

    return jsonify(error="No cafe found")


@app.route("/add", methods=["POST"])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        seats=request.form.get("seats"),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        has_sockets=bool(request.form.get("has_sockets")),
        can_take_calls=bool(request.form.get("can_take_calls")),
        coffee_price=bool(request.form.get("coffee_price"))
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Succesfully added the new cafe."})


@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    # new_price = request.args.get("coffee_price")
    # cafe_to_update = Cafe.query.filter_by(id=cafe_id).update({"coffee_price": new_price})
    # db.session.commit()
    try:
        cafe = db.session.query(Cafe).get(cafe_id)
        print(cafe)
        cafe.coffee_price = request.args.get("new_price")
        db.session.commit()
    except AttributeError:
        return jsonify(response={"error": "Undefined id!"}), 404
    else:
        return jsonify(response={"success": "Price updated succesfully."}), 200


@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    cafe = db.session.query(Cafe).get(cafe_id)
    keys = [i.key for i in db.session.query(Auth).all()]
    key_input = request.args.get("api_key")
    if key_input not in keys:
        return jsonify(response={"error": "That's not allowed!"})
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(response={"success": f"{cafe.name} deleted. "}), 200

    return jsonify(response={"error": "Undefined id!"}), 404


if __name__ == '__main__':
    app.run(debug=True)
