<img src="images/MaDiPHS_logo.png" style="height: 200px; padding-bottom: 50px;"/>


# CKAN Metadata
This repository contains metadata for configuring the [CKAN](https://ckan.org/) installation 
for [MaDiPHS](https://madiphs.org) located at [https://ckan.madiphs.org/](https://ckan.madiphs.org/)

## ckanext-scheming
To create records for MaDiPHS datasets and factsheets, we have used the [ckanext-scheming](https://github.com/ckan/ckanext-scheming) 
extension and added the `factsheets-schema.yaml` and `datasets-schema.yaml` definitions. Please note that these schemas use the 
`display_snippets` property, e.g. like this:

```yaml
- field_name: country_codes
  label: Countries covered
  preset: multiple_select
  display_snippet: madiphstheming_country_codes.html
  choices:
 ```

 In this case, the `madiphstheming_country_codes.html` refers to [this file](https://github.com/MaDiPHS/ckanext-madiphstheming/blob/main/ckanext/madiphstheming/templates/scheming/display_snippets/madiphstheming_country_codes.html) in the [ckanext-madiphsteming repository](https://github.com/MaDiPHS/ckanext-madiphstheming).



## vocabularies
With guidance from Knowmatics we have created vocabularies for a number of categories in the schemas. These can be found in SKOS/RDF format under the `vocabularies` directory. It has been created using [Vocbench3](https://bitbucket.org/art-uniroma2/vocbench3/src/master/)

## Utilities
In the `util/` directory, you find scripts that are or have been part of the process of creating metadata or importing data

## Getting data from CKAN using the API
CKAN has a built-in API that enables a client to pull data directly from the system. The API's general documentation is found here: (https://docs.ckan.org/en/2.10/).

The following paragraphs contain documentation of MaDiPHS specific queries.

### Getting advisory resources
In this context, by "advisory resources" we mean pre-produced plant protection advice matching a specific problem, e.g. Fall Armyworm in Maize. The resources are produced by Malawi's [Department of Agriculture Extension Services (DAES)](https://ckan.madiphs.org/organization/about/daes).

**Per 2025-08-26, only text resources for banana are available.**

For each problem, advice may fall into these categories ("Information subject category"):
* Pest identification
* Pest symptoms/visual injury
* Pest management and control
* Pest spraying
...or optionally
* All subjects

For each category, the advice may be given as:
* Document
* Audio
* Video

#### API request examples
##### Banana advisory documents
Per 2025-08-26 a few PDFs for pests and diseases for banana have been uploaded. They contain "All subjects". Here's how to get them:

https://ckan.madiphs.org/api/3/action/package_search?q=type:advisory-resources-dataset+information_subject_category:"http://voc.madiphs.org%23c_8f96be84"+crop:"https://gd.eppo.int/taxon/MUBPA"&fq=organization:daes

##### FAW prototype resources

Here's an example request that pulls all the advice for spraying (treatment) Fall Armyworm in Maize (this is only prototype data on the CKAN-TEST server):

https://ckan-test.madiphs.org/api/3/action/package_search?q=type:advisory-resources-dataset+information_subject_category:"http://voc.madiphs.org%23c_39965b7c"+crop:"https://gd.eppo.int/taxon/ZEAMX"+pest:"https://gd.eppo.int/taxon/LAPHFR"&fq=organization:daes

Filtering on media type (text, audio, video) must be done after data retreival.

The list of ids for information subject categories, crops and pests can be found in `./ckanext-scheming/advisory-resources-schema.yaml` and in `./vocabularies/madiphs_skos.rdf`