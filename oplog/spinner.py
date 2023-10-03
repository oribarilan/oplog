import itertools
import sys
import threading
from typing import List, Optional, Dict

from oplog.spinner_templates import templates


class Spinner:
    def __init__(self,
                 desc: str,
                 disable: bool = False,
                 cycle: Optional[List[str]] = None,
                 cycle_template: Optional[str] = None,
                 total_nest_level: int = 0,
                 cursor_offset: int = 0,
                 interval: Optional[int] = None):
        """
        A spinner that can be displayed in the terminal, and supports nesting.
        :param desc: a prefix to the spinner
        :param disable: if True, the spinner will not be displayed
        :param cycle: Optional. the spinner frames to cycle through,
            list of strings. If none, default to a template.
        :param cycle_template: Optional. a template for the spinner frames.
            If none, defaults to a default template.
        :param interval: Optional. interval (ms) between spinner frames.
            If none, defaults according to the template.
        """
        self.cursor_offset = cursor_offset
        self.total_nest_level = total_nest_level
        self.desc = desc
        self.disable = disable
        self.stream = sys.stderr
        self.stop_running: Optional[threading.Event] = None
        self.spin_thread: Optional[threading.Thread] = None
        self.paused = False

        cycle_obj: Optional[Dict] = None
        if cycle is not None:
            cycle_obj = {"frames": cycle, "interval": interval or 250}

        if cycle_template:
            cycle_obj = templates.get(cycle_template, None)

        if cycle_obj is None:
            cycle_obj = templates["dots"]

        cycle, interval = cycle_obj["frames"], cycle_obj["interval"]
        assert isinstance(interval, int), "interval must be an integer"

        cycle = [
            f"{self._format_desc(desc=desc, nesting_level=self.total_nest_level)} {c}"
            for c in cycle
        ]
        self.spinner_cycle = itertools.cycle(cycle)
        self.interval = interval / 1000

    def _move_cursor_up(self, n):
        self.stream.write('\033[%dA' % n)

    def start(self):
        if self.disable:
            return
        if self.stream.isatty():
            if self.total_nest_level > 0:
                self.stream.write('\n' * (self.cursor_offset))
            self.stop_running = threading.Event()
            self.spin_thread = threading.Thread(target=self._spin)
            self.spin_thread.start()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def terminate(self):
        if self.disable:
            return
        if self.spin_thread:
            self.stop_running.set()
            self.spin_thread.join()
            if self.stream.isatty():
                self.stream.write(' ' * len(next(self.spinner_cycle)))
                self.stream.write('\b' * len(next(self.spinner_cycle)))
                self.stream.flush()
        if self.total_nest_level > 0:
            self._move_cursor_up(self.cursor_offset)

    def _spin(self):
        while not self.stop_running.is_set():
            if not self.paused:
                content_to_stream = next(self.spinner_cycle)
                self.stream.write(content_to_stream)
                self.stream.flush()
                self.stop_running.wait(self.interval)
                self.stream.write('\b' * len(content_to_stream))
                self.stream.flush()
            else:
                self.stop_running.wait(self.interval)

    @staticmethod
    def _format_desc(desc: str, nesting_level: int):
        indentation = "|   " * nesting_level
        formatted_line = f"{indentation}|── {desc}:    "
        return formatted_line