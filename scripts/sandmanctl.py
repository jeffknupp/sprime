#! /usr/bin/env python
"""sandmanctl is a command-line script used to create a RESTful API service
from a legacy database without requiring the writing of code."""

# Standard library imports
import argparse
import sys

# Application imports
from sandman import reflect_all_app


def main():
    """Main entry point for script."""
    arguments = argparse.ArgumentParser(
        description='Start an auto-generated REST API for an existing'
        'database')
    arguments.add_argument(
        'URI',
        help='The URI of the database to'
        'connect to, in the format '
        'type+driver@user:password@host/database_name.')
    arguments.add_argument(
        '-p', '--port', default=5000, required=False,
        help='Port number for the sandman API service to serve on.')
    arguments.add_argument(
        '-m', '--host', default='0.0.0.0', required=False,
        help='Hostname for the sandman API service to serve on.')

    args = arguments.parse_args()

    app = reflect_all_app(args.URI)
    app.run(args.host, args.port)

if __name__ == '__main__':
    sys.exit(main())
