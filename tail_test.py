import os
import time
import sys

class Tail(object):
    def __init__(self, tailedfile):
        self.check(tailedfile)
        self.tailedfile = tailedfile
        self.callback = sys.stdout.write

    def follow(self, s=1):
        with open(self.tailedfile) as _file:
            _file.seek(0, 2)
            while True:
                curr_pos = _file.tell()
                line = _file.readline()
                if not line:
                    _file.seek(curr_pos)
                else:
                    self.callback(line)
                time.sleep(s)

    def register_callback(self, func):
        self.callback = func

    def check(self, tailedfile):
        if not os.access(tailedfile, os.F_OK):
            raise TailError('file not exist!!!')
        if not os.access(tailedfile, os.R_OK):
            raise TailError('file is not readable!!!')
        if os.path.isdir(tailedfile):
            raise TailError('this is a directory')


class TailError(Exception):
    def __init__(self, msg):
        self.message = msg
    def __str__(self):
        return self.message


def printline(msg):
    print msg.strip('\n')


def main():
    tail = Tail('tailed file')
    tail.register_callback(printline)
    tail.follow(1)

if __name__ == '__main__':
    main()