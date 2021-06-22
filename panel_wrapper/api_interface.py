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
        self.raw_data = paneldex
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
                            warn('Unknown type {t} for key {k}'.format(t=type(data[k]).__name__, k=k))
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

    @property
    def unexpected_keys(self):
        return set(self.raw_data.keys()) - set(self._mapping.values())

    def __str__(self):
        return pprint.pformat({k: v for (k,v) in self.__dict__.items() if type(v).__name__ != 'method' and k != '_data'})
