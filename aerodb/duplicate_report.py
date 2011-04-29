from ucsv import UnicodeWriter
from aerodromes import Aerodromes


def generate_duplicate_report(infile, outfile):
    aerodromes = Aerodromes(filename=infile)
    duplicates = set()

    for code_index in aerodromes.indexes.values():
        for v in code_index.values():
            if len(v) > 1:
                for aerodrome in v:
                    duplicates.add(aerodrome)

    cw = UnicodeWriter(open('duplicates.csv','wb'))

    fields = ['name','icao','iata','faa','lid','airport']

    cw.writerow(fields)

    for aerodrome in duplicates:
        cw.writerow([aerodromes.aerodromes[aerodrome].get(f, '') for f in fields])

generate_duplicate_report("aerodromes-dedup.json", "duplicates.csv")
