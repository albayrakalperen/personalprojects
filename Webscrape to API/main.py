from random import choice
from csv_to_db import CSVtoDB
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///website.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)

print(db.engine.table_names())


class Steam(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(250), unique=True, nullable=False)
    current_player = db.Column(db.String(250), nullable=False)
    peak_24h = db.Column(db.String(250), nullable=False)
    all_time_peak = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random_game():
    csvtodb = CSVtoDB()
    csvtodb.create_database()
    all_games = db.session.query(Steam).all()
    random_game = choice(all_games)
    print(random_game.to_dict())
    return jsonify(game={
        "id": random_game.game_id,
        "name": random_game.game_name,
        "current_player": random_game.current_player,
        "peak_24h": random_game.peak_24h,
        "all_time_peak": random_game.all_time_peak
    })


@app.route("/all")
def get_all_games():
    csvtodb = CSVtoDB()
    csvtodb.create_database()
    all_games = db.session.query(Steam).all()
    return jsonify(game=[game.to_dict() for game in all_games])


@app.route("/search")
def get_searched_game():
    game_name = request.args.get("name", type=str)
    games = Steam.query.filter_by(game_name=game_name)
    if games.first():
        return jsonify(game=[game.to_dict() for game in games])

    return jsonify(error="No game found")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    
