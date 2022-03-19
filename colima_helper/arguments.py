import argparse
import logging


def parse_main_args():
    parser = argparse.ArgumentParser(
        description='Colima host helper',
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(
        help='commands',
        dest='action'
    )

    fs_events_parser = subparsers.add_parser(
        'fs-events',
        help='wath for filesystem changes and "touch" on colima host'
    )
    subparsers.add_parser(
        'kill-fs-events',
        help='kill fs-event daemon'
    )
    fs_events_parser.add_argument(
        '--path',
        action='store',
        help='path to watch'
    )
    fs_events_parser.add_argument(
        '--host',
        action='store',
        help='colima host',
        default='colima'
    )
    fs_events_parser.add_argument(
        '--patterns',
        action='store',
        help='pattern',
        nargs='+',
        default=['*.js*', '*.*cs*', '*.y*ml']
    )
    fs_events_parser.add_argument(
        '--ignore-patterns',
        action='store',
        help='ignore pattern',
        nargs='+',
        default=["*.git"]
    )
    parser.add_argument(
        '--daemon',
        help="daemonize",
        action=argparse.BooleanOptionalAction,
        dest="daemon",
        default=False,
    )
    parser.add_argument(
        '--debug',
        help="Print lots of debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        '--verbose',
        help="Be verbose",
        action="store_const", dest="loglevel", const=logging.INFO,
    )
    return parser
