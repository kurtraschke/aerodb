import json
import codecs
from collections import defaultdict

class Aerodromes(object):
    indexes = {'icao': defaultdict(list),
               'iata': defaultdict(list),
               'lid': defaultdict(list),
               'faa': defaultdict(list)}

    def __init__(self, filename):
        self.aerodromes = json.load(codecs.open(filename, 'r', 'utf-8'))
        for aerodrome in self.aerodromes.values():
            for field in ['icao', 'iata', 'faa', 'lid']:
                if field in aerodrome:
                    self.indexes[field][aerodrome[field]].append(aerodrome['airport'])

    def write(self, filename):
        json.dump(self.aerodromes,
                  codecs.open(filename, 'w',  'utf-8'),
                  ensure_ascii=False,
                  indent=2)
