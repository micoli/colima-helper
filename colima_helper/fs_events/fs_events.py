import time
import logging
from watchdog.observers import Observer
from paramiko import SSHConfig

from colima_helper.fs_events.file_event_handler import FileEventHandler
from colima_helper.process import process_exec


def get_ssh_config(colima_host):
    config_text = process_exec(['/usr/local/bin/colima', 'ssh-config', colima_host])
    configs = SSHConfig.from_text(config_text)
    return configs.lookup(colima_host)


def forward_fsevents(path, colima_host, patterns, ignore_patterns):
    observer = Observer()
    event_handler = FileEventHandler(
        get_ssh_config(colima_host),
        patterns,
        ignore_patterns
    )
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    logging.warning("FS event forwarder started, path '%s', host: '%s'" % (path, colima_host))
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        logging.warning("FS event forwarder stopped")
        observer.stop()
        observer.join()
