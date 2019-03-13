import urllib.request, json, os, pprint


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
    def _get_list(cls):
        """
        Returns a list of all dictionaries form webservices, not the api.
        :return:
        """
        if os.path.isfile(cls._list_outfile):  ## load
            data = json.load(open(cls._list_outfile))
        else:  ##fetch
            # differs from https://panelapp.genomicsengland.co.uk/api/docs/
            with urllib.request.urlopen(cls._list_url) as url:
                data = json.loads(url.read().decode())
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
        return [cls(g) for g in data['results']]



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



