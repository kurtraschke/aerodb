import xml.etree.ElementTree as etree

from aerodb.util.ucsv import UnicodeWriter
from aerodb.data.aerodromes import Aerodromes

def export_kml(aerodromes, outfile):
    kml = etree.Element("{http://www.opengis.net/kml/2.2}kml")
    folder = etree.SubElement(kml, "{http://www.opengis.net/kml/2.2}Folder")
    foldername = etree.SubElement(folder, "{http://www.opengis.net/kml/2.2}name")
    foldername.text = "Aerodromes"

    for aerodrome in aerodromes.values():
        placemark = etree.Element("{http://www.opengis.net/kml/2.2}Placemark")
        name = etree.SubElement(placemark, "{http://www.opengis.net/kml/2.2}name")
        name.text=aerodrome['name']
        description = etree.SubElement(placemark, "{http://www.opengis.net/kml/2.2}description")
        description.text='<a href="%s">%s</a>' % (aerodrome['airport'],
                                                  aerodrome['name'])
        point = etree.SubElement(placemark, "{http://www.opengis.net/kml/2.2}Point")
        coordinates = etree.SubElement(point, "{http://www.opengis.net/kml/2.2}coordinates")
        coordinates.text="%s,%s" % (aerodrome['location']['coordinates'][0],
                                    aerodrome['location']['coordinates'][1])
        folder.append(placemark)

    with outfile:
        et = etree.ElementTree(kml)
        et.write(outfile)

def export_csv(aerodromes, outfile):
    with outfile:
        cw = UnicodeWriter(outfile)
        fields = ['name', 'icao', 'iata', 'faa', 'lid', 'latitude', 'longitude', 'airport']
        cw.writerow(fields)

        for aerodrome in aerodromes.values():
            aerodrome['latitude'] = aerodrome['location']['coordinates'][1]
            aerodrome['longitude'] = aerodrome['location']['coordinates'][0]
            cw.writerow([aerodrome.get(f,'') for f in fields])

def export(infile, outfile, type):
    exporters = {'kml': export_kml,
                 'csv': export_csv}

    with infile:
        aerodromes = Aerodromes(infile)

    exporters[type](aerodromes.aerodromes, outfile)
