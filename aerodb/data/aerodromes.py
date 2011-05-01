import json
import codecs
from collections import defaultdict


class Aerodromes(object):
    indexes = {'icao': defaultdict(list),
               'iata': defaultdict(list),
               'lid': defaultdict(list),
               'faa': defaultdict(list)}

    def __init__(self, aerodromes_file):
        with aerodromes_file:
            self.aerodromes = json.load(aerodromes_file)
        for aerodrome in self.aerodromes.values():
            for field in ['icao', 'iata', 'faa', 'lid']:
                if field in aerodrome:
                    self.indexes[field][aerodrome[field]].append(
                        aerodrome['airport'])

    def write(self, outfile):
        with outfile:
            json.dump(self.aerodromes, outfile, indent=2)
