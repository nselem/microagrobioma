#!/usr/bin/env python3

import csv
import os
import sys
from datetime import datetime

# downloader_path = "fasterq-dump"
downloader_path = "/home/anton/sratoolkit.3.0.1-ubuntu64/bin/fasterq-dump"

# Check input
try:
    accdir = sys.argv[1]
except IndexError:
    print("Error: missing accession CSV file")
    sys.exit(1)
try:
    file_format = sys.argv[2]
    assert sys.argv[2] in ["fasta", "fastq"]
except IndexError:
    print("Error: missing filetype")
    sys.exit(1)
except AssertionError:
    print("Error: filetype can only be fasta or fastq")
    sys.exit(1)

# Open CSV file
with open(accdir, "r") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    next(reader)

    for acc, name in reader:
        filename = f"{acc}_{name}"

        print(f"{datetime.now()}: Downloading {acc}.")

        if file_format == "fastq":

            # Check if file exists, skip if true
            if os.path.exists(f"{filename}_1.fastq"):
                print(f"{datetime.now()}: Skipping {acc} as it already exists.")
                continue
            os.system(f"{downloader_path} -p -o {filename} {acc}")

        elif file_format == "fasta":

            # Check if file exists, skip if true
            if os.path.exists(f"{filename}.fasta"):
                print(f"{datetime.now()}: Skipping {acc} as it already exists.")
                continue
            os.system(f"{downloader_path} --fasta -p -o {filename}.fasta {acc}")

        print(f"{datetime.now()}: Finished downloading {acc}.")

print(f"{datetime.now()}: Finished!")