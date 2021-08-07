#!/usr/bin/env python3
"""Console script for pycs."""
import sys
import click
import pycs

# from .pycs import start


##############################################################################
@click.command()
@click.option('--rounds', help="Number of rounds to run", default=100)
def main(rounds):
    """Console script for pycs."""
    pycs.start(rounds)


##############################################################################
if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

# EOF
