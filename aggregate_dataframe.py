#!/usr/bin/env python

# Not strictly a metagenomic script, but a useful tool to aggregate a tsv file.

# Let's say you have the following input:
'''
taxa   freq
 225   52
  34   25
  43   40
 225   15
'''

# This will be converted to:
'''
taxa    freq
 225      67
  34      25
  43      40
'''

# Import pandas and argparse. Can you name a greater pair? I'll wait.
import argparse
import pandas as pd

# Set global arguments
FILE_TYPE_CHOICES = ("csv", "tsv")
SEP_TYPES = {"csv": ",", "tsv": "\t"}

# Set semi global variables
parser = ""


def import_arguments():
    global parser

    parser = argparse.ArgumentParser(description="Input a tsv or csv file" +
                                     " and specify the column(s) you wish to aggregate.")

    input_type.add_argument(--)