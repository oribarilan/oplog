import itertools
import sys
import threading
import time


class Spinner:
    def __init__(self, disable=False, force=False, stream=sys.stderr, cycle=None, nesting_level=0):
        self.nesting_level = nesting_level
        _cycle = cycle or ['-', '/', '|', '\\']
        self.spinner_cycle = itertools.cycle(_cycle)
        self.disable = disable
        self.force = force
        self.stream = stream
        self.stop_running = None
        self.spin_thread = None
        self.paused = False

    def move_cursor_up(self, n):
        self.stream.write('\033[%dA' % n)

    def clear_current_line(self):
        self.stream.write('\033[2K')

    def start(self):
        if self.disable:
            return
        if self.stream.isatty() or self.force:
            line = "\n" * self.nesting_level
            if len(line) > 0:
                self.stream.write(line)  # St
            self.stop_running = threading.Event()
            self.spin_thread = threading.Thread(target=self.init_spin)
            self.spin_thread.start()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
        self.move_cursor_up(1)

    def terminate(self):
        if self.disable:
            return False
        if self.spin_thread:
            self.stop_running.set()
            self.spin_thread.join()
            if self.stream.isatty() or self.force:
                self.stream.write(' ' * len(next(self.spinner_cycle)))
                self.stream.write('\b' * len(next(self.spinner_cycle)))
                self.stream.flush()
        return False

    def init_spin(self):
        while not self.stop_running.is_set():
            if not self.paused:
                content_to_stream = next(self.spinner_cycle)
                self.stream.write(content_to_stream)
                self.stream.flush()
                self.stop_running.wait(0.25)
                self.stream.write(''.join(['\b'] * len(content_to_stream)))
                self.stream.flush()
            else:
                self.stop_running.wait(0.25)