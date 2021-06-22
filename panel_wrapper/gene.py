from collections import defaultdict

from .api_interface import _APIInterface

class Gene(_APIInterface):
    """
    Inherits __init___ and classmethod _get_list
    """
    _list_outfile = 'list_gene.json'
    _list_url = 'https://panelapp.genomicsengland.co.uk/api/v1/genes/?format=json'
    _mapping = {'gene_data': 'gene_data',
                'type': 'entity_type',
                'name': 'entity_name',
                'confidence_level': 'confidence_level',
                'penetrance': 'penetrance',
                'mode_of_pathogenicity': 'mode_of_pathogenicity',
                'publications': 'publications',
                'evidence': 'evidence',
                'phenotypes': 'phenotypes',
                'mode_of_inheritance': 'mode_of_inheritance',
                'tags': 'tags',
                'panel':'panel'
                }

    def clean_inheritance(self):
        if not self.mode_of_inheritance:
            return 'NA'
        return self.mode_of_inheritance.replace(':', ' ').replace(',', ' ').split(' ')[0].title()

    def __init__(self, dex):
        super().__init__(dex)
        self.confidence_level = int(self.confidence_level)

    def to_flat_dict(self):
        data = {v: getattr(self, v) for v in self._mapping.values() if hasattr(self, v)}
        data['confidence_level'] = int(self.confidence_level)
        for v in self.gene_data:
            data['gene-' + v] = self.gene_data[v]
        for v in self.panel:
            data['panel-' + v] = self.panel[v]
        del data['panel']
        del data['gene_data']
        return data

    @classmethod
    def get_list(cls, verbose=False):
        data = cls._get_list()
        if verbose:
            print('Count',data['count'])
            if 'next' in data:
                print('Next', data['next'])
            if 'prev' in data:
                print('Prev', data['prev'])
        assert data['count'] == len(data['results']), 'There are {0} genes. There should be {1}.'.format(data['count'], len(data['results']))
        return [cls(g) for g in data['results']]

    @classmethod
    def get_dict(cls):
        genedex = defaultdict(list)
        data = cls.get_list()
        for gene in data:
            genedex[gene.name].append(gene)
        return genedex

    @classmethod
    def get_df(cls):
        import pandas as pd
        return pd.DataFrame([gene.to_flat_dict() for gene in cls.get_list()])

