#!/usr/bin/env python
# coding: utf-8
"""
Create BIOM-format tables (http://biom-format.org) from 
Kraken output (http://ccb.jhu.edu/software/kraken/).
"""
from __future__ import absolute_import, division, print_function

from pathlib import Path
import argparse
from collections import OrderedDict
import csv
from datetime import datetime as dt
from gzip import open as gzip_open
import os.path as osp
import re
import sys
from textwrap import dedent as twdd

from biom.table import Table
import numpy as np
import pandas as pd

try:
    import h5py
    HAVE_H5PY = True
except ImportError:
    HAVE_H5PY = False

__author__ = "Shareef M. Dabdoub"
__copyright__ = "Copyright 2016, Shareef M. Dabdoub"
__credits__ = ["Shareef M. Dabdoub", "Akshay Paropkari", 
               "Sukirth Ganesan", "Purnima Kumar"]
__license__ = "MIT"
__url__ = "http://github.com/smdabdoub/kraken-biom"
__maintainer__ = "Shareef M. Dabdoub"
__email__ = "dabdoub.2@osu.edu"
__version__ = '1.2.0'


field_names = ["pct_reads", "clade_reads", "taxon_reads", 
               "rank", "ncbi_tax", "sci_name"]
ranks = ["D", "P", "C", "O", "F", "G", "S", "SS"]



def tax_fmt(tax_lvl, end):
    """
    Create a string representation of a taxonomic hierarchy (QIIME for now).

    :type tax_lvl: dict
    :param tax_lvl: Keyed on the entries in ranks
    :type end: int
    :param end: The end rank index (0-based indexing). If end == 3
                then the returned string will contain K, P, C, and O.
    
    >>> tax_fmt({"K": "Bacteria", "P": "Firmicutes", "C": "Negativicutes", 
    ... "O": "Selenomonadales", "F": "Veillonellaceae", "G": "Veillonella", 
    ... "S": "Veillonella parvula", "SS": "Veillonella parvula DSM 2008"}, 4)
    'k__Bacteria; p__Firmicutes; c__Negativicutes; o__Selenomonadales'
    """
    if "S" in tax_lvl:
        if "G" in tax_lvl and tax_lvl["S"].startswith(tax_lvl["G"]):
            tax_lvl["S"] = tax_lvl["S"][len(tax_lvl["G"])+1:]
    if "SS" in tax_lvl:
        if "S" in tax_lvl and tax_lvl["SS"].startswith(tax_lvl["S"]):
            tax_lvl["SS"] = tax_lvl["SS"][len(tax_lvl["S"])+1:]
    
    tax = ["{}__{}".format(r.lower(), tax_lvl[r] if r in tax_lvl else '') 
             for r in ranks[:end+1]]
    # add empty identifiers for ranks beyond end
    #TODO: remove the :-1 when SS support is added
    tax.extend(["{}__".format(r.lower()) for r in ranks[end+1:-1]])

    # even though Bacteria, Archea are now technically Domains/superkingdoms
    # GreenGenes and other databases still list the traditional 
    # kingdom/phylum/class/etc. So this is a hack to shoehorn the kraken-report
    # data into that format.
    if tax[0].startswith('d'):
        tax[0] = "k"+tax[0][1:]

    return tax


def parse_tax_lvl(entry, tax_lvl_depth=[]):
    """
    Parse a single kraken-report entry and return a dictionary of taxa for its
    named ranks.

    :type entry: dict
    :param entry: attributes of a single kraken-report row.
    :type tax_lvl_depth: list
    :param tax_lvl_depth: running record of taxon levels encountered in
    previous calls.
    """
    # How deep in the hierarchy are we currently?  Each two spaces of
    # indentation is one level deeper.  Also parse the scientific name at this
    # level.
    depth_and_name = re.match('^( *)(.*)', entry['sci_name'])
    depth = len(depth_and_name.group(1))//2
    name = depth_and_name.group(2)
    # Remove the previous levels so we're one higher than the level of the new
    # taxon.  (This also works if we're just starting out or are going deeper.)
    del tax_lvl_depth[depth:]
    # Append the new taxon.
    erank = entry['rank']
    if erank == '-' and depth > 8 and tax_lvl_depth[-1][0] == 'S':
        erank = 'SS'
    tax_lvl_depth.append((erank, name))

    # Create a tax_lvl dict for the named ranks.
    tax_lvl = {x[0]: x[1] for x in tax_lvl_depth if x[0] in ranks}
    return(tax_lvl)


