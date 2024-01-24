import os
import pickle
import sys
from dataclasses import dataclass
from typing import Any, Literal


INDENT = '  '


def _print_data(data: Any, prefix: str = '') -> str:
    """Show data recursively."""

    if isinstance(data, dict):
        content = []
        for key, value in data.items():
            content.append(
                f'{prefix}{key}: {_print_data(value, prefix=prefix + INDENT)}'
            )
        return '\n'.join(content)

    if isinstance(data, list):
        times = f'... x{len(data)}' if len(data) > 1 else ''

        content = [
            '[',
            _print_data(data[0], prefix=prefix + INDENT),
            f'{prefix}],{times}'
        ]
        return '\n'.join(content)

    if isinstance(data, bytes):
        return f'{ord(data)}'

    return f'{data}'

@dataclass
class Dump2:
    header: str
    version: str
    data: dict

    # --------        handlers        --------
    def write(self, format: Literal['pkl',] = 'pkl') -> None:
        """Write dump to `.pkl` file."""

        # parse filedir
        file_path, file_name = os.path.split(self.data['Filename'])
        filedir = os.path.join('data', '.'.join(file_name.split('.')[:-1]))

        # check filedir
        if not os.path.isdir(filedir):
            os.makedirs(filedir, exist_ok=True)

        # write data
        filepath = os.path.join(filedir, f'dump.{format}')

        match format:
            case 'pkl':
                with open(filepath, 'wb') as file:
                    pickle.dump(self.data, file)
            case _:
                raise ValueError(f'Format {format} is not supported!')

    # --------        private        --------
    def __post_init__(self):
        assert self.version == b'\x02', fr'Dump version {self.version} is not supported!'

    def __str__(self) -> str:
        text = _print_data(self.data, prefix=INDENT)
        content = [
            f'HEADER: {self.header}',
            f'VERSION: {self.version}',
            'DATA:',
            text,
        ]
        return '\n'.join(content)
