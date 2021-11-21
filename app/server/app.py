from flask import Flask, request
from pymongo import MongoClient
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import json
from flask import render_template
from bson import ObjectId
import logging
import os

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app_env = os.environ.get("APP_ENV")
    logger = logging.getLogger(app_env) 
    secret_key = os.environ.get("SECRETKEY")
    mongodb = {}
    mongodb["username"] = os.environ.get("MONGODB_USERNAME")
    mongodb["password"] = os.environ.get("MONGODB_PASSWORD")
    mongodb["hostname"] = os.environ.get("MONGODB_HOSTNAME")
    mongodb["urlsuffix"] = os.environ.get("MONGODB_URL_SUFFIX")
    mongodb["dbname"] = os.environ.get("contactdb")

    mongo_uri = "mongodb://"+mongodb["username"]+":"+mongodb["password"]+"@"+mongodb["hostname"]+":27017/contactdb?"+mongodb["urlsuffix"]
    #mongo_uri = "mongodb://admin:password@mongodb:27017/contactdb?authSource=contactdb"
    #os.environ['MONGOURI'] = mongo_uri
    logger.info(mongo_uri)
    app.config.from_mapping(
        SECRET_KEY=secret_key,
        MONGO_DBNAME = mongodb["dbname"],
        MONGO_URI = mongo_uri
    )

    """Try connecting to mongoDB"""
    try:
        mongodb_client = PyMongo(app)
        db = mongodb_client.db
        logger.info("Succesfully connected to MongoDB!")
    except Exception as e:
        logger.error("Could not connect to Mongo.\nException seen:" + str(e))

    if not app_env == "test":
        contact_db = db.contacts
    else:
        contact_db = db.test_contacts

    """ Add a new contact """
    @app.route('/person/<string:id>', methods=['POST'])
    def add_contact(id):
        if not request.data:
            return jsonify(message="The request is not in a json type..")
        if not 'name' in request.json or not 'number' in request.json or not 'city' in request.json:
            return jsonify(message="Some details are missing. Fill them and try again.")
        contact = contact_db.find_one({"id": id})
        if contact:
            return jsonify(message="Contact with such ID already exist.")
        contact_db.insert_one({'id': id, 'name': request.json['name'], 'number':request.json['number'], 'city': request.json['city']})
        logging.info("Succesfully added new contact: " + id )
        return jsonify(message="New contact added succesfully!!")

    """ Update an existing contact """
    @app.route('/person/<string:id>', methods=['PUT'])
    def update_contact(id):
        contact = contact_db.find_one({'id': id})
        updated_contact = {}
        if contact:
            updated_contact['id'] = contact['id']
            if 'name' in request.json:
                updated_contact['name'] = request.json['name']
            else:
                updated_contact['name'] = contact['name']

            if 'number' in request.json:
                updated_contact['number'] = request.json['number']
            else:
                updated_contact['number'] = contact["number"]

            if 'city' in request.json:
                updated_contact['city'] = request.json['city']
            else:
                updated_contact['city'] = contact['city']
        
            result = contact_db.replace_one({'id': id}, updated_contact)
            logging.info("Succesfully updated contact :" + id )
            return jsonify(message="Contact updated succesfully!")
        else:
            return jsonify(message="No such contact. Enter id again")


    """ Delete an existing contact """
    @app.route('/person/<string:id>', methods=['DELETE'])
    def delete_contact(id):
        contact = contact_db.find_one({'id': id})
        if contact:
            deleted_contact = contact_db.delete_one({'id': id})
            logging.info("Succesfully deleted contact :" + id )
            return jsonify(message="Contact deleted succesfully")
        else:
            return jsonify(message="Contact with such ID is not exist") 


    """ Get all contacts """
    @app.route('/person', methods=['GET'])
    def get_all_contacts():
        contacts = contact_db.find()
        contacts_list = []
        for contact in contacts:
            contacts_list.append(JSONEncoder().encode(contact))
        return jsonify(contacts_list)


    """ Get contact with a given ID """
    @app.route('/person/<string:id>', methods=['GET'])
    def get_person(id):
        contact = contact_db.find_one({"id": id})
        if contact:
            return JSONEncoder().encode(contact)
        else:
            return jsonify(message="Contact with such ID is not exist.")


    """ Welcome """
    @app.route('/', methods=['GET'])
    def index():
        return render_template("index.html")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')