#!/usr/bin/python3
"""
    Util script to simplify geocountries polygons 
    (https://github.com/datasets/geo-countries). The purpose is to
    reduce the amount of geospatial data stored for each dataset 

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


import os
import json
from dotenv import load_dotenv
from shapely.geometry import shape
import geojson

# This is needed to load any ENV settings from a .env (dotenv) file
# on your path
load_dotenv()

geocountries = json.load(open(os.getenv("GEO-COUNTRIES_PATH")))

# The maximum allowed geometry displacement. 
# The higher this value, the smaller the number 
# of vertices in the resulting geometry
# See: https://shapely.readthedocs.io/en/stable/reference/shapely.simplify.html
SIMPLIFICATION_TOLERANCE = 0.03

def get_country(country_code):
    for country in geocountries["features"]:
        if country["properties"]["ISO_A3"] == country_code:
            return country
    return None

def get_simplified_country(country_code):
    current_country = get_country(country_code)
    if current_country is not None:
        country_shape = shape(current_country["geometry"])
        simplified_country_shape = country_shape.simplify(SIMPLIFICATION_TOLERANCE)
        print(geojson.dumps(simplified_country_shape))

def get_simplified_geocountries():
    simplified_geocountries = {"type": "FeatureCollection", "features":[]}
    for country in geocountries["features"]:
        country_shape = shape(country["geometry"])
        simplified_country_shape = country_shape.simplify(SIMPLIFICATION_TOLERANCE)
        country["geometry"] = json.loads(geojson.dumps(simplified_country_shape))
        simplified_geocountries["features"].append(country)
    print(json.dumps(simplified_geocountries))

## What do you want to do?
#get_simplified_country("NOR")
get_simplified_geocountries()