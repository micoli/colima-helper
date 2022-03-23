import logging
from shlex import quote
from expiringdict import ExpiringDict
from watchdog.events import PatternMatchingEventHandler
from paramiko.client import SSHClient
from paramiko import AutoAddPolicy, ssh_exception

cache = ExpiringDict(max_len=100, max_age_seconds=6)


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

    def on_any_event(self, event):
        if cache.get(event.src_path) is not None:
            logging.debug("Event not forwarded because of cooldown %s" % event.src_path)
            return
        cache[event.src_path] = True

        command = 'touch -a -c %s' % quote(event.src_path)

        logging.info("Event forwarded %s" % event.src_path)
        if not self.ensure_connected():
            logging.error("Not connected to %s" % self.ssh_config['hostname'])
            return
        try:
            _, stdout, stderr = self.client.exec_command(command)
        except ssh_exception.SSHException as error:
            logging.error("Event forwarded error %s" % error)
            return

        logging.debug("Event forwarded command %s" % command)
        out = ''
        for line in iter(stdout.readline, ""):
            out = out.join(line)
        if out != '':
            logging.debug("Event forwarded result \n%s" % out)

        error = ''
        for line in iter(stderr.readline, ""):
            error = error.join(line)
        if error != '':
            logging.debug("Event forwarded error \n%s" % error)

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