def parse_kraken_report(kdata, max_rank, min_rank):
    """
    Parse a single output file from the kraken-report tool. Return a list
    of counts at each of the acceptable taxonomic levels, and a list of 
    NCBI IDs and a formatted string representing their taxonomic hierarchies.

    :type kdata: str
    :param kdata: Contents of the kraken report file.
    """
    # map between NCBI taxonomy IDs and the string rep. of the hierarchy
    taxa = OrderedDict()
    # the master collection of read counts (keyed on NCBI ID)
    counts = OrderedDict()
    # current rank
    r = 0
    max_rank_idx = ranks.index(max_rank)
    min_rank_idx = ranks.index(min_rank)

    for entry in kdata:
        # update running tally of ranks
        tax_lvl = parse_tax_lvl(entry)

        erank = entry['rank'].strip()
        if 'SS' in tax_lvl:
            erank = 'SS'

        if erank in ranks:
            r = ranks.index(erank)     


        # record the reads assigned to this taxon level, and record the taxonomy string with the NCBI ID
        if erank in ranks and min_rank_idx >= ranks.index(erank) >= max_rank_idx:
            taxon_reads = int(entry["taxon_reads"])
            clade_reads = int(entry["clade_reads"])
            if taxon_reads > 0 or (clade_reads > 0 and erank == min_rank):
                taxa[entry['ncbi_tax']] = tax_fmt(tax_lvl, r)
                if erank == min_rank:
                    counts[entry['ncbi_tax']] = clade_reads
                else:
                    counts[entry['ncbi_tax']] = taxon_reads

    return counts, taxa


def process_samples(kraken_reports_fp, max_rank, min_rank):
    """
    Parse all kraken-report data files into sample counts dict
    and store global taxon id -> taxonomy data
    """
    taxa = OrderedDict()
    sample_counts = OrderedDict()
    for krep_fp in kraken_reports_fp:
        if not osp.isfile(krep_fp):
            raise RuntimeError("ERROR: File '{}' not found.".format(krep_fp))

        # use the kraken report filename as the sample ID
        sample_id = osp.splitext(osp.split(krep_fp)[1])[0]

        with open(krep_fp, "rt") as kf:
            try:
                kdr = csv.DictReader(kf, fieldnames=field_names, 
                                     delimiter="\t")
                kdata = [entry for entry in kdr][1:]
            except OSError as oe:
                raise RuntimeError("ERROR: {}".format(oe))

        scounts, staxa = parse_kraken_report(kdata, max_rank=max_rank, 
                                             min_rank=min_rank)

        # update master records
        taxa.update(staxa)
        sample_counts[sample_id] = scounts

    return sample_counts, taxa


def process_metadata(sample_counts,metadata):
    """
    Reads the sample metadata file. If no metadata is given, dummy metadata
    is added.

    Example dummy metadata:
        {Id : sample name}

    The first column of the TSV file should be samples ids.

    :type sample_counts: dict
    :param sample_counts: A dictionary of dictionaries with the first level
                          keyed on sample ID, and the second level keyed on
                          taxon ID with counts as values.

    :type metadata: file
    :param metadata: The path to the metadata file.

    :rtype: list
    :return: metadata: List of Dictionaries with metadata from
                       every column per sample. Only the metadata
                       corresponding to the input samples is added.
    """
    if metadata:
        metadata_frame = pd.read_csv(metadata,sep='\t')
        metadata_frame = metadata_frame.astype(str)
        samples_imported = list(sample_counts.keys())
        metadata_frame.index = metadata_frame[metadata_frame.columns[0]]
        meta_data = metadata_frame.loc[samples_imported].to_dict(
            orient='records') # select the samples in order of sample_counts.

    else :
        metadata_frame=pd.DataFrame(data=[{"Id":key}
                                          for key in sample_counts.keys() ])
        meta_data = metadata_frame.to_dict(orient='records')
    return meta_data


def create_biom_table(sample_counts, taxa, sample_metadata):
    """
    Create a BIOM table from sample counts and taxonomy metadata.

    :type sample_counts: dict
    :param sample_counts: A dictionary of dictionaries with the first level
                          keyed on sample ID, and the second level keyed on
                          taxon ID with counts as values.
    :type taxa: dict
    :param taxa: A mapping between the taxon IDs from sample_counts to the
                 full representation of the taxonomy string. The values in
                 this dict will be used as metadata in the BIOM table.

    :type sample_metadata : list
    :param sample_metadata: A list with metadata for the imported samples.
                           This is used as metadata for in the BIOM table.

    :rtype: biom.Table
    :return: A BIOM table containing the per-sample taxon counts and full
             taxonomy identifiers as metadata for each taxon.
    """
    data = [[0 if taxid not in sample_counts[sid] else sample_counts[sid][taxid] 
              for sid in sample_counts] 
                for taxid in taxa]
    data = np.array(data, dtype=int)
    tax_meta = [{'taxonomy': taxa[taxid]} for taxid in taxa]
    
    gen_str = "kraken-biom v{} ({})".format(__version__, __url__)

    return Table(data, list(taxa), list(sample_counts), tax_meta,
                 type="OTU table", create_date=str(dt.now().isoformat()),
                 generated_by=gen_str, input_is_dense=True,
                 sample_metadata=sample_metadata)


