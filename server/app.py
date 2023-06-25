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

class Plants(Resource):
       def get(self):
        plants = Plant.query.all()
        serialized_plants = [plant.serialize() for plant in plants]
        return serialized_plants 
        
       def post(self):
        data = request.get_json()
        plant = Plant(name=data['name'], image=data['image'], price=data['price'])
        db.session.add(plant)
        db.session.commit()
        return plant.serialize(), 201

api.add_resource(Plants, '/plants') 
        

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if plant is None:
            return {'error': 'Plant not found'}, 404
        return plant.serialize()

api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
