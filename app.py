"""
This file contains the API endpoints for payment service.
"""
from flask import Flask, jsonify, request, send_file, render_template, send_from_directory
from connections.database import db
from db_models.payment import Payment
from datetime import datetime, timedelta
from payments.pix import Pix
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET'

db.init_app(app)
socketio = SocketIO(app)


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
    json response with the payment message
    """
    data = request.get_json()

    if 'bank_payment_id' not in data and 'value' not in data:
        return jsonify({'message': 'Invalid payment data'}), 400
    payment = Payment.query.filter_by(bank_payment_id=data['bank_payment_id']).first()

    if not payment or payment.paid:
        return jsonify({'message': 'Payment not found'}), 404

    if data.get('value') != payment.value:
        return jsonify({'message': 'Invalid payment value'}), 400

    payment.paid = True
    db.session.commit()
    socketio.emit(f'payment-confirmed-{payment.id}')
    return jsonify({'message': 'PIX payment has been confirmed successfully!'})


@app.route('/resources/<path:filename>')
def resources(filename):
    """
    Get a resource file.
    :param filename:
    :return:
    resource file
    """
    return send_from_directory('resources', filename)


@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def get_pix_payment(payment_id):
    """
    Get a PIX payment.
    :param payment_id:
    PIX payment id
    :return:
    json response with the PIX payment data
    """
    payment = Payment.query.get(payment_id)

    if payment is None:
        return render_template('404.html')

    if payment.paid:
        return render_template('confirmed_payment.html', payment_id=payment.id, value=payment.value)
    return render_template('payment.html',
                           payment_id=payment.id,
                           value=payment.value,
                           host='http://127.0.0.1:5000',
                           qrcode=payment.qr_code)


@socketio.on('connect')
def handle_connect():
    print('Client connected to the server')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected from the server')


if __name__ == '__main__':
    socketio.run(app, debug=True)
