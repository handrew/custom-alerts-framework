"""Scheduler abstraction."""
import datetime
import pandas as pd
from inspect import getmembers, isfunction
from .definitions import *


class Scheduler():
	"""Scheduler takes in a set of `Rule`s, manages the state that needs to
	be given as input, and also manages their output."""
	def __init__(self):
		super(Scheduler, self).__init__()
		self.state = None  # Will be a pandas DataFrame.

	def run(self):
		"""Main entrypoint."""
		pass
		
