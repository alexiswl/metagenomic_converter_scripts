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
FILE_TYPE_CHOICES = ("csv", "tsv")
SEP_TYPES = {"csv":",", "tsv":"\t"}

# Define the standard ranks that we wish to keep of each classification.
# We put superkingdom at the end as a cheeky way of converting the superkingdom
# class to kingdom in the output format.
STANDARD_RANKS = ("kingdom", "phylum", "class", "order", "family", "genus", "species", "superkingdom")

# Semi-global variables (yet to be defined)
parser = ""


def import_arguments():
    global parser
    # Import the argument, will either be a tax_id or a reference to a file.
    parser = argparse.ArgumentParser(description="Input a taxid and convert it to a metaphlan output" +
                                                 "Can also parse in a tsv or csv and specify the column to"
                                                 "select as the taxid.")

    # What type of argument will it be, a single integer or a file?
    input_type = parser.add_mutually_exclusive_group()
    input_type.add_argument("tax_id", type=int,
                            help="input a single tax id")
    input_type.add_argument("--file", type=str,
                            help="path to file")

    # If it's a type of file, csv or tsv
    parser.add_argument("--file_type", type="str",
                        help="what type of file is this?",
                        choices=file_type_choices, default="csv")
    parser.add_argument("--column", type="int",
                        help="Which column represents the taxids?",
                        default=0)

    # Parse the arguments into the script.
    parser.parse_args()


def run_taxid():
    # Is it just a single taxid or is it a csv/tsv with a specific column for tax ids?
    if parser.taxid:
        metaphlan_line = taxid2metaphlan(taxid)
        print(metaphlan_line)
    else:
        taxids = pd.DataFrame.read_csv(parser.file, sep=sep_types[parser.file_type],
                                   usecols=parser.column)
        for taxid in taxids:
            metaphlan_line = taxid2metaphlan(taxid)
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