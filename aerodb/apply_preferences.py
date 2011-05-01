"""Apply CSV preferences"""
import logging


from aerodb.data.preferences import Preferences
from aerodb.data.aerodromes import Aerodromes


def apply_preferences(preferences, infile, outfile, dry_run=False):
    preferences = Preferences(preferences)
    aerodromes = Aerodromes(infile)

    def zap(candidate_aerodromes, choice, field):
        for aerodrome in candidate_aerodromes:
            if aerodrome != choice:
                logging.info("Removing %s from %s" % (field, aerodrome))
                if not dry_run:
                    del aerodromes.aerodromes[aerodrome][field]

    for field, aerodrome_list in aerodromes.indexes.iteritems():
        for code, aerodromes_for_code in aerodrome_list.iteritems():
            if len(aerodromes_for_code) > 1:
                pref = preferences.find_preferred(field, code)
                if pref is not None:
                    zap(aerodromes_for_code, pref, field)

    if not dry_run:
        aerodromes.write(outfile)
