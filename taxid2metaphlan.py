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
SEP_TYPES = {"csv": ",", "tsv": "\t"}

# Define the standard ranks that we wish to keep of each classification.
# We put superkingdom at the end as a cheeky way of converting the superkingdom
# class to kingdom in the output format.
STANDARD_RANKS = ("superkingdom", "kingdom", "phylum", "class", "order", "family", "genus", "species")


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
                        help="are your taxid inputs in a csv/tsv file" +
                        " or as space separated values on the command line?")

    # Nargs = * means that we can have multiple taxids present on the command line
    parser.add_argument('taxids', nargs='*')

    # If it's a type of file, csv or tsv
    parser.add_argument("--file_type",
                        help="what type of file is this?",
                        choices=FILE_TYPE_CHOICES)
    parser.add_argument("--column",
                        help="Which column represents the taxids? (where the first column is the 0th column)")
    parser.add_argument("--header",
                        help="Does the file contain a header? Default = no",
                        default=False, action='store_true')

    # Parse the arguments into the script.
    args = parser.parse_args()
    args_checker()


def args_checker():
    # Check to ensure that switches make logical sense
    if args.mode == "bash" and args.file_type is not None:
        sys.exit("filetype has been defined and bash mode is on, please change mode to 'file'")
    if args.mode == "bash" and args.column is not None:
        sys.exit("column has been defined and bash mode is on, please change mode to 'file'")

    # Ensure that each taxid present is of an integer value
    if args.mode == "bash":
        for taxid in args.taxids:
            try:
                taxid_as_int = int(taxid)  # test to see if taxid can be converted to an int
            except ValueError:
                sys.exit("%s is not an int. Exiting script." % taxid)

    # Ensure that if file mode is on, that the file type has been specified
    if args.mode == "file" and args.file_type is None:
        sys.exit("file mode is on and filetype has not been specified")
    # Ensure that if file mode is on, that the column number has been specified
    if args.mode == "file" and args.column is None:
        sys.exit("file mode is on and column is not specified")

    # Set the header number if the header switch has been enabled
    if args.header:
        args.header = 0
    else:
        args.header = None


def run_taxid2metaphlan():
    # Is it just a single taxid or is it a csv/tsv with a specific column for tax ids?
    if args.mode == "bash":
        for taxid in args.taxids:
            metaphlan_line = taxid2metaphlan(taxid)
            print(metaphlan_line)
    else:  # args.mode is a csv or tsv file
        for taxid_file in args.taxids:
            taxids = pd.read_table(taxid_file, sep=SEP_TYPES[args.file_type], usecols=[int(args.column)], header=args.header)
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
        sys.stderr.write(str(tax_id) + "not found in database\n")
	return

    # Now filter out those that are not within the standard_ranks 
    # Also determine if there exists the subspecies - must be put in manually - as classed as 'no_rank'
    lineages_tmp = []
    subspecies_level = None
    for index, lineage in enumerate(lineages):
        rank = ncbi.get_rank([lineage]).values()[0]
        if rank in STANDARD_RANKS:
            lineages_tmp.append(lineage)
	if rank == "species" and len(lineages) != index + 1:  # Make sure species isn't the last level
	   subspecies_level = index + 1  # Subspecies will be the level after species.
    	   lineages_tmp.append(lineages[subspecies_level])
    lineages = lineages_tmp 

    # Convert the tax ids to scientific names at that node in the tree.
    name_lineages = []
    for lineage in lineages:
        name_lineages.append(ncbi.get_taxid_translator([lineage]).values()[0])

    # Run through each of the standard ranks with the tree node.
    for lineage, name_lineage in zip(lineages, name_lineages):
        rank = ncbi.get_rank([lineage]).values()[0]
        if is_bac(name_lineage):
            rank = "kingdom"  # We change superkingdom to kingdom when dealing with bacteria
	if rank == "no rank":  # Subspecies
	    rank = "subspecies"
	# First letter of rank. double underscore, name at taxid: s__Homo sapien
        metaphlan_lineage.append(rank[0] + "__" + name_lineage) 

    # Join tree nodes with the pipe symbol
    metaphlan_line = '|'.join(metaphlan_lineage)

    # Output in metaphlan format
    return metaphlan_line


def is_bac(rank_0):
    # Grabs the first id from rank to check if bacteria
    if rank_0 == "Bacteria":
        return True
    return False


def main():
    # Import the arguments
    import_arguments()

    # Output the tax id
    run_taxid2metaphlan()

main()
