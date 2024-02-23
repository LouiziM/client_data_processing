from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

def create_satisfaction_surveys_blueprint(db):
    satisfaction_surveys_blueprint = Blueprint('satisfaction_surveys', __name__)

    class SatisfactionSurveys(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
        survey_date = db.Column(db.Date, nullable=True)
        score = db.Column(db.Integer, nullable=True)
        comments = db.Column(db.Text, nullable=True)

    @satisfaction_surveys_blueprint.route('/add_satisfaction_survey', methods=['POST'])
    def add_satisfaction_survey():
        data = request.get_json()

        required_fields = ['client_id', 'survey_date', 'score', 'comments']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'All required fields must be provided'}), 400

        new_satisfaction_survey = SatisfactionSurveys(
            client_id=data['client_id'],
            survey_date=data['survey_date'],
            score=data['score'],
            comments=data['comments']
        )

        try:
            db.session.add(new_satisfaction_survey)
            db.session.commit()
            return jsonify({'message': 'Satisfaction survey added successfully'}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Satisfaction survey with this id already exists'}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @satisfaction_surveys_blueprint.route('/update_satisfaction_survey/<int:survey_id>', methods=['PUT'])
    def update_satisfaction_survey(survey_id):
        data = request.get_json()

        try:
            survey = SatisfactionSurveys.query.get(survey_id)
            if survey:
                for key, value in data.items():
                    setattr(survey, key, value)
                db.session.commit()
                return jsonify({'message': 'Satisfaction survey updated successfully'}), 200
            else:
                return jsonify({'error': 'Satisfaction survey not found'}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @satisfaction_surveys_blueprint.route('/delete_satisfaction_survey/<int:survey_id>', methods=['DELETE'])
    def delete_satisfaction_survey(survey_id):
        try:
            survey = SatisfactionSurveys.query.get(survey_id)
            if survey:
                db.session.delete(survey)
                db.session.commit()
                return jsonify({'message': 'Satisfaction survey deleted successfully'}), 200
            else:
                return jsonify({'error': 'Satisfaction survey not found'}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    return satisfaction_surveys_blueprint
