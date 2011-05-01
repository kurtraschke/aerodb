import csv
from collections import defaultdict


class Preferences(object):
    indexes = {'icao': defaultdict(list),
               'iata': defaultdict(list),
               'lid': defaultdict(list),
               'faa': defaultdict(list)}

    def __init__(self, preferences_file):
        with preferences_file:
            preferences = csv.DictReader(preferences_file)
            for aerodrome in preferences:
                for field in ['icao', 'iata', 'faa', 'lid']:
                    if field in aerodrome:
                        self.indexes[field][aerodrome[field]].append(
                            aerodrome['airport'])

    def find_preferred(self, field, code):
        return self.indexes[field].get(code, None)
