#!/usr/bin/python3

"""
    Util script to import knowledge products datasets from the Excel
    spreadsheets produced by CABI
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

import csv
from dateutil.parser import parse, ParserError
import requests
import validators
import os
from dotenv import load_dotenv

# This code started out by studying this example: https://docs.ckan.org/en/2.9/api/#example-importing-datasets-with-the-ckan-api

# This is needed to load any ENV settings from a .env (dotenv) file
# on your path
load_dotenv()
# This API key can be obtained by logging into ckan.madiphs.org 
api_key=os.getenv("CKAN_API_KEY")

# ckanext-scheming dataset type
scheming_type = "plant-health-knowledge-product"

# Lookup dicts for validation and data conversion from text to category
crop_dict = {
    "maize": "https://gd.eppo.int/taxon/ZEAMX",
    "tomato": "https://gd.eppo.int/taxon/LYPES",
    "groundnut": "https://gd.eppo.int/taxon/ARHHY",
    "soybean": "https://gd.eppo.int/taxon/GLXMA",
    "cassava": "https://gd.eppo.int/taxon/MANES",
    "banana": "https://gd.eppo.int/taxon/MUBPA"
}

pest_dict = {
    "african bollworm": "https://gd.eppo.int/taxon/HELIAR",
    "cassava green mite": "https://gd.eppo.int/taxon/MONOSE",
    "soybean rust": "https://gd.eppo.int/taxon/PHAKIS",
    "fall armyworm": "https://gd.eppo.int/taxon/LAPHFR",
    "cutworm": "https://gd.eppo.int/taxon/SPODLI",
    "maize stalk borer": "https://gd.eppo.int/taxon/BUSSFU",
    "tuta absoluta": "https://gd.eppo.int/taxon/GNORAB"
}

update_frequency_dict = {
    "infrequently/unscheduled": "http://voc.madiphs.org#c_d02399d1",
    "daily": "http://voc.madiphs.org#c_98c125a4",
    "weekly": "http://voc.madiphs.org#c_8548533c",
    "monthly": "http://voc.madiphs.org#c_e26da0ba",
    "quarterly": "http://voc.madiphs.org#c_e4d1137a",
    "semi-annually": "http://voc.madiphs.org#c_d8dfabf4",
    "annually": "http://voc.madiphs.org#c_1c97a174"
}

owner_dict = {
    "cab international": "cabi"
}

language_dict = {
    "english": "eng",
    "chichewa": "nya",
    "swahili": "swa",
    "french": "fra",
    "german": "deu"
}

dataset_physical_format_dict = {
    "electronic": "http://voc.madiphs.org#c_31e9a711",
    "paper": "http://voc.madiphs.org#c_6807c50e"
}

license_dict = {
    "notspecified",
    "odc-pddl",
    "odc-odbl",
    "odc-by",
    "cc-zero",
    "cc-by",
    "cc-by-sa",
    "gfdl",
    "other-open",
    "other-pd",
    "other-at",
    "uk-ogl",
    "cc-nc",
    "other-nc",
    "other-closed"
}

def slugify_title(title):
    return "".join(item for item in title.strip().lower().replace(" ","-") if item.isalnum() or item == "-")


def get_tag_string(tag_input):
    # split 
    tmp_tags = tag_input.split(",")
    trimmed_tags = []
    for tag in tmp_tags:
        trimmed_tags.append(tag.strip())
    return ",".join(trimmed_tags)
    #return tag_input.replace(" ", "+")

def get_description(description, purpose, other):
    if len(purpose.strip()) > 0:
        description = description + f"\n\nPURPOSE: {purpose}"
    if len(other.strip()) > 0:
        description = description + f"\n\nOTHER INFORMATION: {other}"
    return description

def get_fuzzy_date_safe(date_str):
    try:
        return parse(date_str)
    except ParserError as ex:
        return None

def import_row(row, row_idx, dry_run=False):
    
    # Get the dataset dictionary
    
    # TODO: validate mandatory input
    validated = True
    validation_messages = []
    # Title/name
    dataset_name = slugify_title(row[2])
    if len(dataset_name.strip()) == 0:
        validated = False
        validation_messages.append(f"This is not a valid title: \"{dataset_name}\"")
    # Crop and pest
    crop = crop_dict.get(row[0].strip().lower(), None)
    if crop is None:
        validated = False
        validation_messages.append(f"We could not find this crop in our lists: \"{row[0]}\"")
    pest = pest_dict.get(row[1].strip().lower(), None)
    if pest is None:
        validated = False
        validation_messages.append(f"We could not find this pest in our lists: \"{row[1]}\"")
    # Owner organization
    owner_org = owner_dict.get(row[11].strip().lower(), None)
    if owner_org is None:
        validated = False
        validation_messages.append(f"We could not find this organization in our lists: \"{row[11].strip()}\"")
    # License
    license_id = row[25].strip().lower()
    if license_id not in license_dict:
        validated = False
        validation_messages.append("License with id = \"%s\" not found" % license_id)

    # URL
    url = row[24].strip()
    if url != "":
        # Check that it's a proper URL 
        try:
            validators.url(url)
        except validators.ValidationError as ex:
            validated = False
            validation_messages.append(f"{url} is not a valid URL")

    if not validated:
        validation_message_str = "\n* ".join(validation_messages)
        print(f"\n## There were validation errors with row {row_idx}:\n* {validation_message_str}" )
        return False
    
    if dry_run:
        return True
    
    dataset_dict = { 
        "type": scheming_type,
        "name": dataset_name, # Mandatory
        "crop": crop,
        "pest": pest,
        "title": row[2].strip(),
        "notes": get_description(row[3], row[13], row[27]),
        "tag_string": get_tag_string(row[4]),
        "maintainer_name": row[9],
        "maintainer_email": row[10],
        "owner_org": owner_org, # Mandatory
        "language": language_dict[row[14].strip().lower()],
        "creation_date": get_fuzzy_date_safe(row[15]),
        "update_frequency": update_frequency_dict.get(row[16].strip().lower(),None),
        "most_recent_update": get_fuzzy_date_safe(row[17]),
        "dataset_type": row[18],
        "dataset_physical_format": dataset_physical_format_dict[row[19].strip().lower()],
        "dataset_location": row[23],
        "license_id": license_id
    } 

    resource_dict = {
        "package_id": dataset_name,
        "url": row[24].strip(),
        "name": row[2],
        "format": row[20]
    }

    print(dataset_dict)
    r = requests.post(
        "https://ckan.madiphs.org/api/3/action/package_create",
        data=dataset_dict,
        headers={'Authorization':api_key}
    )
    if r.status_code == 200:
        r2 = requests.post(
            "https://ckan.madiphs.org/api/3/action/resource_create",
            data=resource_dict,
            headers={'Authorization':api_key}
        )
        print(r2.text)
    #print(r.text)


with open("factsheets.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=";", quotechar="\"")
    all_rows_validated = True
    for row_idx, row in enumerate(reader):
        if row[0] == "Crop":
            continue
        if not import_row(row, row_idx, True):
            all_rows_validated = False
    if all_rows_validated:
        print("Next: import the data")
    else:
        print("There were validation errors with at least one dataset")

