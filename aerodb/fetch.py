import urlparse
import urllib
import json
import codecs

from SPARQLWrapper import SPARQLWrapper, JSON

query = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?name ?icao ?iata ?faa ?lid ?latitude ?longitude ?airport
FROM <http://dbpedia.org>
WHERE {
    ?airport rdf:type <http://dbpedia.org/ontology/Airport> .

    OPTIONAL {
        ?airport dbo:icaoLocationIdentifier ?icao .
        FILTER regex(?icao, "^[A-Z0-9]{4}$")
    }

    OPTIONAL {
        ?airport dbo:iataLocationIdentifier ?iata .
        FILTER regex(?iata, "^[A-Z0-9]{3}$")
    }

    OPTIONAL {
        ?airport dbo:locationIdentifier ?lid .
        FILTER regex(?lid, "^[A-Z0-9]{4}$")
        FILTER (!bound(?icao) || (bound(?icao) && (?icao != ?lid)))
        OPTIONAL {
            ?airport_y rdf:type <http://dbpedia.org/ontology/Airport> .
            ?airport_y dbo:icaoLocationIdentifier ?other_icao .
            FILTER (bound(?lid) && (?airport_y != ?airport && ?lid = ?other_icao))
        }
        FILTER (!bound(?other_icao))
    }

    OPTIONAL {
        ?airport dbo:faaLocationIdentifier ?faa .
        FILTER regex(?faa, "^[A-Z0-9]{3}$")
        FILTER (!bound(?iata) || (bound(?iata) && (?iata != ?faa)))
        OPTIONAL {
            ?airport_x rdf:type <http://dbpedia.org/ontology/Airport> .
            ?airport_x dbo:iataLocationIdentifier ?other_iata .
            FILTER (bound(?faa) && (?airport_x != ?airport && ?faa = ?other_iata))
        }
        FILTER (!bound(?other_iata))
    }

    FILTER (bound(?icao) || bound(?iata) || bound(?faa) || bound(?lid))

    OPTIONAL {
        ?airport rdfs:label ?name
        FILTER (lang(?name) = "en")
    }

    {
        ?airport geo:lat ?latitude .
        ?airport geo:long ?longitude .
        FILTER (datatype(?latitude) = xsd:float)
        FILTER (datatype(?longitude) = xsd:float)
    } UNION {
        ?airport geo:lat ?latitude .
        ?airport geo:long ?longitude .
        FILTER (datatype(?latitude) = xsd:double)
        FILTER (datatype(?longitude) = xsd:double)
        OPTIONAL {
            ?airport geo:lat ?lat_f .
            ?airport geo:long ?long_f .
            FILTER (datatype(?lat_f) = xsd:float)
            FILTER (datatype(?long_f) = xsd:float)
        }
        FILTER (!bound(?lat_f) && !bound(?long_f))
    }
}
ORDER BY ?airport OFFSET %i LIMIT %i
"""

def fetch_aerodromes():
   
    limit = 500

    aerodromes = {}

    def fetchResults(offset):
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery(query % (offset, limit))
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
            values = dict([(key, value['value']) for key, value \
                           in result.items()])
            values['location'] = {"type": "Point",
                                  "coordinates": [values['longitude'],
                                                  values['latitude']]}
            del values['longitude']
            del values['latitude']

            if 'name' not in values:
                values['name'] = urllib.unquote(urlparse.urlparse(
                        values['airport']).path.decode(
                        'utf-8').split('/')[-1]).replace('_', ' ')

            aerodromes[values['airport']] = values

        if len(results["results"]["bindings"]) == limit:
            fetchResults(offset + limit)

    fetchResults(0)

    return aerodromes

results = fetch_aerodromes()
print len(results)
json.dump(results, codecs.open('aerodromes.json', 'w',  'utf-8'), ensure_ascii=False, indent=2)
