from aerodb.data.aerodromes import Aerodromes

def duplicate_report(infile, outfile):
    aerodromes = Aerodromes(infile)
    duplicates = set()

    for code_index in aerodromes.indexes.values():
        for v in code_index.values():
            if len(v) > 1:
                for aerodrome in v:
                    duplicates.add(aerodrome)

    with outfile:
        cw = UnicodeWriter(outfile)
        fields = ['name', 'icao', 'iata', 'faa', 'lid', 'airport']
        cw.writerow(fields)

        for aerodrome in duplicates:
            cw.writerow(
                [aerodromes.aerodromes[aerodrome].get(f,
                                                      '') for f in fields])


def duplicate_summary(infile):
    aerodromes = Aerodromes(infile)

    for code_type, code_index in aerodromes.indexes.iteritems():
        for k, v in code_index.iteritems():
            if len(v) > 1:
                print "%s code %s is assigned to %i aerodromes:" % (code_type.upper(),
                                                                    k, len(v))
                for aerodrome in v:
                    print aerodromes.aerodromes[aerodrome]['name']
                    print '\t', aerodromes.aerodromes[aerodrome]['airport']
                print
