#!/usr/bin/env python

import argparse


def bootstrap(args):
    print('Bootstrapping process starting...')
    print("{} successfully activated!".format(args.environment))
    print('Bootstrap process completed!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--environment',
        dest='environment',
        type=str,
        required=True,
        help='Name of the environment we are bootstrapping',
    )
    args = parser.parse_args()
    bootstrap(args)
