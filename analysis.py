from panelWrapper import Gene, Panel

import csv, json

#panels = Panel.get_list()
genedex = Gene.get_dict()

print(genedex['FOXN1'][0])
print('******')

## load gene to uniprot json (overkill here)
namedex=json.load(open('human_prot_namedex.json'))

## save
with open('tally.csv','w',newline='') as w:
    sheet=csv.DictWriter(w, fieldnames=('name','full_name','tally','panel', 'ensembl','location', 'uniprot','tags','OMIM','panels','disease_group','disease_sub_group','mode_of_inheritance'))
    sheet.writeheader()
    for gene in genedex:
        try:
            data = {'name': gene, 'tally': len(genedex[gene])}
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
                data['OMIM'] = '|'.join(genedex[gene][0].gene_data['omim_gene'])
            data['panels']='|'.join({str(gene.panel['id']) if gene.panel['id'] else 'NA' for gene in genedex[gene]})
            data['disease_group'] =  '|'.join({gene.panel['disease_group'] if gene.panel['disease_group'] else 'NA' for gene in genedex[gene]})
            data['disease_sub_group'] = '|'.join({gene.panel['disease_sub_group'] if gene.panel['disease_sub_group'] else 'NA' for gene in genedex[gene]})
            data['mode_of_inheritance'] = '|'.join({gene.mode_of_inheritance if gene.mode_of_inheritance else 'NA' for gene in genedex[gene]})
            sheet.writerow(data)
        except NotImplementedError as err: ### change to Exception to activate
            sheet.writerow(data)
            print('****** ERROR ******')
            print(str(err))
            print(genedex[gene][0])
            print('****** ERROR END ******')

