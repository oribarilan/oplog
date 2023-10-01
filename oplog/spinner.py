import itertools
import sys
import threading
import time


class Spinner:
    def __init__(self, desc: str, disable=False, force=False, stream=sys.stderr, cycle=None, nesting_level=0):
        self.desc = desc
        self.nesting_level = nesting_level
        _cycle = cycle or [
            "( ●    )",
            "(  ●   )",
            "(   ●  )",
            "(    ● )",
            "(     ●)",
            "(    ● )",
            "(   ●  )",
            "(  ●   )",
            "( ●    )",
            "(●     )"
        ]
        _cycle = [f"{self._format_desc(desc=desc, nesting_level=nesting_level)}: {c}" for c in _cycle]
        self.spinner_cycle = itertools.cycle(_cycle)
        self.disable = disable
        self.force = force
        self.stream = stream
        self.stop_running = None
        self.spin_thread = None
        self.paused = False

    def move_cursor_up(self, n):
        self.stream.write('\033[%dA' % n)

    def move_cursor_backward(self, n):
        self.stream.write('\033[%dD' % n)

    def move_cursor_down(self, n):
        self.stream.write('\033[%dB' % n)

    def clear_current_line(self):
        self.stream.write('\033[2K')

    def move_cursor_right(self, n):
        self.stream.write('\033[%dC' % n)

    def start(self):
        if self.disable:
            return
        if self.stream.isatty() or self.force:
            if self.nesting_level > 0:
                self.stream.write('\n')
            self.stop_running = threading.Event()
            self.spin_thread = threading.Thread(target=self.init_spin)
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
            if self.stream.isatty() or self.force:
                self.stream.write(' ' * len(next(self.spinner_cycle)))
                self.stream.write('\b' * len(next(self.spinner_cycle)))
                self.stream.flush()
        if self.nesting_level > 0:
            self.move_cursor_up(1)
        # return False

    def init_spin(self):
        while not self.stop_running.is_set():
            if not self.paused:
                content_to_stream = next(self.spinner_cycle)
                self.stream.write(content_to_stream)
                self.stream.flush()
                self.stop_running.wait(0.25)
                self.stream.write('\b' * len(content_to_stream))
                self.stream.flush()
            else:
                self.stop_running.wait(0.25)

    def _format_desc(self, desc: str, nesting_level: int):
        indentation = "|   " * nesting_level
        formatted_line = f"{indentation}|── {desc}:    "
        return formatted_line
