from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

def create_clients_blueprint(db):
    clients_blueprint = Blueprint('clients', __name__)

    class Clients(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255), nullable=True)
        email = db.Column(db.String(255), nullable=True)
        phone = db.Column(db.String(20), nullable=True)
        address = db.Column(db.String(255), nullable=True)
        gender = db.Column(db.String(10), nullable=True)
        age = db.Column(db.Integer, nullable=True)
        profession = db.Column(db.String(255), nullable=True)

    @clients_blueprint.route('/add_client', methods=['POST'])
    def add_client():
        data = request.get_json()

        required_fields = ['name', 'email', 'phone', 'address', 'gender', 'age', 'profession']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'All required fields must be provided'}), 400

        new_client = Clients(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            address=data['address'],
            gender=data['gender'],
            age=data['age'],
            profession=data['profession']
        )

        try:
            db.session.add(new_client)
            db.session.commit()
            return jsonify({'message': 'Client added successfully'}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Client with this id already exists'}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @clients_blueprint.route('/update_client/<int:client_id>', methods=['PUT'])
    def update_client(client_id):
        data = request.get_json()

        try:
            client = Clients.query.get(client_id)
            if client:
                for key, value in data.items():
                    setattr(client, key, value)
                db.session.commit()
                return jsonify({'message': 'Client updated successfully'}), 200
            else:
                return jsonify({'error': 'Client not found'}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @clients_blueprint.route('/delete_client/<int:client_id>', methods=['DELETE'])
    def delete_client(client_id):
        try:
            client = Clients.query.get(client_id)
            if client:
                db.session.delete(client)
                db.session.commit()
                return jsonify({'message': 'Client deleted successfully'}), 200
            else:
                return jsonify({'error': 'Client not found'}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    return clients_blueprint
