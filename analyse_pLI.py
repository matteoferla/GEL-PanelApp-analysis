#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__doc__ = \
    """
    This uses data from Protein class from SNV analyser (VENUS).
    NB. Written for python 3, not tested under 2.
    
    gene.mode_of_inheritance is an enum (not implement as such here nor serverside given BiALLELIC dubplication) of values: {'', 'X-LINKED: hemizygous mutation in males, monoallelic mutations in females may cause disease (may be less severe, later onset than males)', 'MONOALLELIC, autosomal or pseudoautosomal, imprinted status unknown', 'MITOCHONDRIAL', 'Other - please specifiy in evaluation comments', 'MONOALLELIC, autosomal or pseudoautosomal, paternally imprinted (maternal allele expressed)', 'Other - please specify in evaluation comments', 'BIALLELIC, autosomal or pseudoautosomal', 'BiALLELIC, autosomal or pseudoautosomal', 'X linked: hemizygous mutation in males, monoallelic mutations in females may cause disease (may be less severe, later onset than males)', 'X-LINKED: hemizygous mutation in males, biallelic mutations in females', 'Unknown', 'BOTH monoallelic and biallelic (but BIALLELIC mutations cause a more SEVERE disease form), autosomal or pseudoautosomal', 'MONOALLELIC, autosomal or pseudoautosomal, NOT imprinted', 'MONOALLELIC, autosomal or pseudoautosomal, maternally imprinted (paternal allele expressed)', 'MONOALLELIC, autosomal or pseudoautosomal, paternally imprinted (maternal allele expressed) ', 'x-linked over-dominance', 'Other', 'BOTH monoallelic and biallelic, autosomal or pseudoautosomal', 'MONOALLELIC, autosomal or pseudoautosomal'}
    {'', 'BIALLELIC,', 'MONOALLELIC,', 'MITOCHONDRIAL', 'X-LINKED:', 'Other', 'Unknown', 'X', 'BOTH', 'BiALLELIC,', 'x-linked'}
    
    
    """

from panelWrapper import Gene, Panel
import csv

genedex = Gene.get_dict()
print({genedex[genename][0].mode_of_inheritance.split(' ')[0] for genename in genedex})

pli = {row['gene_name']: row for row in csv.DictReader(open('GEL_pLI.csv'))}

bag = {}

with open('list tally.csv','w',newline='') as w:
    sheet = csv.DictWriter(w,('name','mode','pLI','pRec','pNull','ExAC_type'),extrasaction='ignore')
    sheet.writeheader()
    for genename in genedex:
        data = {}
        if genename in pli:
            if float(pli[genename]['pLI']) == -1:
                continue
            data['pLI'] = float(pli[genename]['pLI'])
            data['pRec'] = float(pli[genename]['pRec'])
            data['pNull'] = float(pli[genename]['pNull'])
            data['len'] = pli[genename]['sequence']
            data['pfam'] = pli[genename]['pfam']
            if data['pLI'] < 0:  # error.
                data['ExAC_type'] = 'Unknown'
            elif data['pLI'] > max(data['pRec'], data['pNull']):
                data['ExAC_type'] = 'Dominant'
            elif data['pRec'] > max(data['pLI'], data['pNull']):
                data['ExAC_type'] = 'Recessive'
            elif data['pNull'] > max(data['pLI'], data['pRec']):
                data['ExAC_type'] = 'None'
            else:
                data['ExAC_type'] = 'Unknown'
        else:
            print('OOODD')
            print(genename)
            continue

        for mode in sorted({g.clean_inheritance() for g in genedex[genename]}):
            sheet.writerow({'name':genename,
                            'mode': mode,
                            **data})