def write_biom(biomT, output_fp, fmt="hdf5", gzip=False):
    """
    Write the BIOM table to a file.

    :type biomT: biom.table.Table
    :param biomT: A BIOM table containing the per-sample OTU counts and metadata
                  to be written out to file.
    :type output_fp str
    :param output_fp: Path to the BIOM-format file that will be written.
    :type fmt: str
    :param fmt: One of: hdf5, json, tsv. The BIOM version the table will be
                output (2.x, 1.0, 'classic').
    """
    opener = open
    mode = 'w'
    if gzip and fmt != "hdf5":
        if not output_fp.endswith(".gz"):
            output_fp += ".gz"
        opener = gzip_open
        mode = 'wt'

    # HDF5 BIOM files are gzipped by default
    if fmt == "hdf5":
        opener = h5py.File

    with opener(output_fp, mode) as biom_f:
        if fmt == "json":
            biomT.to_json(biomT.generated_by, direct_io=biom_f)
        elif fmt == "tsv":
            biom_f.write(biomT.to_tsv())
        else:
            biomT.to_hdf5(biom_f, biomT.generated_by)

    return output_fp


def write_otu_file(otu_ids, fp):
    """
    Write out a file containing only the list of OTU IDs from the kraken data.
    One line per ID.

    :type otu_ids: list or iterable
    :param otu_ids: The OTU identifiers that will be written to file.
    :type fp: str
    :param fp: The path to the output file.
    """
    fpdir = osp.split(fp)[0]

    if not fpdir == "" and not osp.isdir(fpdir):
        raise RuntimeError("Specified path does not exist: {}".format(fpdir))

    with open(fp, 'wt') as outf:
        outf.write('\n'.join(otu_ids))


