import loompy
import numpy

def expression_loom(input_file):
    """Expression matrix attribute handler for loom files

    Supported file format may be different for each server, this function maps
    loom-specific attributes to a general data structure that can be used by
    all content testing functions regardless of file format

    Arguments:
        input_file (str): input loom file
    
    Returns:
        (dict): attribute handler, consistent structure regardless of file type 
    """

    # connects to the loom file, then remaps loom specific attributes to general
    # attribute names which are used in the content testing functions
    # eg. the loom-specific ds.ra.GeneID is mapped to dict["GeneID"]
    ds = loompy.connect(input_file)
    return {
        "GeneID": ds.ra.GeneID,
        "GeneName": ds.ra.GeneName,
        "Condition": ds.ca.Condition,
        "Tissue": ds.ca.Tissue,
        "Sample": ds.ca.Sample,
        "Value": ds,
        "FH": ds # loom file handle, closed after content testing
    }

def expression_tsv(input_file):
    """Expression matrix attribute handler for tsv files

    Parses a tsv expression matrix, maps its attributes to a dictionary with
    consistent keys that can be used by all content testing functions
    
    Arguments:
        input_file (str): input tsv file
    
    Returns:
        (dict): attribute handler, consistent structure regardless of file type
    """

    gene_ids = []
    gene_names = []
    conditions = []
    tissues = []
    samples = []
    values = []

    inc = 0
    # open the tsv file
    for l in open(input_file, "r"):
        ls = l.rstrip().split("\t")

        if not l.startswith("#"): # ignore any starting comment lines if any
            if inc == 0: # column header line

                # using the column header line, assign the conditions, samples,
                # and tissues lists
                columns = ls[2:]
                samples = [column.split(", ")[0] for column in columns]
                n_col_split = len(columns[0].split(", "))
                if n_col_split > 1:
                    conditions = [column.split(", ")[1] for column in columns]
                    if n_col_split > 2:
                        tissues = [column.split(", ")[2] for column in columns]

            else: # data lines
                # each data line contains the gene id, gene name, and all 
                # expression values
                gene_ids.append(ls[0])
                gene_names.append(ls[1])
                values.append([float(v) for v in ls[2:]])

            inc += 1
    
    # return the populated values and attribute names under consistent keys
    return {
        "GeneID": gene_ids,
        "GeneName": gene_names,
        "Condition": conditions,
        "Tissue": tissues,
        "Sample": samples,
        "Value": numpy.matrix(values),
        "FH": None
    }

def continuous_loom(input_file):
    """Continuous matrix attribute handler for loom files

    Supported file format may be different for each server, this function maps
    loom-specific attributes to a general data structure that can be used by
    all content testing functions regardless of file format

    Arguments:
        input_file (str): input loom file
    
    Returns:
        (dict): attribute handler, consistent structure regardless of file type 
    """

    # connects to the loom file, then remaps loom specific attributes to general
    # attribute names which are used in the content testing functions
    ds = loompy.connect(input_file)
    return {
        "Track": ds.ra.tracks,
        "Position": ds.ca.position,
        "Value": ds,
        "FH": ds # loom file handle, should be closed after content testing
    }

def continuous_tsv(input_file):
    """Continuous matrix attribute handler for tsv files

    Parses a tsv continuous matrix, maps its attributes to a dictionary with
    consistent keys that can be used by all content testing functions
    
    Arguments:
        input_file (str): input tsv file
    
    Returns:
        (dict): attribute handler, consistent structure regardless of file type
    """

    tracks = []
    positions = []
    values = []

    inc = 0
    # open the tsv file
    for l in open(input_file, "r"):
        ls = l.rstrip().split("\t")

        if not l.startswith("#"): # ignore any starting comment lines if any
            if inc == 0: # column header line

                # using the column header line, assign the conditions, samples,
                # and tissues lists
                positions = ls[1:]

            else: # data lines
                # each data line contains the gene id, gene name, and all 
                # expression values
                tracks.append(ls[0])
                values.append([float(v) for v in ls[1:]])

            inc += 1
    
    # return the populated values and attribute names under consistent keys
    return {
        "Track": tracks,
        "Position": positions,
        "Value": numpy.matrix(values),
        "FH": None
    }

ATTRIBUTE_HANDLERS = {
    "expressions": {
        "loom": expression_loom,
        "tsv": expression_tsv
    },
    "continuous": {
        "loom": continuous_loom,
        "tsv": continuous_tsv
    }
}
"""maps format keywords to their attribute handler functions"""