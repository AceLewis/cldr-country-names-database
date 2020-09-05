import re
import os
import json
import glob
from collections import defaultdict

from lxml import etree


def save_dict_as_json(file_name, dictionary):
    """Save a dictionary as a json file"""
    with open(file_name, 'w', encoding="utf-8") as file:
        json.dump(dictionary, file, indent=4, sort_keys=True)


def load_json_as_dict(file_name):
    """Load a json as a dictionary"""
    with open(file_name, 'r', encoding="utf-8") as file:
        return json.load(file)


def get_languages(glob_string):
    """Get the language code from the XML/json filenames"""
    # split on (. / and \)  and take the second from last you get the file name.
    languages = [re.split(r'\\|/|\.', name)[-2] for name in glob.glob(glob_string)]
    # root is not a language so filter it out
    return list(filter(lambda x: x not in ['root', 'supplementalData'], languages))


def save_language_to_json(language, cldr_file_path, save_path, load_parent_language=False):
    """
    Get the country names for a language and convert it to json.

    Keyword argument:
    load_parent_language -- If this language is a dialect/sublanguage should
                            the parent language be loaded. If False the language
                            will be skipped (default False)
    """
    file_name = fr'{cldr_file_path}\{language}.xml'

    xml_doc = etree.parse(file_name)
    language_type = xml_doc.find('identity').find('language').get('type')

    # If the language is a dialect/sublanguage the language type will be of it's parent
    # e.g "en_GB" will have a type "en".
    all_name_dict = defaultdict(dict)

    if language_type != language:
        if load_parent_language:
            # Only load the parent language after it has been saved
            all_name_dict.update(load_json_as_dict(f"{save_path}/{language_type}.json"))
        else:
            return False
    # Try to get territories
    try:
        territories = xml_doc.find('localeDisplayNames').find('territories')
    except AttributeError:
        # If there is an AttributeError then it is the same as the parent
        save_dict_as_json(f"{save_path}/{language}.json", all_name_dict)
        return True

    if territories is None:
        # Also it there are no territories listed then it is the same as the parent
        save_dict_as_json(f"{save_path}/{language}.json", all_name_dict)
        return True

    territories_list = territories.findall('territory')
    territory_codes = list(set(x.get('type') for x in territories_list))
    # If you want to ignore 'continents' then uncomment the following line
    # territory_codes = list(filter(lambda x: len(x) == 2, territory_codes))

    for x in territory_codes:
        instances = territories.findall(f'territory[@type="{x}"]')
        # if ↑↑↑ then use the parent languages name
        name_dict = {x.get('alt', 'name'): x.text for x in instances if x.text != '↑↑↑'}
        all_name_dict[x].update(name_dict)
    # Save dictionary as a json
    save_dict_as_json(f"{save_path}/{language}.json", all_name_dict)
    return True


def extract_territories_from_xml_and_save_to_json(save_path):
    """Extract the information from all XMLs and save to json"""
    cldr_file_path = r'./temp/cldr_data'
    os.makedirs(save_path, exist_ok=True)

    languages = get_languages(f'{cldr_file_path}/*.xml')
    number_of_languages = len(languages)
    # Save the parent languages first then the dialects/sublanguages
    language_saving = 1
    language_with_parent = []
    for language in languages:
        if not save_language_to_json(language, cldr_file_path, save_path):
            language_with_parent.append(language)
        else:
            print(f"Saved {language} ({language_saving} of {number_of_languages})")
            language_saving += 1

    for language in language_with_parent:
        save_language_to_json(language, cldr_file_path, save_path, load_parent_language=True)
        print(f"Saved {language} ({language_saving} of {number_of_languages})")
        language_saving += 1


if __name__ == "__main__":
    save_path = f"./data/json"
    extract_territories_from_xml_and_save_to_json(save_path)
