#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load()
# use command line arguments to open a file,
# read in its contents line by line, and save appropriate data into RAM
cpu.run()
