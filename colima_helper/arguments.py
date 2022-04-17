import argparse
import logging

class ArgumentAction:
    FS_EVENTS = 'fs-events'
    KILL_FS_EVENTS = 'kill-fs-events'


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
    kill_fs_events_parser = subparsers.add_parser(
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
    fs_events_parser.add_argument(
        '--replace-patterns',
        action='store',
        help='replace pattern',
        nargs='+',
        default=[]
    )
    fs_events_parser.add_argument(
        '--cooldown-timeout',
        action='store',
        help='cooldown timeout',
        type=int,
        default=3
    )
    parser.add_argument(
        '--daemon',
        help="daemonize",
        action=argparse.BooleanOptionalAction,
        dest="daemon",
        default=False,
    )
    fs_events_parser.add_argument(
        '--address',
        help='http log address',
        dest='address',
        default='127.0.0.1',
    )
    fs_events_parser.add_argument(
        '--port',
        help='http log port',
        type=int,
        dest='port',
        default=8087,
    )
    kill_fs_events_parser.add_argument(
        '--path',
        action='store',
        help='watched path',
        type=str,
        default=None
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
