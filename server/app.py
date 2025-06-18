#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants]), 200

@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return make_response({"error": "Plant not found"}, 404)
    return jsonify(plant.to_dict()), 200
@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()
    
    try:
        name = data['name']
        image = data['image']
        price = data['price']
    except KeyError:
        return make_response({"error": "Missing required fields"}, 400)

    new_plant = Plant(name=name, image=image, price=price)
    
    db.session.add(new_plant)
    db.session.commit()

    return jsonify(new_plant.to_dict()), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)
