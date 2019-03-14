from panelWrapper import Gene,Panel

import csv

import json

panels = Panel.get_list()
genes = Gene.get_list(True)

### assert
raw = json.load(open('list_gene.json'))


from collections import Counter
genetally = Counter([l.name for l in genes])

print(len(genetally.keys()))
print(genetally)

with open('tally.csv','w',newline='') as w:
    sheet=csv.DictWriter(w, fieldnames=('name','tally','panel'))
    sheet.writeheader()
    for gene in genes:
        sheet.writerow({'name': gene.name,
                        'tally': genetally[gene.name]})

