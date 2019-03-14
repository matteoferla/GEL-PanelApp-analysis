import urllib.request, json, os, pprint
from warnings import warn
from collections import defaultdict


class _APIInterface:
    """
    Inherited by Panel and Gene
    """
    _list_outfile = 'error.json' #tobeoverridden
    _list_url = 'localhost' #tobeoverridden
    _mapping = {}

    def __init__(self, paneldex):

        def defaults(key, default=None):
            if key in paneldex:
                return paneldex[key]
            elif self._mapping[key] in paneldex:
                return paneldex[self._mapping[key]]
            else:
                return default

        # verify not already parsed.
        if self.__class__ == paneldex.__class__:
            self.__dict__ = paneldex.__dict__
        else: # parse
            self._data = paneldex
            for k in self._mapping.keys():
                setattr(self, k, defaults(k))

    @classmethod
    def _fetch_list_query(cls, this_url):
        with urllib.request.urlopen(this_url) as url:
            data = json.loads(url.read().decode())
        return data

    @classmethod
    def _get_list(cls):
        """
        Returns a list of all dictionaries form webservices, not the api.
        :return:
        """
        if os.path.isfile(cls._list_outfile):  ## load
            data = json.load(open(cls._list_outfile))
        else:  ##fetch
            # differs from https://panelapp.genomicsengland.co.uk/api/docs/
            this_url = cls._list_url
            done = False
            data = {}
            while not done:
                new_data = cls._fetch_list_query(this_url)
                ### assert no error
                if len(new_data.keys())== 0 and 'detail' in data:
                    raise ValueError('Error in page retrieval')
                ### load data
                for k in new_data.keys():
                    if k in data:
                        if isinstance(data[k], list):
                            data[k].extend(new_data[k])
                        elif isinstance(data[k], str):
                            data[k] += str(new_data[k])
                        else:
                            warn('Unknown type {t} for key {k}'.format(t=type(data[k]).__name__,k=k))
                    else:
                        data[k] = new_data[k]
                ### proceed
                if 'next' in new_data and new_data['next']:  ##the last one is None/null.
                    print('Next', new_data['next'])
                    this_url = new_data['next']
                else:
                    done = True
            json.dump(data, open(cls._list_outfile, 'w'))
        return data


    def __str__(self):
        return pprint.pformat({k: v for (k,v) in self.__dict__.items() if type(v).__name__ != 'method' and k != '_data'})


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



class Panel(_APIInterface):
    """
    Inherits __init___ and classmethod _get_list
    """
    _list_outfile = 'list_panels.json'
    _list_url = 'https://panelapp.genomicsengland.co.uk/WebServices/list_panels/?format=json'
    _mapping = {'name': 'Name',
               'id':'Panel_Id',
               'disease_group': 'DiseaseGroup',
               'disease_sub_group': 'DiseaseSubGroup',
               'status': 'status',
               'relevant_disorders': 'Relevant_disorders',
               'n_genes':'Number_of_Genes',
               'types': 'PanelTypes'}

    @classmethod
    def get_list(cls):
        return [cls(p) for p in cls._get_list()['result']]



