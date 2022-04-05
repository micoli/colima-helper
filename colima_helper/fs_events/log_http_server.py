import json
import logging
import time
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from logging import LogRecord

from colima_helper.threads import StoppableThread
from ..data_structure.constrained_list import ConstrainedList


@dataclass
class _LogItem:
    timestamp: float
    record: LogRecord


class _LogHTTPServer(ThreadingHTTPServer):
    def __init__(self, server_address: tuple[str, int], logs_list: ConstrainedList):
        self.logs_list = logs_list
        ThreadingHTTPServer.__init__(self, server_address, self._LogHandleRequests)

    class _LogHandleRequests(BaseHTTPRequestHandler):
        def __init__(self, request, client_address, server):
            BaseHTTPRequestHandler.__init__(self, request, client_address, server)

        def log_message(self, _, *args):
            return

        def do_GET(self):
            if self.path == '/logs':
                return self.do_logs()

            self.send_response(404)
            self.end_headers()

        def do_logs(self):
            self.send_response(200)
            self.send_header('Content-type', 'application/stream+json')
            self.end_headers()
            last_index = 0
            while True:
                try:
                    logs_list: ConstrainedList = self.server.logs_list
                    for (index, log) in logs_list.get_from(last_index):
                        line = json.dumps({
                            'timestamp': log.timestamp,
                            'name': log.record.name,
                            'levelName': log.record.levelname,
                            'message': log.record.getMessage(),
                        })
                        self.wfile.write((line + '\n').encode('UTF-8'))
                        last_index = index
                    time.sleep(1)

                except BrokenPipeError:
                    return


class HttpLogHandler(logging.StreamHandler):
    def __init__(self, address: str, port: int, history_max_items: int):
        logging.StreamHandler.__init__(self)
        self.server_thread = None
        if port == 0:
            return
        self.logs = ConstrainedList(history_max_items)

        server = _LogHTTPServer((address, port), self.logs)
        self.server_thread = StoppableThread(target=server.serve_forever)
        self.server_thread.start()

    def stop(self):
        if self.server_thread is None:
            return
        self.server_thread.stop()
        self.server_thread.join()

    def emit(self, record: LogRecord):
        if self.server_thread is None:
            return
        try:
            self.logs.append(_LogItem(time.time(), record))
        except (KeyboardInterrupt, SystemExit):
            self.handleError(record)
