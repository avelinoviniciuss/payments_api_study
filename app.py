"""
This file contains the API endpoints for payment service.
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/payments/pix', methods=['POST'])
def create_pix_payment():
    """
    Create a new PIX payment.
    :return:
    json response with the creation message
    """
    return jsonify({'PIX payment has been created successfully!'})


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
