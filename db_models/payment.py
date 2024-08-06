"""
Payment database model.
"""
from connections.database import db


class Payment(db.Model):
    """
    Payment model.
    :param db.Model:
    SQLAlchemy model class.
    """
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    paid = db.Column(db.Boolean, default=False)
    bank_payment_id = db.Column(db.Integer, nullable=True)
    qr_code = db.Column(db.String(100), nullable=True)
    expiration_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Payment {self.id}>'