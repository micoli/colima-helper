import logging
import time

from paramiko import SSHConfig
from watchdog.observers import Observer

from colima_helper.process import process_exec
from .file_event_handler import FileEventHandler
from .log_http_server import HttpLogHandler

logger = logging.getLogger('fs_event')


def _get_ssh_config(colima_host):
    config_text = process_exec(['/usr/local/bin/colima', 'ssh-config', colima_host])
    configs = SSHConfig.from_text(config_text)
    return configs.lookup(colima_host)


def forward_fsevents(
        path: str,
        colima_host: str,
        patterns: list[str],
        ignore_patterns: list[str],
        server_address: str,
        server_port: int
):
    http_log_handler = HttpLogHandler(server_address, server_port, 10)
    logging.getLogger().addHandler(http_log_handler)

    observer = Observer()
    event_handler = FileEventHandler(
        _get_ssh_config(colima_host),
        patterns,
        ignore_patterns
    )
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    logger.warning(
        "FS event forwarder started, path '%s', host: '%s', patterns:%s, ignored:%s, address:%s, port: %s" %
        (path, colima_host, patterns, ignore_patterns, server_address, server_port)
    )

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        logger.warning("FS event forwarder stopped")
        http_log_handler.stop()
        observer.stop()
        observer.join()
