#!/usr/bin/python3

"""
    Util script to import datasets from the Excel
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


import json
import pprint
import re
import csv
from dateutil.parser import parse, ParserError
import requests
import validators
from dotenv import load_dotenv
import africa_metadata, metadata, skos_utils

# This example was found here: https://docs.ckan.org/en/2.9/api/#example-importing-datasets-with-the-ckan-api

# This is needed to load any ENV settings from a .env (dotenv) file
# on your path
load_dotenv()
# This API key can be obtained by logging into ckan.madiphs.org 
api_key=os.getenv("CKAN_API_KEY")

# ckanext-scheming dataset type
scheming_type = "plant-health-knowledge-product"

OVERWRITE = True

CKAN_API_PATH = "https://ckan.madiphs.org/api/3/action/"

tag_pattern = r"[^a-zA-Z0-9\s\-_.]"


def slugify_title(title):
    return "".join(item for item in title.strip().lower().replace(" ","-") if item.isalnum() or item == "-")


def get_tag_string(tag_input):
    # split 
    tmp_tags = tag_input.replace(";",",").split(",")
    trimmed_tags = []
    for tag in tmp_tags:
        trimmed_tags.append(re.sub(tag_pattern, "", tag.strip().replace("\n","")))
    return ",".join(trimmed_tags)
    #return tag_input.replace(" ", "+")

def get_description(description, purpose, type, other):
    if len(purpose.strip()) > 0:
        description = description + f"\n\nPURPOSE: {purpose}"
    if len(type.strip()) > 0:
        description = description + f"\n\nTYPE: {type}"
    if len(other.strip()) > 0:
        description = description + f"\n\nOTHER INFORMATION: {other}"
    return description

def get_fuzzy_date_safe(date_str):
    try:
        return parse(date_str)
    except ParserError as ex:
        return None


allowed_crops = skos_utils.get_concepts_in_scheme_with_lowercase_label_as_key(skos_utils.CROPS_SCHEME,"EN")
allowed_pests = skos_utils.get_concepts_in_scheme_with_concept_as_key(skos_utils.PESTS_SCHEME,"EN")
#print(crops)
#exit()

def get_countries_covered(spatial_2):
    country_codes = []
    if spatial_2 == "":
        country_codes = africa_metadata.get_africa_country_codes()
    else:    
        country_names = [name.strip() for name in spatial_2.split(",")]
        #print(country_names)
        country_codes = africa_metadata.get_country_iso_codes(country_names)
        #print(country_codes)
        if len(country_codes) != len(country_names):
            # Check for SSA (Sub-Saharan Africa, a super region)
            if spatial_2.strip() == "SSA":
                country_codes = africa_metadata.get_super_region_country_codes(spatial_2.strip())
                #print(country_codes)
            
    return country_codes

# Book keeping - checking for duplicats
ids_in_import_dataset = []

def validate_row(row, row_idx):
    global ids_in_import_dataset
    # Get the dataset dictionary
    
    # TODO: validate mandatory input
    validated = True
    validation_messages = []
    # Title/name
    dataset_name = slugify_title(row["title"])
    

    if len(dataset_name.strip()) == 0:
        validated = False
        validation_messages.append(f"This is not a valid title: \"{dataset_name}\"")

    if dataset_name in ids_in_import_dataset:
        validated = False
        validation_messages.append(f"This title is a duplicate: {row["title"]}")
    else:
        ids_in_import_dataset.append(dataset_name)

    # Crop and pest
    crop = allowed_crops.get(row["crop"].strip().lower(), None)
    if crop is None:
        validated = False
        validation_messages.append(f"We could not find this crop in our lists: \"{row["crop"]}\"")
    if len(row["EPPO_pest"].strip()) > 0:
        pests = [pest.strip() for pest in row["EPPO_pest"].split(",")]
        for pest in pests:
            pest = allowed_pests.get(pest.strip(), None)
            if pest is None:
                validated = False
                validation_messages.append(f"We could not find this pest in our lists: \"{row["pest"]}\"")
    else:
        pest = ""
    # Owner organization
    owner_org = metadata.owner_dict.get(row["owner_name"].strip().lower(), None)
    if owner_org is None:
        validated = False
        validation_messages.append(f"We could not find this organization in our lists: \"{row["owner_name"].strip()}\"")

    # License
    license_id = row["license"].strip().lower()
    if license_id not in metadata.license_dict:
        validated = False
        validation_messages.append("License with id = \"%s\" not found" % license_id)

    # URL
    url = row["article_link"].strip()
    if url != "":
        # Check that it's a proper URL 
        try:
            validators.url(url)
        except validators.ValidationError as ex:
            validated = False
            validation_messages.append(f"{url} is not a valid URL")
    
    # Countries covered
    spatial_2 = row["spatial_2"].strip()
    countries_covered = get_countries_covered(spatial_2)
    if len(countries_covered) == 0:
        validated = False
        validation_messages.append(f"{spatial_2} contains countries not found in our list of African countries")
    
    # Georeference
    record_georeferenced = metadata.georeference_dict.get(row["record_georeferenced"].strip(), None)
    if record_georeferenced is None:
        record_georeferenced = False
        validation_messages.append(f"This record_georeferenced code is not valid: \"{row["record_georeferenced"].strip()}\"")

    # Update frequency
    update_frequency = metadata.update_frequency_dict.get(row["update_frequency"].strip().lower(), None)
    if update_frequency is None:
        validated = False
        validation_messages.append(f"This update frequency is not valid: \"{row["update_frequency"].strip()}\"")
    
    # Timestamp recording
    record_timestamp = metadata.record_timestamp_dict.get(row["record_timestamp"].strip().lower(), None)
    if record_timestamp is None:
        validated = False
        validation_messages.append(f"This record timestamp code is not valid: \"{row["record_timestamp"].strip()}\"")

    # Privacy
    privacy = metadata.privacy_dict.get(row["privacy"].strip().lower(), None)
    if privacy is None:
        validated = False
        validation_messages.append(f"This privacy code is not valid: \"{row["privacy"].strip()}\"")

    if not validated:
        validation_message_str = "\n* ".join(validation_messages)
        print(f"\n## There were validation errors with row {row_idx}:\n* {validation_message_str}" )
        return False
    
    return True

existing_datasets = []

def get_existing_datasets():
    global existing_datasets
    r = requests.get(
        f"{CKAN_API_PATH}/package_list",
        headers={'Authorization':api_key}
    )
    response = r.json()
    if response["success"]:
        existing_datasets = response["result"]
    #print(existing_datasets)

def import_row(row, row_idx, dry_run=True):
    #print(row["title"])
    dataset_name = slugify_title(row["title"])
    crop = allowed_crops.get(row["crop"].strip().lower(), None)
    if len(row["EPPO_pest"].strip()) > 0:
        pests = pests = [pest.strip() for pest in row["EPPO_pest"].split(",")]
    else:
        pests = "000"

    owner_org = metadata.owner_dict.get(row["owner_name"].strip().lower(), None)
    license_id = row["license"].strip().lower()
    url = row["resource_link"].strip()

    dataset_dict = { 
        "type": scheming_type,
        "name": dataset_name, # Mandatory
        "crop": crop,
        "pest": pests,
        "title": row["title"].strip(),
        "notes": get_description(row["description"], row["purpose"], row["type"], row["other_information"]),
        "tag_string": get_tag_string(row["key_words"]),
        "author": row["creator_name"],
        "author_email": row["creator_email"],
        "maintainer": row["manager_name"],
        "maintainer_email": row["manager_email"],
        "owner_org": owner_org, # Mandatory
        "language": metadata.language_dict.get(row.get("language","").strip().lower(),"000"),
        "creation_date": get_fuzzy_date_safe(row["creation_date"]),
        "update_frequency": metadata.update_frequency_dict.get(row["update_frequency"].strip().lower(),metadata.update_frequency_dict["infrequently/unscheduled"]),
        "most_recent_update": get_fuzzy_date_safe(row["most_recent_update"]),
        "dataset_physical_format": metadata.dataset_physical_format_dict.get(row.get("format_1","").strip().lower(),""),
        "dataset_size": row["size"].strip(),
        "dataset_location": row["location"].strip(),
        "spatial_resolution": row["spatial_resolution"].strip(),
        "temporal_resolution": row["temporal_resolution"].strip(),
        "record_georeferenced": metadata.georeference_dict.get(row["record_georeferenced"].strip(), None),
        "record_timestamp": metadata.record_timestamp_dict.get(row["record"].strip().lower(), None),
        "privacy": metadata.privacy_dict.get(row["privacy"].strip().lower, None),
        "country_codes": get_countries_covered(row["spatial_2"]),
        "license_id": license_id
    } 

    resource_dict = {
        "package_id": dataset_name,
        "url": url,
        "name": row["title"],
        "format": row["format_1"]
    }

    if dry_run:
        print(dataset_dict)
        print("DRY RUN")
        return
    
    
    if dataset_name in existing_datasets:
        if OVERWRITE:
            # Delete the existing dataset before recreating it
            r = requests.post(f"{CKAN_API_PATH}/dataset_purge",
                data={"id":dataset_name},
                headers={'Authorization':api_key}
            )
            print("Overwriting %s " % dataset_dict["title"])
        else:
            print(f"WARNING: Dataset with title \"{dataset_dict["title"]}\" already exists!")
    r = requests.post(
        f"{CKAN_API_PATH}/package_create",
        data=dataset_dict,
        headers={'Authorization':api_key}
    )
    if r.status_code == 200:
        r2 = requests.post(
            f"{CKAN_API_PATH}/resource_create",
            data=resource_dict,
            headers={'Authorization':api_key}
        )
    else:
        print("ERROR when trying to import row with title \"%s\": %s" % (dataset_dict["title"],r.text))
        #exit(0)
    #print(r.text)


with open("datasets.csv") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";", quotechar="\"")
    all_rows_validated = True
    all_rows=[]
    for row_idx, row in enumerate(reader):
        all_rows.append(row)
        if not validate_row(row, row_idx):
            all_rows_validated = False
    if all_rows_validated:
        get_existing_datasets()
        for row_idx, row in enumerate(all_rows):
            import_row(row, row_idx, False)         
    else:
        print("There were validation errors with at least one dataset")

