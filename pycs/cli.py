#!/usr/bin/env python3
"""Console script for pycs."""
import sys
import click
import pycs

# from .pycs import start


##############################################################################
@click.command()
def main(args=None):
    """Console script for pycs."""
    pycs.start()


##############################################################################
if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

# EOF
