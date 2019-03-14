panels = Panel.get_list()
genes = Gene.get_list(True)

from collections import Counter
genetally = Counter([l.name for l in genes])

print(len(genetally.keys()))
print(genetally)
