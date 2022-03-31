# Custom Alerts Framework

Meant to be a lightweight script you can just run continuously on a cloud instance, check things you want to check, and then send you a text when some arbitrarily defined logic resolves to `True`. Just makes it easier than running a bunch of cronjobs.

## Instructions

On a cloud instance, you could: 

0. Change `requirements.txt` to fit your needs, if you plan to write custom rules.
1. Set up a virtual environment and then run `pip install -r requirements.txt`. 
2. Define a `.env` file with `TWILIO_SID`, `TWILIO_AUTH`, `TWILIO_PHONE_FROM`, `TWILIO_PHONE_TO`, and any other secrets you have.
3. Write rules in `logic/definitions.py`.
4. Run `python main.py run`.

## Architecture

The ontology is as follows. 

The `Scheduler` accepts a list of `Rule`s and increments time forward. Each `Rule` has a `predicate_fn`, a `time_fn`, and an `alert_fn`. At each time step, the `Scheduler` asks each Rule if it is time (via `time_fn`) to check the rule (`predicate_fn`). If the `predicate_fn` returns true, and `dont_bother_for` seconds has elapsed, then `alert_fn` is called.

That's it.