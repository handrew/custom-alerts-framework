"""
This is where the custom alert logic goes.

See the `rule.py` definition of the `Rule` object. Each Rule must consist of
both a predicate function, a time function, and an alert function.

Predicate functions take kwargs `logs`, which is a dataframe of last times
that the function was triggered.
"""
import inspect
import requests


