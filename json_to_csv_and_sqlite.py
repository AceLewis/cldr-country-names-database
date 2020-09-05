import sqlite3
import os
import contextlib
import functools
import operator

import pandas as pd
import numpy as np

from cldr_xml_to_json import load_json_as_dict, get_languages


def delete_file_if_exist(file_name):
    """Try to delete a file if it exists"""
    try:
        os.remove(file_name)
    except OSError:
        pass


def replace_quotation(string):
    """Replace quotation marks with escaped ones"""
    return string.replace("'", "''") if string is not None else string


def save_to_sqlite_db(save_path, json_save_path='/data/json', file_name='cldr_names.db'):
    """Save the data to a sqlite database"""
    sqlite_path = f'{save_path}/{file_name}'
    delete_file_if_exist(sqlite_path)

    with contextlib.closing(sqlite3.connect(sqlite_path)) as conn:
        c = conn.cursor()
        for language in get_languages(f'{json_save_path}/*.json'):
            # Create a table for each language
            c.execute(f"""CREATE TABLE `{language}`
                      (territory_code, cldr_name, cldr_short, cldr_variant)""")
            # Load the json and save each territory
            language_dict = load_json_as_dict(f"{json_save_path}/{language}.json")
            for territory_code, dictionary in language_dict.items():
                cldr_name = replace_quotation(dictionary.get('name', None))
                short_cldr_name = replace_quotation(dictionary.get('short', None))
                cldr_variant = replace_quotation(dictionary.get('variant', None))
                c.execute(f"""INSERT INTO `{language}` VALUES (?, ?, ?, ?)""",
                          (territory_code, cldr_name, short_cldr_name, cldr_variant))
        # Commit changes
        conn.commit()


def save_to_csv(save_path, json_save_path='/data/json', file_name='cldr_names.csv'):
    """Save the data to CSV"""
    csv_path = f'{save_path}/{file_name}'
    delete_file_if_exist(csv_path)
    languages = get_languages(f'{json_save_path}/*.json')
    all_column_names = [[f"cldr_name_{x}", f"cldr_short_{x}", f"cldr_variant_{x}"]
                        for x in languages]
    all_column_names = functools.reduce(operator.iconcat, all_column_names, [])
    # The 'en' language has all territories
    all_territories = load_json_as_dict(f"{json_save_path}/en.json").keys()
    # Create empty datafrom with columns as the cldr names and rows as territory codes
    df = pd.DataFrame(columns=all_territories, dtype=str)
    df = df.transpose()
    df = df.reindex(columns=all_column_names)
    df = df.replace(np.nan, '', regex=True)

    for language in languages:
        language_dict = load_json_as_dict(f"{json_save_path}/{language}.json")
        for cc, dictionary in language_dict.items():
            cldr_name = dictionary.get('name', None)
            short_cldr_name = dictionary.get('short', None)
            cldr_variant = dictionary.get('variant', None)
            df.at[cc, f'cldr_name_{language}'] = cldr_name
            df.at[cc, f'cldr_short_{language}'] = short_cldr_name
            df.at[cc, f'cldr_variant_{language}'] = cldr_variant
    # Save dataframe as CSV
    df.index.name = 'territory_code'
    df.to_csv(csv_path, encoding='utf-8-sig')


if __name__ == "__main__":
    save_path = "data"
    save_to_csv(save_path)
    save_to_sqlite_db(save_path)
