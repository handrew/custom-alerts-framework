"""Scheduler abstraction."""
import time
import datetime
import pandas as pd


class Scheduler:
    """Scheduler takes in a set of `Rule`s, manages the state that needs to
    be given as input, and also manages their output. By default it will poll
    every `poll_every` seconds, so depending on latency that can be adjusted."""

    def __init__(self, list_of_rules, poll_every=1):
        super(Scheduler, self).__init__()
        self.poll_every = poll_every
        self.rules = list_of_rules
        self.state = pd.DataFrame(columns=["time", "rule", "triggered"])

    def log_rule(self, rule, result):
    	timestamp = int(time.time())
    	self.state = pd.concat(
    		self.state, [
    			{"time": timestamp, "rule": rule.name, "triggered": result}
    		]
    	)

    def run(self):
        """Main entrypoint."""
        while True:
            time.sleep(self.poll_every)
            for rule in self.rules:
                
                if rule.is_time_yet_to_check():
                	rule_is_triggered = rule.is_triggered(self.state)

                	if rule_is_triggered:
	                    # Trigger the alert.
	                    rule.alert()

	                    # Log the alert.
	                    self.log_rule(rule, rule_is_triggered)
	                    
