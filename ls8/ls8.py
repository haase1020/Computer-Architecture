#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

# sys.argv[0] == "ls8.py"
# sys.argv[1] == "examples/mult.ls8"

cpu.load()
# use command line arguments to open a file,
# read in its contents line by line, and save appropriate data into RAM
cpu.run()
