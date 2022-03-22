import argparse
import logging
import os


class ArgumentAction:
    FS_EVENTS = 'fs-events'
    KILL_FS_EVENTS = 'kill-fs-events'
    GUI = 'gui'


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
        ArgumentAction.FS_EVENTS,
        help='wath for filesystem changes and \'touch\' on colima host'
    )
    subparsers.add_parser(
        ArgumentAction.KILL_FS_EVENTS,
        help='kill fs-event daemon'
    )
    gui_parser = subparsers.add_parser(
        ArgumentAction.GUI,
        help='docker_container GUI'
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
        default=['*.*js*', '*.*cs*', '*.y*ml']
    )
    fs_events_parser.add_argument(
        '--ignore-patterns',
        action='store',
        help='ignore pattern',
        nargs='+',
        default=['*.git']
    )
    fs_events_parser.add_argument(
        '--daemon',
        help='daemonize',
        action=argparse.BooleanOptionalAction,
        dest='daemon',
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
    parser.add_argument(
        '--debug',
        help='Print lots of debugging statements',
        action='store_const',
        dest='loglevel',
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        '--verbose',
        help='Be verbose',
        action='store_const',
        dest='loglevel',
        const=logging.INFO,
    )
    gui_parser.add_argument(
        '--docker-host',
        help='docker-host',
        action='store',
        dest='docker_host',
        default='unix://Users/%s/.colima/docker.sock' % os.getenv('USER'),
    )
    gui_parser.add_argument(
        '--fsevents-address',
        help='fsevents log address',
        dest='fsevents_address',
        default='127.0.0.1',
    )
    gui_parser.add_argument(
        '--fsevents-port',
        help='fsevents log port',
        type=int,
        dest='fsevents_port',
        default=8087,
    )
    return parser
