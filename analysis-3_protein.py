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

from collections import Counter
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import os

from multiprocessing.pool import ThreadPool as Pool
from threading import Lock

from pprint import PrettyPrinter
pprint = PrettyPrinter().pprint

names = json.load(open('GEL_names.json'))
namedex = json.load(open(os.path.join(Protein.settings.data_folder,'human_prot_namedex.json')))




def partA():
    def ops(name):
        # print(name)
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

    with open('GEL.csv', 'w', newline='') as w:
        keys = ('gene_name', 'uniprot_name', 'uniprot', 'pLI', 'pRec', 'pNull')
        lenkeys = ('pdbs', 'pdb_matches', 'sequence')
        sheet = csv.DictWriter(w, keys + lenkeys + ('%modelled',))
        sheet.writeheader()
        lock = Lock()
        Pool(50).map(ops, names)

genes = [x.rstrip() for x in open('names.txt')]


def partB(name, test):
    protein = Protein(uniprot=name)
    try:
        protein.parse_uniprot()
        if 'transmembrane region' in protein.features:
            return 'TM'
        if test == 'stability':
            stability = ProteinAnalysis(protein.sequence).instability_index()
            if stability > 40:
                return 'Stable'
            else:
                return 'Unstable'
        elif test == 'fexibility':
            f = ProteinAnalysis(protein.sequence).flexibility()
            flexibility  = sum(f)/len(f)
            print(flexibility)
            raise NotImplementedError
    except:
        return 'ERROR'

def partC():
    Protein.settings.error_tolerant = False
    # c = Counter([partB(n, 'stability') for n in genes])
    # print(c.most_common())

    candidates = []
    for name in genes:
        protein = Protein(uniprot=name)
        protein.parse_uniprot()
        if 'transmembrane region' in protein.features:
            continue
        else:
            stability = ProteinAnalysis(protein.sequence).instability_index()
            if stability > 40:
                candidates.append((name, protein.gene_name, protein.recommended_name, len(protein)))

    for g in candidates:
        # print(g)
        print(g[0])

def redux():
    def ops(name):
        # print(name)
        protein = Protein(gene_name=name)
        if name in namedex:
            protein.uniprot = namedex[name]
            try:
                protein.parse_uniprot()
                if 'transmembrane region' in protein.features:
                    candidates[protein.uniprot] = 'TM'
                elif len(protein) > 300 and 1 == 0: ##disabled.
                    candidates[protein.uniprot] = 'BIG'
                else:
                    stability = ProteinAnalysis(protein.sequence).instability_index()
                    if stability > 40:
                        protein.parse_swissmodel()
                        if protein.swissmodel:
                            candidates[protein.uniprot] = 'MODEL'
                        else:
                            candidates[protein.uniprot] = 'BINGO'
                            variants.append(protein)
                    else:
                        candidates[protein.uniprot] = 'UNSTABLE'
            except Exception as err:
                candidates[protein.uniprot] = 'ERROR'
                print(str(err))
        else:
            candidates[protein.uniprot] = 'ERROR'


    names = json.load(open('GEL_names.json'))
    ref = {m['uniprot']: m for m in csv.DictReader(open('tally.csv', 'r'))}
    candidates = {}
    variants = []
    Pool(200).map(ops, names)
    print(Counter(candidates.values()).most_common())
    for v in variants:
        print('| {uniprot} | {recommended_name} | {l} | {c}'.format(uniprot = v.uniprot,
                                                                    recommended_name= v.recommended_name,
                                                                    l=len(v),
                                                                    c=max([int(x) for x in ref[v.uniprot]['confidence_level'].split('|')])))

if __name__ == '__main__':
    redux()






