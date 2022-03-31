"""Scheduler abstraction."""
import time
import datetime
import pandas as pd


class Scheduler:
    """Scheduler takes in a set of `Rule`s, manages the state that needs to
    be given as input, and also manages their output. By default it will poll
    every `poll_every` seconds, so depending on latency that can be adjusted."""

    def __init__(self, list_of_rules, poll_every=1, dont_bother_for=5 * 60):
        super(Scheduler, self).__init__()
        self.poll_every = poll_every
        self.rules = list_of_rules
        self.state = pd.DataFrame(columns=["timestamp", "rule", "triggered"])
        self.dont_bother_for = dont_bother_for

    def log_rule(self, rule, result):
        timestamp = int(time.time())
        new_row = pd.DataFrame(
            [{"timestamp": timestamp, "rule": rule.name, "triggered": result}]
        )
        self.state = pd.concat([self.state, new_row])

    def _get_last_time_rule_was_alerted(self, rule):
        if self.state.empty:
            return
        last_time = self.state[self.state["rule"] == rule.name].timestamp.iloc[-1]
        return last_time

    def run(self):
        """Main entrypoint."""
        while True:
            time.sleep(self.poll_every)
            for rule in self.rules:

                if rule.is_time_yet_to_check():
                    rule_is_triggered = rule.is_triggered(logs=self.state)

                    if rule_is_triggered:
                        # Trigger the alert.
                        last_time = self._get_last_time_rule_was_alerted(rule)
                        if (
                            last_time
                            and time.time() - last_time <= self.dont_bother_for
                        ):
                            print("Don't bother sending an alert. Too soon!")
                            continue

                        print("Rule {} was triggered! Alerting.".format(rule.name))
                        rule.alert()

                        # Log the alert.
                        self.log_rule(rule, rule_is_triggered)
