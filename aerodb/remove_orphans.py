from aerodromes import Aerodromes


def remove_orphans(infile, outfile=None, dry_run=False):
    aerodromes = Aerodromes(infile)

    to_delete = []
    
    for key, aerodrome in aerodromes.aerodromes.iteritems():
        if not ('icao' in aerodrome or 'iata' in aerodrome or 'lid' in aerodrome or 'faa' in aerodrome):
            print aerodrome['name'] + " has no codes"
            to_delete.append(key)

    if not dry_run:
        for key in to_delete:
            print "Deleting", aerodromes.aerodromes[key]['name']
            del aerodromes.aerodromes[key]
        aerodromes.write(outfile)

remove_orphans("aerodromes-dedup.json", "aerodromes-audited.json", False)