def handle_program_options():
    descr = """\
    Create BIOM-format tables (http://biom-format.org) from Kraken output 
    (http://ccb.jhu.edu/software/kraken/).

    The program takes as input, one or more files output from the kraken-report
    tool. Each file is parsed and the counts for each OTU (operational taxonomic
    unit) are recorded, along with database ID (e.g. NCBI), and lineage. The
    extracted data are then stored in a BIOM table where each count is linked
    to the Sample and OTU it belongs to. Sample IDs are extracted from the input
    filenames (everything up to the '.').

    OTUs are defined by the --max and --min arguments. By default these are
    set to Order and Species respectively. This means that counts assigned
    directly to an Order, Family, or Genus are recorded under the associated
    OTU ID, and counts assigned at or below the Species level are assigned to
    the OTU ID for the species. Setting a minimum rank below Species is not yet
    available.

    The BIOM format currently has two major versions. Version 1.0 uses the 
    JSON (JavaScript Object Notation) format as a base. Version 2.x uses the
    HDF5 (Hierarchical Data Format v5) as a base. The output format can be
    specified with the --fmt option. Note that a tab-separated (tsv) output
    format is also available. The resulting file will not contain most of the
    metadata, but can be opened by spreadsheet programs.

    Version 2 of the BIOM format is used by default for output, but requires the
    Python library 'h5py'. If the library is not installed, kraken-biom will 
    automatically switch to using version 1.0. Note that the output can 
    optionally be compressed with gzip (--gzip) for version 1.0 and TSV files. 
    Version 2 files are automatically compressed.

    Usage examples
    --------------
    1. Basic usage with default parameters:

    $ kraken-biom S1.txt S2.txt

      This produces a compressed BIOM 2.1 file: table.biom

    2. BIOM v1.0 output:

    $ kraken-biom S1.txt S2.txt --fmt json

      Produces a BIOM 1.0 file: table.biom

    3. Compressed TSV output:

    $ kraken-biom S1.txt S2.txt --fmt tsv --gzip -o table.tsv

      Produces a TSV file: table.tsv.gz

    4. Change the max and min OTU levels to Class and Genus:

    $ kraken-biom S1.txt S2.txt --max C --min G
    
    5. Basic usage with default parameters and metadata::
   
    $ kraken-biom S1.txt S2.txt -m metadata.tsv



    Program arguments
    -----------------"""

    parser = argparse.ArgumentParser(description=twdd(descr),
                           formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('kraken_reports', nargs='*',
                        help="Results files from the kraken-report tool.")
    parser.add_argument('-k', '--kraken_reports_fp', metavar="REPORTS_FP",
                        help="Folder containing kraken reports")
    parser.add_argument('--max', default="O", choices=ranks,
                        help="Assigned reads will be recorded only if \
                              they are at or below max rank. Default: O.")
    parser.add_argument('--min', default="S", choices=ranks,
                        help="Reads assigned at and below min rank \
                              will be recorded as being assigned to the \
                              min rank level. Default: S.")
    parser.add_argument('-o', '--output_fp', default="table.biom",
                        help="Path to the BIOM-format file. By default, the\
                        table will be in the HDF5 BIOM 2.x format. Users can\
                        output to a different format using the --fmt option.\
                        The output can also be gzipped using the --gzip\
                        option. Default path is: ./table.biom")

    parser.add_argument('-m','--metadata',default=False,
                        help="Path to the sample metadata file. This should\
                        be in TSV format. The first column should be \
                        the Sample ID. This is the same name as the \
                        input files. If no metadata is given, basic\
                        metadata is added to support importing the\
                        BIOM table into sites like phinch \
                        (http://phinch.org/index.html).\
                        Example for metadata files:\
                        http://qiime.org/documentation/\
                        file_formats.html#mapping-file-overview")
    parser.add_argument('--otu_fp',
                        help="Create a file containing just the (NCBI) OTU IDs\
                        for use with a service such as phyloT \
                        (http://phylot.biobyte.de/) to generate a phylogenetic\
                        tree for use in downstream analysis such as UniFrac, \
                        iTol (itol.embl.de), or PhyloToAST (phylotoast.org).")
    parser.add_argument('--fmt', default="hdf5", 
                        choices=["hdf5", "json", "tsv"],
                        help="Set the output format of the BIOM table.\
                              Default is HDF5.")
    parser.add_argument('--gzip', action='store_true',
                        help="Compress the output BIOM table with gzip.\
                              HDF5 BIOM (v2.x) files are internally\
                              compressed by default, so this option\
                              is not needed when specifying --fmt hdf5.")

    
    parser.add_argument('--version', action='version',                    
             version="kraken-biom version {}, {}".format(__version__, __url__))
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Prints status messages during program \
                              execution.")

    return parser.parse_args()


def main():
    args = handle_program_options()

    if args.fmt == 'hdf5' and not HAVE_H5PY:
        args.fmt = 'json'
        msg = """\
        Library 'h5py' not found, unable to write BIOM 2.x (HDF5) files.
        Defaulting to BIOM 1.0 (JSON)."""
        print(twdd(msg))

    if ranks.index(args.max) > ranks.index(args.min):
        msg = "ERROR: Max and Min ranks are out of order: {} < {}"
        sys.exit(msg.format(args.max, args.min))

    reports = args.kraken_reports
    if args.kraken_reports_fp:
        reports += [str(p) for p in Path(args.kraken_reports_fp).glob('*')]

    # load all kraken-report files and parse them
    sample_counts, taxa = process_samples(reports,
                                          max_rank=args.max,
                                          min_rank=args.min)

    # Make sample metadata. Reads the given file or
    # adds dummy metadata.
    sample_metadata = process_metadata(sample_counts, args.metadata)

    # create new BIOM table from sample counts and taxon ids
    # add taxonomy strings to row (taxon) metadata
    biomT = create_biom_table(sample_counts, taxa, sample_metadata)

    out_fp = write_biom(biomT, args.output_fp, args.fmt, args.gzip)

    if args.otu_fp:
        try:
            write_otu_file(list(taxa), args.otu_fp)
        except RuntimeError as re:
            msg = "ERROR creating OTU file: \n\t{}"
            sys.exit(msg.format(re))

    if args.verbose:
        print("".format(out_fp))
        table_str = """\
        BIOM-format table written to: {out_fp}
        Table contains {rows} rows (OTUs) and {cols} columns (Samples)
        and is {density:.1%} dense.""".format(out_fp=out_fp, 
                                              rows=biomT.shape[0], 
                                              cols=biomT.shape[1],
                                              density=biomT.get_table_density())
        print(twdd(table_str))


if __name__ == '__main__':
    main()

