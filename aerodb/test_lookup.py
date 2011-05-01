from pprint import pprint
from itertools import chain

from aerodb.data.aerodromes import Aerodromes

def test_lookup(infile, code, type=None):
    aerodromes = Aerodromes(infile)

    if type is not None:
        pprint([aerodromes.aerodromes[a] for a in aerodromes.indexes[type][code]])
    else:
        pprint([aerodromes.aerodromes[a] for a in chain.from_iterable(
            [index[code] for index in aerodromes.indexes.values()])])
