import logging

from aerodb.data.aerodromes import Aerodromes
from aerodb.duplicates import mark_iata_duplicates

def cleanup(infile, outfile=None, dry_run=False):
    aerodromes = Aerodromes(infile)
    mark_iata_duplicates(aerodromes)
    
    to_delete = []

    for key, aerodrome in aerodromes.aerodromes.iteritems():
        if not ('icao' in aerodrome or 'iata' in aerodrome or 'lid' in aerodrome or 'faa' in aerodrome):
            logging.info("%s has no codes" % (aerodrome['name']))
            to_delete.append(key)

    if not dry_run:
        for key in to_delete:
            logging.warn("Deleting %s" % (aerodromes.aerodromes[key]['name']))
            del aerodromes.aerodromes[key]
        aerodromes.write(outfile)
