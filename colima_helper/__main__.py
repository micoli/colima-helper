import glob
import logging
import os
import pprint
import signal
import sys

import colored_traceback
import daemon
import daemon.pidfile

from colima_helper.arguments import parse_main_args, ArgumentAction
from colima_helper.fs_events.fs_events import forward_fsevents

colored_traceback.add_hook(always=True)
pp = pprint.PrettyPrinter(indent=4)

FS_EVENT_PID_FILE_MASK = '/tmp/colima-helper-fs-events-%s.pid'
FS_EVENT_LOG_FILE_MASK = '/tmp/colima-helper-fs-events-%s.log'


def init_logger(level, filename=None):
    _format = '%(levelname)s - %(asctime)s - %(message)s'
    _date_format = '%Y-%m-%d %H:%M:%S'
    if filename is not None:
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(
            level=level,
            filename=filename,
            format=_format,
            datefmt=_date_format
        )
        return logging.root.handlers[0]
    logging.basicConfig(
        level=level,
        format=_format,
        datefmt=_date_format
    )
    return None


def main() -> None:
    parser = parse_main_args()
    args = parser.parse_args()

    if args.action == ArgumentAction.FS_EVENTS:
        def start_forward_fsevents():
            forward_fsevents(
                args.path,
                args.host,
                args.patterns,
                args.ignore_patterns,
                args.replace_patterns,
                args.address,
                args.port,
                args.cooldown_timeout
            )

        if args.daemon:
            project_name = os.path.basename(args.path)
            handler = init_logger(args.loglevel, FS_EVENT_LOG_FILE_MASK % project_name)
            daemon_context = daemon.DaemonContext(
                stdout=handler.stream,
                stderr=handler.stream,
                working_directory=args.path,
                umask=0o002,
                pidfile=daemon.pidfile.PIDLockFile(FS_EVENT_PID_FILE_MASK % project_name)
            )
            with daemon_context:
                start_forward_fsevents()
                sys.exit(0)
        else:
            init_logger(args.loglevel)
            start_forward_fsevents()
            sys.exit(0)

    if args.action == ArgumentAction.KILL_FS_EVENTS:
        project_name = os.path.basename(args.path) if args.path is not None else '*'
        files = glob.glob(FS_EVENT_PID_FILE_MASK % project_name)
        for file in files:
            with open(file, encoding='ASCII') as file_handler:
                fs_event_pid = int(file_handler.read())
                os.unlink(file)
            os.kill(fs_event_pid, signal.SIGKILL)
        sys.exit(0)

    parser.print_help(sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
