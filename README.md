# cldr-country-names-database

The CLDR (Unicode **C**ommon **L**ocale **D**ata **R**epository) publishes data for the names of countries/regions/territories in many languages, I prefer this data over the ISO 3166-1 names (that are only in English and French) e.g the "short" ISO name for the United Kingdom is "UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND". The CLDR name is "United Kingdom" and the short name is "UK", much better.

This project processes both past and present territory names from the CLDR and puts it into a more usable format for use in other projects. The data is available in a JSON, CSV and SQLite. https://github.com/unicode-cldr/cldr-json does provide the data in JSON format but the release is currently months outdated (version 36 not 37) and this only goes back until version 27 (2015-03-19).

#### Data format
The data is located in the releases, you can also run [download_and_process_cldr_data.py](download_and_process_cldr_data) to download and process the latest CLDR data to [/data/](./data/) if the releases are outdated.

* JSON - a file for every language contained in [/data/json](./data/json). If the language has a name/names for the territory then the names available are an object with keys of "name", "short" or "variant".
* CSV - A large CSV file with rows for all territory codes and columns "cldr_name_{x}", "cldr_short_{x}", "cldr_variant_{x} where x is every language. If there is no name it will be a blank string.
* SQLite - A database with a table for every language containing the one column for the territory code and three columns for the types of names possible. If there is no name it will be NULL.

#### Country names

The data contained has three types of names, these are outlined [by Unicode here.](http://cldr.unicode.org/translation/displaynames/country-names);

*  "name" - The name of the country
*  "short" - A shorter country name, typically more informal. e.g "UK" instead of "United Kingdom"
*  "variant" - An alternate name that may be appropriate in certain contexts e.g "Czech Republic" instead of "Czechia"

Obviously not all languages have names for every territory.

One assumption you should not make is that if a variant/short name exists then it must have a normal name. e.g Yiddish only has a variant for Timor-Leste (TL) not but a normal name. The other territories that have only short/variants in multiple languages are Congo (DRC) (CD), Congo (Republic) (CG), Hong Kong (HK), and Macao (MO). These are edge cases in uncommon languages but should not be ignored.

#### Scripts

* [download_and_extract_cldr_data.py](download_and_extract_cldr_data.py) - A script to download zipped data from CLDR and extract it
* [cldr_xml_to_json.py](cldr_xml_to_json.py) - Convert the XML supplied from CLDR into JSON
* [json_to_csv_and_sqlite.py](json_to_csv_and_sqlite.py) - Convert this JSON to both a CSV file and a SQLite database
* [download_and_process_cldr_data.py](download_and_process_cldr_data) - Uses the three other scripts to download the data and process it, saving it in JSON, CSV and SQLite.

#### Previous versions

If you want to build a database for previously released versions of CLDR you need to specify the release number in [download_and_process_cldr_data.py](download_and_process_cldr_data). The strings for these are not consistent e.g v2.0 is "2.0.0" but v21.0 is just "21". Use the folder name from https://unicode.org/Public/cldr/ (Note v1.4 is listed twice as "1.4" and "1.4.0").
