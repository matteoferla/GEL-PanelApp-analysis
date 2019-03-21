#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__doc__ = \
    """
    This part of the analysis was conducted in SNV analyser folder as the protein module's data uses 50 GB and needs to be compressed and streamlined.
    NB. Written for python 3, not tested under 2.
    """


import json, csv

from warnings import warn

from protein import Protein

import os

from multiprocessing.pool import ThreadPool as Pool
from threading import Lock

from pprint import PrettyPrinter
pprint = PrettyPrinter().pprint

names = json.load(open('GEL_names.json'))
namedex = json.load(open(os.path.join(Protein.settings.data_folder,'human_prot_namedex.json')))

def ops(name):
    #print(name)
    protein = Protein(gene_name=name)
    if name in namedex:
        protein.uniprot = namedex[name]
    else:
        protein.uniprot = 'ERROR'
    try:
        protein.parse_uniprot()
        protein.parse_pLI()
        protein.parse_swissmodel()
    except Exception as err:
        warn(str(err))
    data = {'%modelled': protein.get_percent_modelled(),
            **{k: getattr(protein, k) for k in keys},
            **{k: len(getattr(protein, k)) for k in lenkeys}}
    lock.acquire()
    sheet.writerow(data)
    lock.release()
    return True


with open('GEL.csv','w',newline='') as w:
    keys = ('gene_name','uniprot_name','uniprot','pLI','pRec','pNull')
    lenkeys = ('pdbs','pdb_matches','sequence')
    sheet = csv.DictWriter(w,keys+lenkeys+('%modelled',))
    sheet.writeheader()
    lock = Lock()
    Pool(50).map(ops, names)




