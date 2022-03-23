import os
import pprint
import signal
import sys
import logging
import colored_traceback

import daemon
import daemon.pidfile
from colima_helper.arguments import parse_main_args
from colima_helper.fs_events.fs_events import forward_fsevents

colored_traceback.add_hook(always=True)
pp = pprint.PrettyPrinter(indent=4)

FS_EVENT_PID_FILE = '/tmp/colima-helper-fs-events.pid'
FS_EVENT_LOG_FILE = '/tmp/colima-helper-fs-events.log'


def main() -> None:
    parser = parse_main_args()
    args = parser.parse_args()

    logging.basicConfig(
        level=args.loglevel,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    if args.action == 'kill-fs-events':
        if not os.path.exists(FS_EVENT_PID_FILE):
            sys.exit(0)
        with open(FS_EVENT_PID_FILE, encoding='ASCII') as file_handler:
            fs_event_pid = int(file_handler.read())
            os.unlink(FS_EVENT_PID_FILE)
        os.kill(fs_event_pid, signal.SIGKILL)
        sys.exit(0)

    if args.action == 'fs-events':
        if args.daemon:
            handler = logging.FileHandler(FS_EVENT_LOG_FILE)
            logger = logging.getLogger(__name__)
            logger.addHandler(handler)

            daemon_context = daemon.DaemonContext(
                stdout=handler.stream,
                stderr=handler.stream,
                working_directory=args.path,
                umask=0o002,
                pidfile=daemon.pidfile.PIDLockFile(FS_EVENT_PID_FILE)
            )
            with daemon_context:
                start_forward_fsevents(args)
                sys.exit(0)
        else:
            start_forward_fsevents(args)
            sys.exit(0)

    parser.print_help(sys.stderr)
    sys.exit(1)


def start_forward_fsevents(args):
    forward_fsevents(args.path, args.host, args.patterns, args.ignore_patterns)


if __name__ == "__main__":
    main()
