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