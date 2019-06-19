#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__doc__ = \
    """
    Here I make a file to take stock of the genes needed.
    Making a file called tally.csv
    NB. Written for python 3, not tested under 2.
    """

from panelWrapper import Gene, Panel

import csv, json

panels = Panel.get_list()
genedex = Gene.get_dict()

print('number of panels: {0}'.format(len(panels)))
print('number of unique genes: {0}'.format(len(genedex)))
print('******')

## load gene to uniprot json (overkill here)
namedex=json.load(open('human_prot_namedex.json'))

# data folder is too big to copy
#from protein import Protein
# parsed there.
pli = {row['gene_name']: row for row in csv.DictReader(open('GEL_pLI.csv'))}



## analyse.
with open('tally.csv','w',newline='') as w:
    sheet=csv.DictWriter(w, fieldnames=('name','full_name','tally','panel', 'ensembl','location', 'uniprot','tags','OMIM','panels','panel_names','disease_group','disease_sub_group','mode_of_inheritance','confidence_level', 'len','pfam', 'pLI', 'pRec', 'pNull','ExAC_type'))
    sheet.writeheader()
    for gene in genedex:
        data = {'name': gene, 'tally': len(genedex[gene])}
        try:
            ### build
            if 'GRch38' in genedex[gene][0].gene_data['ensembl_genes']:
                data['ensembl'] = genedex[gene][0].gene_data['ensembl_genes']['GRch38']['90']['ensembl_id']
                data['location'] = '(build: 38)' + genedex[gene][0].gene_data['ensembl_genes']['GRch38']['90']['location']
            elif 'GRch37' in genedex[gene][0].gene_data['ensembl_genes']:
                data['ensembl'] = genedex[gene][0].gene_data['ensembl_genes']['GRch37']['82']['ensembl_id']
                data['location'] = '(build: 38)' + genedex[gene][0].gene_data['ensembl_genes']['GRch37']['82']['location']
            else:
                pass #'tags': ['locus-type-phenotype-only'],
            ### uniprot
            if gene not in namedex:
                data['uniprot'] = 'Error'
            else:
                data['uniprot'] = namedex[gene]
            ### tags
            data['tags'] = '|'.join(genedex[gene][0].tags)
            data['full_name'] = genedex[gene][0].gene_data['gene_name']
            if genedex[gene][0].gene_data['omim_gene']:
                data['OMIM'] = '|'.join(sorted(genedex[gene][0].gene_data['omim_gene']))
            data['panels']='|'.join(sorted({str(g.panel['id']) if g.panel['id'] else 'NA' for g in genedex[gene]}))
            data['disease_group'] =  '|'.join(sorted({g.panel['disease_group'] if g.panel['disease_group'] else 'NA' for g in genedex[gene]}))
            data['disease_sub_group'] = '|'.join(sorted({g.panel['disease_sub_group'] if g.panel['disease_sub_group'] else 'NA' for g in genedex[gene]}))
            data['mode_of_inheritance'] = '|'.join(sorted({g.clean_inheritance() for g in genedex[gene]}))
            data['confidence_level'] = '|'.join(sorted({g.confidence_level if g.confidence_level else 'NA' for g in genedex[gene]}))
            data['panel_names'] = '|'.join(sorted({str(g.panel['name']) if g.panel['id'] else 'NA' for g in genedex[gene]}))
            ##pLI
            if gene in pli:
                data['pLI'] = pli[gene]['pLI']
                data['pRec'] = pli[gene]['pRec']
                data['pNull'] = pli[gene]['pNull']
                data['len'] = pli[gene]['sequence']
                data['pfam'] = pli[gene]['pfam']
                if pli[gene]['pLI'] < 0:  # error.
                    data['ExAC_type'] = 'Unknown'
                elif pli[gene]['pLI'] > max(pli[gene]['pRec'], pli[gene]['pNull']):
                    data['ExAC_type'] = 'Dominant'
                elif pli[gene]['pRec'] > max(pli[gene]['pLI'], pli[gene]['pNull']):
                    data['ExAC_type'] = 'Recessive'
                elif pli[gene]['pNull'] > max(pli[gene]['pLI'], pli[gene]['pRec']):
                    data['ExAC_type'] = 'None'
                else:
                    data['ExAC_type'] = 'Unknown'
            sheet.writerow(data)

        except NotImplementedError as err: ### change to Exception to activate
            sheet.writerow(data)
            print('****** ERROR ******')
            print(str(err))
            print(genedex[gene][0])
            print('****** ERROR END ******')

