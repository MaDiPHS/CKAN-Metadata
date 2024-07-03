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

import geopandas
from shapely.geometry import shape
from shapely import to_geojson
import json
from pathlib import Path

my_path = Path( __file__ ).parent.absolute()

# Please note that some countries are part of more than one region!
# Source: https:#en.wikipedia.org/wiki/Sub-Saharan_Africa#List_of_countries_and_regional_organisation and https:#en.wikipedia.org/wiki/North_Africa 
africa = {
    "regions": [
        {
        "name":"Central Africa", "countries":[
            "SSD", # South Sudan
            "AGO", # Angola
            "BDI", # Burundi
            "COD", # Democratic Republic of the Congo
            "RWA", # Rwanda
            "STP", # Sao Tome and Principe
            "CMR", # Cameroon
            "CAF", # The Central African Republic
            "TCD", # Chad
            "COG", # The Republic of the Congo
            "GNQ", # The Republic of Equatorial Guinea
            "GAB" # Gabon
            ]
        },
        {"name": "East Africa", "countries":[
            "SSD", # South Sudan
            "SOM", # Somalia
            "SOL", # Somaliland (not recognized, but countries.geojson has it as a separate feature. The SOL code is invented by me)
            "KEN", # Kenya
            "UGA", # Uganda
            "TZA", # Tanzania
            "ERI", # Eritrea
            "RWA", # Rwanda
            "BDI", # Burundi
            "DJI" # Djibouti
            ]
        },
        {"name": "Northeast Africa", "countries":[
            "SSD", # South Sudan
            "SDN", # Sudan
            "SOM", # Somalia
            "SOL", # Somaliland (not recognized, but countries.geojson has it as a separate feature. The SOL code is invented by me)
            "ETH", # Ethiopia
            "ERI", # Eritrea
            "DJI" # Djibouti
            ]
        },
        {"name": "Southeast Africa", "countries":[
            "BDI", # Burundi
            "KEN", # Kenya
            "RWA", # Rwanda
            "UGA", # Uganda
            "TZA" # Tanzania
            ]
        },
        {"name": "Southern Africa", "countries":[
            "AGO", # Angola
            "BWA", # Botswana
            "COM", # Comoros
            "SWZ", # Eswatini
            "LSO", # Lesotho
            "MDG", # Madagascar
            "MWI", # Malawi
            "MUS", # Mauritius
            "MOZ", # Mozambique
            "NAM", # Namibia
            "SYC", # Seychelles
            "ZAF", # South Africa
            "ZMB", # Zambia
            "ZWE" # Zimbabwe
            ]
        },
        {"name": "West Africa", "countries":[
            "CIV", # Ivory coast
            "GMB", # Gambia
            "GHA", # Ghana
            "GIN", # Guinea
            "LBR", # Liberia
            "MRT", # Mauritania
            "NGA", # Nigeria
            "SLE", # Sierra Leone
            "BEN", # Benin
            "BFA", # Burkina Faso
            "GNB", # Guinea-Bissau
            "MLI", # Mali
            "NER", # Niger
            "SEN", # Senegal
            "TGO" # Togo
            ]
        },
        {"name": "North Africa", "countries":[
            "DZA", # Algeria
            "EGY", # Egypt
            "LBY", # Libya
            "MAR", # Morocco
            "TUN", # Tunisia
            "ESH" # Western Sahara
            ]
        }
    ]
}

africa_super_regions = [
    {
        "name": "SSA", # Sub-Saharan Africa
        "regions": [
            "Central Africa",
            "East Africa",
            "Northeast Africa",
            "Southeast Africa",
            "Southern Africa",
            "West Africa"
        ]
    }
]

all_countries = None


def get_country_iso_codes(country_name_list:list)->list:
    country_codes = []
    for feature in get_all_countries():
        if feature["name"] in country_name_list:
            country_codes.append(feature["ISO_A3"])
    return country_codes
    
def get_super_region_country_codes(super_region_name:str)->list:
    country_codes = set()
    for super_region in africa_super_regions:
        if super_region["name"] == super_region_name:
            for region in super_region["regions"]:
                for r in africa["regions"]:
                    if r["name"] == region:
                        for country_code in r["countries"]:
                            country_codes.add(country_code)
    return country_codes

def get_africa_country_codes()->list:
    country_codes = set()
    for r in africa["regions"]:
        for country_code in r["countries"]:
            country_codes.add(country_code)
    return country_codes



def get_all_countries():
    global all_countries
    if all_countries == None:
        with open(f"{my_path}/countries.geojson") as geocountries:
            country_list = []
            countries = json.load(geocountries)
            for feature in countries["features"]:
                country_list.append({
                    "ISO_A3": feature["properties"]["ISO_A3"],
                    "name": feature["properties"]["ADMIN"]
                    })
        all_countries = country_list
    return all_countries


def get_country_list(country_codes):
    with open("countries.geojson") as geocountries:
        country_list = []
        countries = json.load(geocountries)
        for feature in countries["features"]:
            if feature["properties"]["ISO_A3"] in country_codes:
                country_list.append({
                    "ISO_A3": feature["properties"]["ISO_A3"],
                    "name": feature["properties"]["ADMIN"]
                    })
        return country_list

def get_countries_as_shapes(country_codes:list):
    with open("countries.geojson") as geocountries:
        shapes = []
        all_countries = json.load(geocountries)
        for feature in all_countries["features"]:
            if feature["properties"]["ISO_A3"] in country_codes:
                shapes.append(shape(feature["geometry"]))
        return shapes

def get_multi_country_geojson(country_codes:list):
    shape_list = get_countries_as_shapes(country_codes)
    s = geopandas.GeoSeries(shape_list)
    #union = s.unary_union
    union = s.union_all()
    fc = json.loads("""{"type":"FeatureCollection","features":[{"type":"Feature","properties":{}}]}""")
    mp = json.loads(to_geojson(union))
    fc["features"][0]["geometry"] = mp
    return fc



