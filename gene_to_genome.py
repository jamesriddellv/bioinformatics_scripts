# Author: James Riddell V (riddell.26@buckeyemail.osu.edu)
# Date: 01/22/2023
# Purpose: This script takes in an amino acid file from DRAM-v output called genes.faa and formats it
# into a gene-to-genome file for vConTACT2. May need to modify for specific header.

# Example header this file parses:
# >assembly_ANENOME3P0-PE-IL12-1--IL12Illumina_CTTGTA_L001.fa_contig_31__full-cat_1_4 rank: D; Bacteriophage replication gene A protein (GPA) [PF05840.16] (db=pfam)

# example command-line usage: python3 gene_to_genome.py <infile> <outfile>
import sys
import regex as re

# opens output file to write to
with open(sys.argv[2],'wt') as outfile:
    outfile.write("protein_id\tcontig_id\tkeywords\n")

    # reads input file
    with open(sys.argv[1], 'r') as input_table:

        # parses each line of the amino acid file
        for line in input_table:

            # searches for fasta headers
            if (">" in line):

                # extract contig id
                contig_id = re.findall("assembly.*contig_.* rank", line)[0][:-5]

                # searches for brackets that contain the protein id
                protein_id = re.findall("\[(.*)\]", line)
                if protein_id == []:
                    protein_id = 'NA'
                else:
                    protein_id = protein_id[0]

                # extracts other information from the header
                rank = re.findall("(rank: [A-Z])", line)
                if len(rank) == 0:
                    rank = 'NA'
                if type(rank) == list:
                    rank = rank[0]
                description = re.findall("(; .*) \[", line)
                if len(description) == 0:
                    description = '; NA'
                if type(description) == list:
                    description = description[0]
                    
                # write to the outfile
                outfile.write(protein_id + '\t' + contig_id + '\t' + rank + description + '\n')
