import click
from logic import definitions
from logic.scheduler import Scheduler
from inspect import getmembers, isfunction
from dotenv import load_dotenv
from utils import create_rules_from_functions

load_dotenv()


@click.group()
def cli():
    """Command line interface."""


@cli.command()
@click.option(
    "--dont_bother_for",
    default=5 * 60,
    help="how long to wait between alerts of the same rule",
)
def run(dont_bother_for):
    """Main subroutine."""
    print("Creating rules...")
    defined_functions = getmembers(definitions, isfunction)
    rules = create_rules_from_functions(defined_functions)
    for rule in rules:
        print("> {}".format(rule.name))
    print("\nStarting...")
    schedule = Scheduler(rules, dont_bother_for=dont_bother_for)
    schedule.run()


if __name__ == "__main__":
    cli()
