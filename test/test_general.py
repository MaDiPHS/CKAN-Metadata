import africa_metadata, skos_utils
import json

def test_get_country_iso_codes():
    assert africa_metadata.get_country_iso_codes(["Malawi","Nigeria"]) == ["MWI","NGA"]

def test_get_super_region_country_codes():
    ssa_country_codes = africa_metadata.get_super_region_country_codes("SSA")
    assert len(ssa_country_codes) == 49

def test_get_africa_country_codes():
    africa_country_codes = africa_metadata.get_africa_country_codes()
    assert len(africa_country_codes) == 55
    """
    country_list = africa_metadata.get_country_list(africa_country_codes)
    country_list = sorted(country_list, key=lambda d: d["name"])
    for country in country_list:
        print("  - value: %s\n    label: %s" % (country["ISO_A3"],country["name"]))
    """

def test_get_multi_country_geojson():
    """
    Looking for crashes
    """
    ssa_country_codes = africa_metadata.get_super_region_country_codes("SSA")
    multi_country_geojson = africa_metadata.get_multi_country_geojson(ssa_country_codes)
    #with open("multi_countries.geojson","w") as outfile:
    #    json.dump(multi_country_geojson, outfile)

def test_get_concepts_in_scheme():
    assert "Fall Armyworm" in [concept["name"] for concept in skos_utils.get_concepts_in_scheme(skos_utils.PESTS_SCHEME,"EN")]

