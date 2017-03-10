#!/usr/bin/env python

"""
This picks uo a file with a single column list.
Converts this list into a Series type and outputs a summary.
"""

import pandas
import sys

# Open file and generate list from each line
file_name = sys.argv[1]

file_h = open(file_name, 'r')
# series, list on lines in file.
# Last line is always blank
series = [line.rstrip() for line in file_h]

file_h.close()
# Import into series
my_series = pandas.Series(series)

print(my_series.value_counts().to_string())
