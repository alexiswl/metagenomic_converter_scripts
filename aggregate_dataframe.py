#!/usr/bin/env python

# Not strictly a metagenomic script, but a useful tool to aggregate a tsv file.

# Let's say you have the following input:
"""
taxa   freq
 225   52
  34   25
  43   40
 225   15

This will be converted to:

taxa    freq
 225      67
  34      25
  43      40
"""

# Import pandas and argparse libraries. Can you name a greater pair? I'll wait.
import argparse
import pandas as pd
import numpy as np

# Import the still very important but taken for granted sys library
import sys

# Set global arguments
FILE_TYPE_CHOICES = ("csv", "tsv")
SEP_TYPES = {"csv": ",", "tsv": "\t"}

# Set semi global variables
args = ""


def import_arguments():
    global args

    parser = argparse.ArgumentParser(description="Input a tsv or csv file" +
                                     " and specify the column(s) you wish to aggregate.")
    # Where's the file?
    parser.add_argument("--input_file", help="/path/to/dataframe")
    # Delimiter type
    parser.add_argument("--input_delimiter", help="what type of file is the input?", choices=FILE_TYPE_CHOICES,
                        default="csv")
    parser.add_argument("--output_delimiter", help="what type of file is the output", choices=FILE_TYPE_CHOICES,
                        default="csv")
    # Key columns (generally the taxid)
    parser.add_argument("--key_columns", help="Names of the columns would you like to aggregate by. " +
                        "Multiple columns should be separated by commas")
    # Value columns (generally the frequency)
    parser.add_argument("--value_columns", help="Names of the columns would you like to aggregate?" +
                        "Multiple columns should be separated by commas")

    # A file should contain a header, if it doesn't, you'll need to parse in the names
    parser.add_argument("--header", help="Does this file contain a header? Default = no",
                        default=None, action='store_true')
    parser.add_argument("--names", help="Names of the columns you wish to pass in to the dataframe " +
                        "(not required if a header exists)")

    # Parse the arguments into the script
    args = parser.parse_args()

    # Check that the arguments are logical
    args_checker(parser)


def args_checker(parser):
    if not args.header and not args.names:
        parser.print_usage()
        sys.exit("Need to print either names or header")


def import_dataframe():
	if args.header:
    		df = pd.read_table(args.input_file, sep=SEP_TYPES[args.input_delimiter], header=args.header)
	else:  # Names
		df = pd.read_table(args.input_file, sep=SEP_TYPES[args.input_delimiter], header=None, names=args.names.split(","))
	return df


def aggregate_dataframe():
    df = import_dataframe()
    print(df)
    key_columns = args.key_columns.split(",") 

    value_columns = args.value_columns.split(",")
    value_columns_dict = {}

    # Create value_columns_dict:
    for column in value_columns:
       	value_columns_dict[column] = "sum"
	
    	print(key_columns)
    	print(value_columns)

    # Create the aggregate dataframe
    print(list(df.groupby([key for key in key_columns])))
    output_df = df.groupby([key for key in key_columns]).aggregate(np.sum)
    #output_df = df.groupby([key for key in key_columns]).agg(value_columns)
    output_df.to_csv(sys.stdout, sep=SEP_TYPES[args.output_delimiter])


def main():
    # Import the arguments
    import_arguments()

    # Import and output the data frame to stdout
    aggregate_dataframe()

main()
