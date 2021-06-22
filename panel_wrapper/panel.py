from .api_interface import _APIInterface

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