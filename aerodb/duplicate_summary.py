from aerodb.data.aerodromes import Aerodromes


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
