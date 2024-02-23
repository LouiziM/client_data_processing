from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

def create_purchase_blueprint(db):
    purchase_blueprint = Blueprint('purchase', __name__)

    class Purchase(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
        model = db.Column(db.String(255), nullable=True)
        year = db.Column(db.Integer, nullable=True)
        brand = db.Column(db.String(255), nullable=True)
        purchase_type = db.Column(db.String(20), nullable=True)
        amount_spent = db.Column(db.Float, nullable=True)
        purchase_date = db.Column(db.Date, nullable=True)

    @purchase_blueprint.route('/add_purchase', methods=['POST'])
    def add_purchase():
        data = request.get_json()

        required_fields = ['client_id', 'model', 'year', 'brand', 'purchase_type', 'amount_spent', 'purchase_date']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'All required fields must be provided'}), 400

        new_purchase = Purchase(
            client_id=data['client_id'],
            model=data['model'],
            year=data['year'],
            brand=data['brand'],
            purchase_type=data['purchase_type'],
            amount_spent=data['amount_spent'],
            purchase_date=data['purchase_date']
        )

        try:
            db.session.add(new_purchase)
            db.session.commit()
            return jsonify({'message': 'Purchase added successfully'}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Purchase with this id already exists'}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @purchase_blueprint.route('/update_purchase/<int:purchase_id>', methods=['PUT'])
    def update_purchase(purchase_id):
        data = request.get_json()

        try:
            purchase = Purchase.query.get(purchase_id)
            if purchase:
                for key, value in data.items():
                    setattr(purchase, key, value)
                db.session.commit()
                return jsonify({'message': 'Purchase updated successfully'}), 200
            else:
                return jsonify({'error': 'Purchase not found'}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @purchase_blueprint.route('/delete_purchase/<int:purchase_id>', methods=['DELETE'])
    def delete_purchase(purchase_id):
        try:
            purchase = Purchase.query.get(purchase_id)
            if purchase:
                db.session.delete(purchase)
                db.session.commit()
                return jsonify({'message': 'Purchase deleted successfully'}), 200
            else:
                return jsonify({'error': 'Purchase not found'}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    return purchase_blueprint
