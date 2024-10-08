"""
    This module is responsible for the implementation of the PIX payment method.
"""

import uuid
from typing import Dict

import qrcode


class Pix:
    def __init__(self):
        pass

    @staticmethod
    def create_payment(base_dir:str = "") -> Dict[str, str]:
        """
        Create a new PIX payment.
        :param base_dir:
        base directory to save the QR code image
        :return:
        payment data
        """
        bank_payment_id = str(uuid.uuid4())
        hash_payment = f'hash_payment_{bank_payment_id}'
        img = qrcode.make(hash_payment)
        img.save(f'{base_dir}/resources/img/qr_code_payment_{bank_payment_id}.png')
        return {"bank_payment_id": bank_payment_id,
                "qr_code_path": f"qr_code_payment_{bank_payment_id}"}
