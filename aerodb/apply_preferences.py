"""Apply CSV preferences"""

from preferences import Preferences
from aerodromes import Aerodromes


def apply_preferences(infile, outfile, dry_run=False):
    preferences = Preferences()
    aerodromes = Aerodromes(filename=infile)

    def zap(candidate_aerodromes, choice, field):
        for aerodrome in candidate_aerodromes:
            if aerodrome != choice:
                print "Removing", field, "from", aerodrome
                if not dry_run:
                    del aerodromes.aerodromes[aerodrome][field]

    for field, aerodrome_list in aerodromes.indexes.iteritems():
        for code, aerodromes_for_code in aerodrome_list.iteritems():
            if len(aerodromes_for_code) > 1:
                pref = preferences.find_preferred(field, code)
                if pref is not None:
                    zap(aerodromes_for_code, pref, field)

    aerodromes.write(outfile)

apply_preferences("aerodromes.json", "aerodromes-dedup.json")
