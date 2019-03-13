from panelWrapper import Gene,Panel

import csv


genes = Gene.get_list(True)

from collections import Counter
genenames = Counter([l.name for l in genes])
print(genenames)
