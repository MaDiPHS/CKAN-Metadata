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

# Lookup dicts for validation and data conversion from text to category


update_frequency_dict = {
    "infrequently/unscheduled": "http://voc.madiphs.org#c_d02399d1",
    "hourly": "http://voc.madiphs.org#c_5c3c0589",
    "daily": "http://voc.madiphs.org#c_98c125a4",
    "weekly": "http://voc.madiphs.org#c_8548533c",
    "monthly": "http://voc.madiphs.org#c_e26da0ba",
    "quarterly": "http://voc.madiphs.org#c_e4d1137a",
    "semi-annually": "http://voc.madiphs.org#c_d8dfabf4",
    "annually": "http://voc.madiphs.org#c_1c97a174"
}

georeference_dict = {
    "0": "http://voc.madiphs.org#c_fd25ee02",
    "1": "http://voc.madiphs.org#c_56b63488",
    "2": "http://voc.madiphs.org#c_df3474ed",
    "3": "http://voc.madiphs.org#c_cb970135",
    "4": "http://voc.madiphs.org#c_b28b92e7",
    "5": "http://voc.madiphs.org#c_874d5d55",
    "6": "http://voc.madiphs.org#c_5a6946e1"
}

record_timestamp_dict = {
    "0": "http://voc.madiphs.org#c_21594acd",
    "1": "http://voc.madiphs.org#c_a0dde2d5",
    "2": "http://voc.madiphs.org#c_a25bd43f",
    "3": "http://voc.madiphs.org#c_3c497f9f",
    "4": "http://voc.madiphs.org#c_a3a8e068"
}

privacy_dict = {
    "0": "http://voc.madiphs.org#c_b16d2487",
    "1": "http://voc.madiphs.org#c_45fa9a35",
    "2": "http://voc.madiphs.org#c_777b79b4",
    "3": "http://voc.madiphs.org#c_69fc1494",
    "4": "http://voc.madiphs.org#c_4581d1c6"
}


owner_dict = {
    "cab international": "cabi",
    "cabi": "cabi",
    "dccms": "dccms",
    "iita": "iita",
    "plant village": "plantvillage",
    "icipe": "icipe",
    "usaid": "usaid",
    "fao": "fao",
    "sawbo": "sawbo",
    "daes": "daes",
    "icrisat": "icrisat",
    "cimmyt": "cimmyt"
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
