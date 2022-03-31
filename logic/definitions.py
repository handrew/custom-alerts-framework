"""
This is where the custom alert logic goes.

See the `rule.py` definition of the `Rule` object. Each Rule must consist of
both a predicate function, a time function, and an alert function.

Predicate functions take kwargs `logs`, which is a dataframe of last times
that the function was triggered.
"""
import inspect
import requests


"""
Gas price is high (>200 wei) rule.
"""


def gas_price_is_high_predicate_fn(**kwargs):
    resp = requests.get("https://api.gasprice.io/v1/estimates").json()
    estimated_fee = resp["result"]["fast"]["feeCap"]
    return estimated_fee > 200


def gas_price_is_high_time_fn(curr_time):
    """Every 5 min."""
    return int(curr_time) % (5 * 60) == 0


def gas_price_is_high_alert_fn():
    from .alerts import twilio_alert
    twilio_alert("Alert: ETH gas price is high! (>200)")


"""
ETH price is above $3300.
"""


def eth_price_is_high_predicate_fn(**kwargs):
    resp = requests.get("https://api.gasprice.io/v1/estimates").json()
    eth_price = resp["result"]["ethPrice"]
    return eth_price > 3300


def eth_price_is_high_time_fn(curr_time):
    """Every 5 min."""
    return int(curr_time) % 5 == 0


def eth_price_is_high_alert_fn():
    from .alerts import twilio_alert
    twilio_alert("Handrew alert: ETH price is high! (>3300)")