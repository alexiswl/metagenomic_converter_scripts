#!/usr/bin/env python

# This script takes in an a taxid as an input and outputs
# as a k__bacteria|p_bacteriodetes etc output.

# Import the required directories
import sys
from ete3 import NCBITaxa
import argparse
import pandas as pd
ncbi = NCBITaxa()

# Define the global variables (constants)
FILE_TYPE_CHOICES = ["csv", "tsv"]
SEP_TYPES = {"csv":",", "tsv":"\t"}

# Define the standard ranks that we wish to keep of each classification.
# We put superkingdom at the end as a cheeky way of converting the superkingdom
# class to kingdom in the output format.
STANDARD_RANKS = ("kingdom", "phylum", "class", "order", "family", "genus", "species", "superkingdom")

# Semi-global variables (yet to be defined)
args = "" 


def import_arguments():
    global args 
    # Import the argument, will either be a tax_id or a reference to a file.
    parser = argparse.ArgumentParser(description="Input a taxid and convert it to a metaphlan output" +
                                                 "Can also parse in a tsv or csv and specify the column to"
                                                 "select as the taxid.")

    # What type of argument will it be, a single integer or a file?
    parser.add_argument("mode", choices=['bash', 'file'], 
                         help="are your taxid inputs in a csv/tsv file or as space separated values on the command line?")
    parser.add_argument('taxids', nargs='*')


    # If it's a type of file, csv or tsv
    parser.add_argument("--file_type", #type="str",
                       help="what type of file is this?", 
                       choices=FILE_TYPE_CHOICES)
    parser.add_argument("--column", #type="int",	
                        help="Which column represents the taxids? (where the first column is the 0th column)")

    # Parse the arguments into the script.
    args = parser.parse_args()
    args_checker(args)


def args_checker(args):
	if args.mode == "bash" and args.file_type is not None:
		sys.exit("filetype has been defined and bash mode is on, please change mode to 'file'")
	if args.mode == "bash" and args.column is not None:
		sys.exit("column has been defined and bash mode is on, please change mode to 'file'")
	if args.mode == "bash":
		for taxid in args.taxids:
			try:
				taxid_as_int = int(taxid)
			except ValueError:
				sys.exit("%s is not an int. Exiting script." % taxid)
	if args.mode == "file" and args.file_type is None:
		sys.exit("file mode is on and filetype has not been specified")
	if args.mode == "file" and args.column is None:
		sys.exit("file mode is on and column is not specified")


def run_taxid():
    # Is it just a single taxid or is it a csv/tsv with a specific column for tax ids?
    if args.mode == "bash":
	for taxid in args.taxids:
        	metaphlan_line = taxid2metaphlan(taxid)
        	print(metaphlan_line)
    else:
	for taxid_file in args.taxids:
        	taxids = pd.read_table(taxid_file, sep=SEP_TYPES[args.file_type], usecols=[int(args.column)], header=None)
        	for index, taxid in taxids.iterrows():		
            		metaphlan_line = taxid2metaphlan(taxid[0])
            		print(metaphlan_line)


def taxid2metaphlan(tax_id):
    # Declare the metaphlan lineage as a list that we will later convert into a string.
    metaphlan_lineage = []

    # Get a list of taxids of ancestors from the tax id to the root of the tree of life.
    try:
        lineages = ncbi.get_lineage(tax_id)
    except ValueError:  # Depending on which database you use, some tax ids will not be found.
        sys.exit(tax_id + "not found in database")

    # Now filter out those that are not within the standard_ranks
    lineages_tmp = []
    for lineage in lineages:
        rank = ncbi.get_rank([lineage]).values()[0]
        if rank in STANDARD_RANKS:
            lineages_tmp.append(lineage)
    lineages = lineages_tmp
    name_lineages = []

    # Convert the tax ids to scientific names at that node in the tree.
    for lineage in lineages:
        name_lineages.append(ncbi.get_taxid_translator([lineage]).values()[0])

    # Run through each of the standard ranks with the tree node.
    for lineage, standard in zip(name_lineages, STANDARD_RANKS):
        metaphlan_lineage.append(standard[0] + "__" + lineage)

    # Join tree nodes with the pipe symbol
    metaphlan_line = '|'.join(metaphlan_lineage)

    # Output in metaphlan format
    return(metaphlan_line)


def main():
    # Import the arguments
    import_arguments()

    # Output the tax id
    run_taxid()

main()
