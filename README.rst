Introduction
============

Aerodrome data has historically been closely guarded, licensed only on a subscription basis as part of various proprietary data sets.  However, there are many projects which benefit from having at least a minimal data set—aerodrome names, identifiers, and locations.  Wikipedia editors have compiled this information for many aerodromes, and the DBpedia project can be used to query this information programmatically.  This project aims to provide a suitable SPARQL query for extracting aerodrome information from Wikipedia via DBpedia, as well as post-processing tools.

Constraints
===========

There are certain constraints applied in this project. They are:

* Where ICAO codes and Transport Canada location identifiers clash, the ICAO code is preferred
* Where IATA codes and FAA location identifiers clash, the IATA code is preferred
* If there are no codes for an aerodrome, it is not included in the output
* If there is no location for an aerodrome, it is not included in the output

Duplicates
==========

The Wikipedia data returned by the query contains duplicates for certain codes. ICAO, FAA, and Transport Canada identifiers are not multiply assigned, and duplicates should be eliminated.  IATA maintains a policy of 'controlled duplication' with respect to aerodrome identifiers. This package includes a file of 'preferences' which are used to eliminate duplicates. The following rules are followed in developing the preferences file:

* Where a civil and military facility share the same code but are listed in separate Wikipedia articles, the civil facility is preferred
* Where a code has been transferred from a deactivated aerodrome to a new aerodrome, the new aerodrome is preferred
* Where there are multiple articles for the same aerodrome (possibly using different names), the article which uses the correct name for the aerodrome and/or provides the most (sourced) information is preferred

These rules can be applied without modification for ICAO, FAA, and Transport Canada identifiers. However, for IATA identifiers, it is necessary to distinguish between legitimate duplicates caused by the IATA's 'controlled duplication' policy, and duplicates caused by the factors listed above.

What Wikipedians can do
=======================

* Ensure that every active aerodrome has only one article. In some cases, this will be simple—merge and redirect as needed. In other cases, there may be naming disputes, conflicts over the correct name of an aerodrome, etc. There is also a particularly thorny problem which exists when a civil and military facility share the same physical aerodrome, and thus the same identifiers. These are generally listed in entirely separate Wikipedia articles, which results in duplicate listings for those aerodrome identifiers. This requires manual untangling.
* Ensure that defunct and deactivated aerodromes are treated correctly. It is perfectly acceptable for defunct and deactivated aerodromes to have Wikipedia articles, but their identifiers should not be listed in the ``{{Infobox airport}}``.  This is particularly critical in the case of identifiers which have been transferred to an aerodrome from a deactivated aerodrome—if both articles have the same identifiers listed in their ``{{Infobox airport}}``, then duplicate listings will result, which must be manually corrected to ensure that the current aerodrome is the one which is listed.

Using aerodb
============

aerodb requires Python 2.7 or later (but not Python 3), with SPARQLWrapper installed (``easy_install SPARQLWrapper``).

To generate an aerodrome database dump:

#. ``python manage.py fetch aerodromes.json``
#. ``python manage.py duplicate_report aerodromes.json duplicates.csv``
#. Examine the duplicates report (in ``duplicates.csv``) and update the preferences file in ``preferences.csv`` as needed.
#. ``python manage.py apply_preferences preferences.csv aerodromes.json - | python manage.py cleanup - aerodromes-dedup.json``

``aerodromes-dedup.json`` is now ready for use.  To produce a CSV or KML export, run:

* ``$ python manage.py export -f kml aerodromes-dedup.json aerodromes.kml``
* ``$ python manage.py export -f csv aerodromes-dedup.json aerodromes.csv``