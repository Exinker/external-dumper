import sys

from .app import Dumper


VERBOSE = ('-v' in sys.argv) or ('--verbose' in sys.argv)


dumper = Dumper()
dumper.run(verbose=VERBOSE)
dumper.write()
