#!/usr/bin/env python3
"""Console script for pycs."""
import sys
import click
import pycs


##############################################################################
@click.command()
@click.option("--rounds", help="Number of rounds to run", default=1)
def main(rounds: int) -> int:
    """Console script for pycs."""
    pycs.start(rounds)
    return 0


##############################################################################
if __name__ == "__main__":
    sys.exit(main(1))  # pragma: no cover

# EOF
