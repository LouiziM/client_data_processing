# service_history.py
from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

def create_service_history_blueprint(db):
    service_history_blueprint = Blueprint('service_history', __name__)

    class ServiceHistory(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
        visit_date = db.Column(db.Date, nullable=True)
        service_type = db.Column(db.String(255), nullable=True)
        amount_spent = db.Column(db.Float, nullable=True)
        satisfaction = db.Column(db.Integer, nullable=True)

    @service_history_blueprint.route('/add_service_history', methods=['POST'])
    def add_service_history():
        data = request.get_json()

        required_fields = ['client_id', 'visit_date', 'service_type', 'amount_spent', 'satisfaction']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'All required fields must be provided'}), 400

        new_service_history = ServiceHistory(
            client_id=data['client_id'],
            visit_date=data['visit_date'],
            service_type=data['service_type'],
            amount_spent=data['amount_spent'],
            satisfaction=data['satisfaction']
        )

        try:
            db.session.add(new_service_history)
            db.session.commit()
            return jsonify({'message': 'Service history added successfully'}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Service history with this id already exists'}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @service_history_blueprint.route('/update_service_history/<int:service_history_id>', methods=['PUT'])
    def update_service_history(service_history_id):
        data = request.get_json()

        try:
            service_history = ServiceHistory.query.get(service_history_id)
            if service_history:
                for key, value in data.items():
                    setattr(service_history, key, value)
                db.session.commit()
                return jsonify({'message': 'Service history updated successfully'}), 200
            else:
                return jsonify({'error': 'Service history not found'}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @service_history_blueprint.route('/delete_service_history/<int:service_history_id>', methods=['DELETE'])
    def delete_service_history(service_history_id):
        try:
            service_history = ServiceHistory.query.get(service_history_id)
            if service_history:
                db.session.delete(service_history)
                db.session.commit()
                return jsonify({'message': 'Service history deleted successfully'}), 200
            else:
                return jsonify({'error': 'Service history not found'}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    return service_history_blueprint
