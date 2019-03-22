__doc__ = """
I really don't like that 52% without a match. How many have high confidence?
"""

import csv
from collections import Counter
from pprint import PrettyPrinter
pprint = PrettyPrinter().pprint
import json
'''
genes={m['uniprot']: m for m in csv.DictReader(open('tally.csv','r'))}

confdex = Counter([max([int(x) for x in genes[u]['confidence_level'].split('|')]) for u in genes if genes[u]['%modelled'] == '0'])
refdex = Counter([max([int(x) for x in genes[u]['confidence_level'].split('|')]) for u in genes])

print(confdex.most_common())
print(refdex.most_common())

con4 = [(u,genes[u]['name'],genes[u]['full_name']) for u in genes if genes[u]['%modelled'] == '0' and '4' in genes[u]['confidence_level']]
#pprint(con4)

#ordered sub-300AA con-4 non-TM unchar
# for the non-TM and ordered I need the protein module...
i = 0
for u in genes:
    if genes[u]['len'] and int(genes[u]['len']) < 300 and genes[u]['%modelled'] == '0' and '4' in genes[u]['confidence_level']:
        print(u)
        i+=1
print(i)
'''


raise NotImplementedError


