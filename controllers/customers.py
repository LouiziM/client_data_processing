from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict


def create_customers_blueprint(db):
    customers_blueprint = Blueprint('customer', __name__)

    class Customer(db.Model):
        __tablename__ = 'A_CUSTOMER'
        CUSTNO = db.Column(db.Integer, primary_key=True)
        NAME2 = db.Column(db.String(255))
        FIRSTNAME = db.Column(db.String(255))
        ADDRESS = db.Column(db.String(255))
        ZIP = db.Column(db.String(50))
        CITY = db.Column(db.String(255))
        COUNTRY = db.Column(db.String(255))
        BIRTHDATE = db.Column(db.Date)
        PHONE = db.Column(db.String(20))
        PHONEPRI = db.Column(db.String(20))
        EMAIL = db.Column(db.String(255))
        FAX = db.Column(db.String(20))
        CIVILITY = db.Column(db.String(20))
        DATECRE = db.Column(db.Date)
        TYPECUST = db.Column(db.String(255))
        TYPECUST2 = db.Column(db.String(255))
        ICE = db.Column(db.String(255))
        CIN = db.Column(db.String(255))
        INTERGROUPE = db.Column(db.String(255))
        SITE = db.Column(db.String(255))
        REGION = db.Column(db.String(255))
        GENDER = db.Column(db.String(10))
        NATIONALITY = db.Column(db.String(255))
        isFormatted = db.Column(db.Boolean)
        isImputed = db.Column(db.Boolean)
        LIBSITE = db.Column(db.String(255))

    contact_fields = ['BIRTHDATE', 'PHONE', 'PHONEPRI', 'EMAIL', 'FAX']
    demographic_fields = ['CIVILITY', 'GENDER', 'NATIONALITY', 'CIN']
    geographic_fields = ['SITE', 'REGION', 'ADDRESS', 'ZIP', 'CITY', 'COUNTRY']

    def calculate_ratio(customer, fields):
        total_fields = len(fields)
        filled_fields = sum(1 for field in fields if getattr(customer, field))
        return (filled_fields / total_fields) * 100 if total_fields != 0 else 0

    @customers_blueprint.route('/completion/<int:custno>', methods=['GET'])
    def get_customer_completion(custno):
        try:
            customer = Customer.query.filter_by(CUSTNO=custno).first()
            if customer:
                # Calculate ratios
                contact_ratio = round(calculate_ratio(customer, contact_fields), 2)
                demographic_ratio = round(calculate_ratio(customer, demographic_fields), 2)
                geographic_ratio = round(calculate_ratio(customer, geographic_fields), 2)

                # Find missing fields
                missing_contact_fields = [field for field in contact_fields if not getattr(customer, field)]
                missing_demographic_fields = [field for field in demographic_fields if not getattr(customer, field)]
                missing_geographic_fields = [field for field in geographic_fields if not getattr(customer, field)]

                return jsonify({
                    'Contact': {
                        'Completion Ratio': contact_ratio,
                        'Missing Fields': missing_contact_fields
                    },
                    'Situation démographique': {
                        'Completion Ratio': demographic_ratio,
                        'Missing Fields': missing_demographic_fields
                    },
                    'Situation géographique': {
                        'Completion Ratio': geographic_ratio,
                        'Missing Fields': missing_geographic_fields
                    }
                }), 200
            else:
                return jsonify({'error': 'Customer not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @customers_blueprint.route('/customer-count-by-region', methods=['GET'])
    def get_customer_count_by_region():
        try:
            region_counts = defaultdict(int)
            customers = Customer.query.all()
            for customer in customers:
                region = customer.REGION
                if region is not None:
                    region_counts[region] += 1

            region_ids = {
                "Dakhla-Oued Eddahab": 11,
                "Tanger-Tetouan-Hoceima": 3,
                "Marrakech-Safi": 12,
                "Daraa-Tafilelt": 8,
                "Guelmim-Oued Noun": 10,
                "Fes-Meknes": 4,
                "Oriental": 2,
                "Casablanca-Settat": 6,
                "Souss Massa": 9,
                "Laayoune-Saguia Hamra": 1,
                "Rabat-Sale-Kenitra": 5,
                "Beni Mellal-Khenifra": 7
            }
            result = [{"id": region_ids[region], "value": count} for region, count in region_counts.items()]

            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return customers_blueprint
