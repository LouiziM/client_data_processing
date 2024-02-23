from flask_sqlalchemy import SQLAlchemy
from controllers.clients import create_clients_blueprint
from controllers.purchase import create_purchase_blueprint
from controllers.service_history import create_service_history_blueprint
from controllers.satisfaction_surveys import create_satisfaction_surveys_blueprint
from controllers.marketing_campaigns import create_marketing_campaigns_blueprint
from flask import Flask, jsonify


def generate_database_structure(app, db):
    clients_blueprint = create_clients_blueprint(db)
    app.register_blueprint(clients_blueprint, url_prefix='/clients')

    purchase_blueprint = create_purchase_blueprint(db)
    app.register_blueprint(purchase_blueprint, url_prefix='/purchase')

    service_history_blueprint = create_service_history_blueprint(db)
    app.register_blueprint(service_history_blueprint, url_prefix='/service_history')

    satisfaction_surveys_blueprint = create_satisfaction_surveys_blueprint(db)
    app.register_blueprint(satisfaction_surveys_blueprint, url_prefix='/satisfaction_surveys')

    marketing_campaigns_blueprint = create_marketing_campaigns_blueprint(db)
    app.register_blueprint(marketing_campaigns_blueprint, url_prefix='/marketing_campaigns')

    @app.route('/generate_database', methods=['POST'])
    def generate_database():
        try:
            db.create_all()
            return jsonify({'message': 'Database structure generated successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500



generate_database_structure(app, db)

app.run(debug=True)
