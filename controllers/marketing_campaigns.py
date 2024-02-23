from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

def create_marketing_campaigns_blueprint(db):
    marketing_campaigns_blueprint = Blueprint('marketing_campaigns', __name__)

    class MarketingCampaigns(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
        campaign_name = db.Column(db.String(255), nullable=True)
        participation_status = db.Column(db.String(20), nullable=True)
        conversion_status = db.Column(db.String(20), nullable=True)
        response_date = db.Column(db.Date, nullable=True)

    @marketing_campaigns_blueprint.route('/add_marketing_campaign', methods=['POST'])
    def add_marketing_campaign():
        data = request.get_json()

        required_fields = ['client_id', 'campaign_name', 'participation_status', 'conversion_status', 'response_date']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'All required fields must be provided'}), 400

        new_marketing_campaign = MarketingCampaigns(
            client_id=data['client_id'],
            campaign_name=data['campaign_name'],
            participation_status=data['participation_status'],
            conversion_status=data['conversion_status'],
            response_date=data['response_date']
        )

        try:
            db.session.add(new_marketing_campaign)
            db.session.commit()
            return jsonify({'message': 'Marketing campaign added successfully'}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Marketing campaign with this id already exists'}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @marketing_campaigns_blueprint.route('/update_marketing_campaign/<int:campaign_id>', methods=['PUT'])
    def update_marketing_campaign(campaign_id):
        data = request.get_json()

        try:
            marketing_campaign = MarketingCampaigns.query.get(campaign_id)
            if marketing_campaign:
                for key, value in data.items():
                    setattr(marketing_campaign, key, value)
                db.session.commit()
                return jsonify({'message': 'Marketing campaign updated successfully'}), 200
            else:
                return jsonify({'error': 'Marketing campaign not found'}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @marketing_campaigns_blueprint.route('/delete_marketing_campaign/<int:campaign_id>', methods=['DELETE'])
    def delete_marketing_campaign(campaign_id):
        try:
            marketing_campaign = MarketingCampaigns.query.get(campaign_id)
            if marketing_campaign:
                db.session.delete(marketing_campaign)
                db.session.commit()
                return jsonify({'message': 'Marketing campaign deleted successfully'}), 200
            else:
                return jsonify({'error': 'Marketing campaign not found'}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    return marketing_campaigns_blueprint
