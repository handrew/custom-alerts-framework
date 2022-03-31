"""Alerting functions."""

import os
from twilio.rest import Client


def twilio_alert(message):
    client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_AUTH"])
    twilio_from = os.environ["TWILIO_PHONE_FROM"]
    twilio_to = os.environ["TWILIO_PHONE_TO"]
    message = client.messages.create(body=message, from_=twilio_from, to=twilio_to)
