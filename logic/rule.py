import time


class Rule:
    """Rule is a wrapper over a predicate function, a time function, and an
    alert function. It handles communications between the predicate fn and
    the alert fn..

    The predicate function takes the history of logs (for caching purposes)
    and tells you whether or not the alert should be triggered.

    The time function dictates how often the rule should be checked.

    The alert function dictates what should happen when the rule is triggered.
    """

    def __init__(self, rule_fn, time_fn, alert_fn):
        self.name = rule_fn.__name__.replace("_predicate_fn", "")
        self.predicate_fn = rule_fn
        self.time_fn = time_fn
        self.alert_fn = alert_fn
        self.last_triggered = []

    def is_time_yet_to_check(self):
        return self.time_fn(time.time())

    def is_triggered(self, **kwargs):
        is_triggered = self.predicate_fn(**kwargs)
        assert isinstance(is_triggered, dict), "Predicate function must return a dict."
        if is_triggered:
            self.last_triggered.append(int(time.time()))
        return is_triggered

    def alert(self, data={}):
        self.alert_fn(data=data)
