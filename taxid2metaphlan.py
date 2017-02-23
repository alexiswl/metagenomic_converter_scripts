#!/usr/bin/env python

# This script takes in an a taxid as an input and outputs
# as a k__bacteria|p_bacteriodetes etc output.

# Import the required directories
import sys
from ete3 import NCBITaxa
ncbi = NCBITaxa()

# Get the tax id
tax_id = sys.argv[1]

# Define the standard ranks that we wish to keep of each classification.
# We put superkingdom at the end as a cheeky way of converting the superkingdom
# class to kingdom in the output format.
standard_ranks = ("kingdom", "phylum", "class", "order", "family", "genus", "species", "superkingdom")

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
    if rank in standard_ranks:
        lineages_tmp.append(lineage)
lineages = lineages_tmp
name_lineages = []

# Convert the tax ids to scientific names at that node in the tree.
for lineage in lineages:
    name_lineages.append(ncbi.get_taxid_translator([lineage]).values()[0])

# Run through each of the standard ranks with the tree node.
for lineage, standard in zip(name_lineages, standard_ranks):
    metaphlan_lineage.append(standard[0] + "__" + lineage)

# Join tree nodes with the pipe symbol
metaphlan_line = '|'.join(metaphlan_lineage)

# Output in metaphlan format
print(metaphlan_line)
