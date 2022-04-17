import logging
import os
import datetime
from shlex import quote

from expiringdict import ExpiringDict
from paramiko import AutoAddPolicy, ssh_exception
from paramiko.client import SSHClient
from watchdog.events import PatternMatchingEventHandler, FileModifiedEvent

cache = ExpiringDict(max_len=2000, max_age_seconds=5)
logger = logging.getLogger('fs_event')


class FileEventHandler(PatternMatchingEventHandler):
    def __init__(self, ssh_config, patterns, ignore_patterns):
        PatternMatchingEventHandler.__init__(
            self,
            patterns=patterns,
            ignore_patterns=ignore_patterns if ignore_patterns != [] else None,
            ignore_directories=True,
            case_sensitive=False
        )
        self.ssh_config = ssh_config
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh_connect()
        self.client.exec_command('apk info coreutils -e || sudo apk add coreutils')

    def on_any_event(self, event: FileModifiedEvent):
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(event.src_path))
        if cache.get(event.src_path) is not None:
            logger.info(
                "Event not forwarded because of cooldown %s %s" % (
                    event.src_path,
                    mtime.isoformat(' ', 'microseconds')
                )
            )
            return
        cache[event.src_path] = True

        command = 'touch -c --time=modify -d "%s" %s' % (mtime.isoformat(' ', 'microseconds'), quote(event.src_path))

        logger.info("Event forwarded %s" % command)
        if not self.ensure_connected():
            logger.error("Not connected to %s" % self.ssh_config['hostname'])
            return
        try:
            _, stdout, stderr = self.client.exec_command(command)
        except ssh_exception.SSHException as error:
            logger.error("Event forwarded error %s" % error)
            return

        out = ''
        for line in iter(stdout.readline, ""):
            out = out.join(line)
        if out != '':
            logger.debug("Event forwarded result \n%s" % out)

        error = ''
        for line in iter(stderr.readline, ""):
            error = error.join(line)
        if error != '':
            logger.debug("Event forwarded error \n%s" % error)

    def ensure_connected(self):
        if self.client is None or self.client.get_transport() is None or not self.client.get_transport().is_active():
            self.client = self.ssh_connect()
            return self.client.get_transport().is_active()
        return True

    def ssh_connect(self):
        try:
            self.client.connect(
                hostname=self.ssh_config['hostname'],
                port=int(self.ssh_config['port']),
                username=self.ssh_config['user'],
                key_filename=self.ssh_config['identityfile'],
                allow_agent=False,
                timeout=30,
            )
            return self.client
        except OSError:
            return None
