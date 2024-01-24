"""Debug module to write data from stdin buffer to `.abs` file."""
from datetime import datetime
import sys


if __name__ == '__main__':
    stream = sys.stdin.buffer

    # read dump
    dump = stream.read()

    # write dump
    filename = f'{datetime.now().strftime("%Y.%m.%d_%H-%M-%S")}.abs'
    with open(filename, 'wb') as file:
        file.write(dump)
