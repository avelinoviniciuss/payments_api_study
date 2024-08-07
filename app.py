"""
This file contains the API endpoints for payment service.
"""
from flask import Flask, jsonify, request, send_file
from connections.database import db
from db_models.payment import Payment
from datetime import datetime, timedelta
from payments.pix import Pix

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET'

db.init_app(app)


@app.route('/payments/pix', methods=['POST'])
def create_pix_payment():
    """
    Create a new PIX payment.
    :return:
    json response with the creation message
    """
    data = request.get_json()

    if 'value' not in data:
        return jsonify({'error': 'value is required'}), 400

    expiration_date = datetime.now() + timedelta(minutes=30)
    new_payment = Payment(value=data['value'], expiration_date=expiration_date)
    pix = Pix()
    data_payment_pix = pix.create_payment()
    new_payment.bank_payment_id = data_payment_pix['bank_payment_id']
    new_payment.qr_code = data_payment_pix['qr_code_path']
    db.session.add(new_payment)
    db.session.commit()

    return jsonify({'message': 'PIX payment has been created successfully!',
                    'payment': new_payment.to_dict()})


@app.route('/payments/pix/qr_code/<file_name>', methods=['GET'])
def get_qr_code(file_name):
    """
    Get a QR code.
    :param file_name:
    QR code file name
    :return:
    QR code image
    """
    return send_file(f'resources/img/{file_name}.png', mimetype='image/png')


@app.route('/payments/pix/confirmation', methods=['POST'])
def confirm_pix_payment():
    """
    Confirm a PIX payment.
    :return:
    json response with the confirmation message
    """
    return jsonify({'PIX payment has been confirmed successfully!'})


@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def get_pix_payment(payment_id):
    """
    Get a PIX payment.
    :param payment_id:
    PIX payment id
    :return:
    json response with the PIX payment data
    """
    return jsonify({'payment_id': payment_id, 'status': 'paid'})


if __name__ == '__main__':
    app.run(debug=True)
