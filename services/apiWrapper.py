from yookassa import Configuration, Payment
from services.bdWrapper import *
import json
from config import *

Configuration.account_id = get_setting(15)
Configuration.secret_key = get_setting(14)


def create_payment_link(amount, email):
    payment = Payment.create({
        "amount": {
            "value": str(amount),
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": None
        },
        "receipt": {
            'customer': {
                'email': email
            },
            'items': [{
                'description': get_setting(17),
                "amount": {
                    "value": str(amount),
                    'currency': "RUB"
                },
                "vat_code": 1,
                'quantity': 1
            }]
        },
        "capture": True,
        "description": get_setting(16)
    })
    payment_data = json.loads(payment.json())
    payment_id = payment_data['id']
    payment_url = (payment_data['confirmation'])['confirmation_url']
    return payment_id, payment_url


def check_payment(payment_id):
    payment = json.loads((Payment.find_one(payment_id)).json())
    try:
        return payment['status'] == 'succeeded'
    except Exception:
        return False
