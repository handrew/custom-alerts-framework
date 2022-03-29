# Custom Alerts Framework

Meant to be a lightweight script you can just run continuously on a cloud instance, check things you want to check, and then send you a text when some arbitrarily defined logic resolves to `True`. Just makes it easier than running a bunch of cronjobs.

## Instructions

On a cloud instance, you could: 

0. Change `requirements.txt` to fit your needs, if you plan to write custom rules.
1. Define a `.env` file with `TWILIO_AUTH_TOKEN`, `PHONE_TO_TEXT`, and any other secrets you have.
2. Set up a virtual environment and then run `pip install -r requirements.txt`. 
3. Write rules in any Python file.
4. Run `python main.py run --definitions YOUR_PYTHON_DEFINITIONS_FILE.py`.
