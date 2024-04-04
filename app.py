from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import urllib
from controllers.customers import create_customers_blueprint


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///?odbc_connect={}'.format(urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-LILEUDB\\SQLEXPRESS;DATABASE=CDP;UID=master;PWD=louizi'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    customers_blueprint = create_customers_blueprint(db)
    app.register_blueprint(customers_blueprint, url_prefix='/customers')

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
