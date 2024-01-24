"""
Debug module to stream dump from `.abs` file to stream.

Example of pipeline:
    `python debug/streamer.py "./dump/2023.06.01_16-29-09.abs" | python -m external_dumper -v`
"""
import sys
from typing import BinaryIO


def load_dump(filename: str) -> str:
    """Load dump (binary data) from `.abs` filename."""
    with open(filename, 'rb') as file:
        return file.read()


def write_dump(dump: bytes, stream: BinaryIO):
    """Write dump (binary data) to buffer."""

    stream.write(dump)


if __name__ == '__main__':
    _, filename, *_ = sys.argv

    dump = load_dump(filename)
    write_dump(dump, stream=sys.stdout.buffer)
