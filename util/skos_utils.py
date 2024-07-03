#!/usr/bin/python3

"""
    Copyright (C) 2024 NIBIO

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import rdflib
from pathlib import Path

my_path = Path( __file__ ).parent.absolute()

graph = rdflib.Graph()
graph.parse("%s/../vocabularies/madiphs_skos.rdf" % my_path, format="application/rdf+xml")

PESTS_SCHEME = "https://gd.eppo.int/taxon/pest"
CROPS_SCHEME = "https://rd.madiphs.net/scheme/common-crops"


#print(graph)

def get_concepts_in_scheme(scheme, language):
    """ 
    Using SPARQL https://www.w3.org/TR/rdf-sparql-query/
    """

    q = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT ?concept ?prefLabel
    WHERE {
        ?concept skos:inScheme <%s> . 
        ?concept skos:prefLabel ?prefLabel .
        FILTER(langMatches(lang(?prefLabel), "%s"))
    }

    """ % (scheme,language)
    results = graph.query(q)
    #print(results)
    scheme_concepts = []
    for result in results:
        #print(result)
        scheme_concepts.append({
            "id":result["concept"].toPython(),
            "name": result["prefLabel"].toPython()
            })
        #print("%s %s" % (result["concept"], result["prefLabel"]))
    return scheme_concepts

def get_concepts_in_scheme_with_concept_as_key(scheme, language):
    concepts_list = get_concepts_in_scheme(scheme,language)
    retval = {}
    for concept in concepts_list:
        retval[concept["id"]] = concept["name"]
    return retval

def get_concepts_in_scheme_with_label_as_key(scheme, language):
    concepts_list = get_concepts_in_scheme(scheme,language)
    retval = {}
    for concept in concepts_list:
        retval[concept["name"]] = concept["id"]
    return retval

def get_concepts_in_scheme_with_lowercase_label_as_key(scheme, language):
    concepts_list = get_concepts_in_scheme(scheme,language)
    retval = {}
    for concept in concepts_list:
        retval[concept["name"].lower()] = concept["id"]
    return retval

#for crop in get_concepts_in_scheme("https://rd.madiphs.net/scheme/common-crops","EN"):
#    print("%s %s" % (crop["id"], crop["name"]))

#for crop in get_concepts_in_scheme("https://gd.eppo.int/taxon/pest","NY"):
#    print("%s %s" % (crop["id"], crop["name"]))
