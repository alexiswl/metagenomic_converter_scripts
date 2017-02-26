# metagenomic_converter_scripts
List of python scripts useful for converting from one metagenomic format to another

### taxid2metaphlan
Create a metaphlan string from a taxid.

#### A simple example:
`taxid2metaphlan.py bash 561`
k__Bacteria|p__Proteobacteria|c__Gammaproteobacteria|o__Enterobacterales|f__Enterobacteriaceae|g__Escherichia

#### An example twice as complex:
`./taxid2metaphlan.py bash 561 9606`
k__Bacteria|p__Proteobacteria|c__Gammaproteobacteria|o__Enterobacterales|f__Enterobacteriaceae|g__Escherichia
k__Eukaryota|p__Metazoa|c__Chordata|o__Mammalia|f__Primates|g__Hominidae|s__Homo|s__Homo sapiens

#### Loading in a file:
`taxid2metaphlan.py file examples/taxid_list.txt --file_type tsv --column 0 --header`
k__Bacteria|p__Proteobacteria|c__Gammaproteobacteria|o__Enterobacterales|f__Enterobacteriaceae|g__Escherichia
k__Eukaryota|p__Viridiplantae|c__Streptophyta|o__Myrtales|f__Myrtaceae|g__Eugenia|s__Eugenia axillaris
k__Eukaryota|p__Metazoa|c__Chordata|o__Mammalia|f__Primates|g__Hominidae|s__Homo|s__Homo sapiens

