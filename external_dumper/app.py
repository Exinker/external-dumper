import struct
import sys
from typing import BinaryIO

from external_dumper.core import Dump


DATA_TYPE_SIZE = {
    'b': 1,
    'i': 4,
    'l': 8,
    'f': 4,
    'd': 8,
    's': 4,
}  # в словаре хранится размер каждого типа данных в байтах
DEBUG = False


def _format_key(key: str) -> str:
    """Format keys struct.unpack()."""

    return {
        'l': 'q',  # идентификатор типа данных 'l' соответствует значению параметра format='q'
    }.get(key, key)


def _parse_heading(stream: BinaryIO) -> str:
    """Read dump's heading from stream."""
    heading = ''.join([
        chr(line)
        for line in stream.read(3)
    ])

    if not heading:
        raise IOError('`heading` is not parsed!')
    return heading


def _parse_version(stream: BinaryIO) -> int:
    """Read dump's version from stream."""
    version = stream.read(1)

    if not version:
        raise IOError('`version` is not parsed!')
    return version


def _parse_data(stream: BinaryIO) -> dict:
    """Read dump's data from stream and parse it recursively."""

    dump = {}
    while True:
        line = stream.read(1)

        if line == b'':  # end of buffer
            break

        elif line == b'<':  # begin nest
            name_size = struct.unpack('>i', stream.read(4))[0]
            name = stream.read(name_size).decode('utf-8')

            #
            if name not in dump:
                dump[name] = []

            dump[name].append(_parse_data(stream=stream))

        elif line == b'>':  # end nest
            break

        else:  # parse variable
            data_type = chr(int.from_bytes(line, byteorder='big')).lower()
            data_type_is_array = not chr(int.from_bytes(line, byteorder='big')).islower()
            data_type_size = DATA_TYPE_SIZE.get(data_type, 0)

            if DEBUG:
                print('data_type:', data_type)
                print('data_type_size:', data_type_size)

            name_size = int.from_bytes(stream.read(4), byteorder='big')
            name = ''.join([chr(datum) for datum in stream.read(name_size)])

            if DEBUG:
                print('name:', name)
                print('name_size:', name_size)

            if data_type_is_array:
                length = int.from_bytes(stream.read(4), byteorder='big')

                if DEBUG:
                    print('array length:', length)

                value = []
                for _ in range(length):
                    line = stream.read(data_type_size)

                    if data_type in ['i', 'l', 'f', 'd']:
                        value.append(struct.unpack('>' + _format_key(data_type), line)[0])

                    elif data_type in ['b']:
                        value.append(line)

                    elif data_type in ['s']:
                        value_size = struct.unpack('>i', line)[0]
                        value.append(stream.read(value_size).decode('utf-8'))

                    else:
                        raise TypeError(f'{data_type} is unknown dump type')

            else:
                line = stream.read(data_type_size)

                if data_type in ['i', 'l', 'f', 'd']:
                    value = struct.unpack('>' + _format_key(data_type), line)[0]

                elif data_type in ['b']:
                    value = line

                elif data_type in ['s']:
                    value_size = struct.unpack('>i', line)[0]
                    # value = ''.join([chr(datum) for datum in stream.read(value_size)])
                    value = stream.read(value_size).decode('utf-8')

                else:
                    raise TypeError(f'{data_type} is unknown dump type')

            dump[name] = value

    return dump


class Dumper:

    def __init__(self):
        self._dump = None

    @property
    def stream(self) -> BinaryIO:
        return sys.stdin.buffer

    @property
    def dump(self) -> Dump:
        if self._dump is None:
            raise ValueError

        return self._dump

    # --------        handlers        --------
    def run(self, verbose: bool = False) -> None:
        """Run dumper."""

        # dump
        heading = _parse_heading(self.stream)
        version = _parse_version(self.stream)
        data = _parse_data(self.stream)

        dump = Dump(
            header=heading,
            version=version,
            data=data,
        )

        # verbose
        if verbose:
            dump.print()

        #
        self._dump = dump

    def write(self) -> None:
        """Write dump to file."""
        self.dump.write()

    def print(self) -> None:
        """Print dump to stdin."""
        self.dump.print()


if __name__ == '__main__':
    dumper = Dumper()

    dumper.run()
    dumper.write()
    dumper.print()
