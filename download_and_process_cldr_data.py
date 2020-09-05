import sys
import shutil

from download_and_extract_cldr_data import download_and_extract_cldr_data
from cldr_xml_to_json import extract_territories_from_xml_and_save_to_json
from json_to_csv_and_sqlite import save_to_csv, save_to_sqlite_db


def download_all():
    """Download and process all availible versions"""
    versions = ['37', '36.1', '36', '35.1', '35', '34',
                '33.1', '33', '32.0.1', '32', '31.0.1', '31',
                '30.0.3', '30.0.2', '30.0.1', '30', '29',
                '28', '27.0.1', '27', '26.0.1', '26', '25',
                '24', '23.1', '23', '22.1', '22', '21',
                '2.0.1', '2.0.0', '1.9.1', '1.9.0', '1.8.1',
                '1.8.0', '1.7.2', '1.7.1', '1.7.0', '1.6.1',
                '1.6.0', '1.5.1', '1.5.0', '1.4.1', '1.4.0',
                '1.3.0', '1.2.0', '1.1.1', '1.1.0']

    for i, version in enumerate(versions):
        print(f"({i+1} of {len(versions)}) {version}")
        sys.stdout.flush()
        save_path = f"data/{version}"
        json_save_path = f'{save_path}/json'
        download_and_extract_cldr_data(download_path=f'temp/cldr_data_{version}.zip',
                                       version=version)
        extract_territories_from_xml_and_save_to_json(json_save_path)
        save_to_csv(save_path, json_save_path=json_save_path)
        save_to_sqlite_db(save_path, json_save_path=json_save_path)
        shutil.make_archive(f'{save_path}/json', 'zip', json_save_path)


def download_latest():
    """Download and process the latest version"""
    save_path = f"data"
    json_save_path = f'{save_path}/json'
    download_and_extract_cldr_data()
    extract_territories_from_xml_and_save_to_json(json_save_path)
    save_to_csv(save_path, json_save_path=json_save_path)
    save_to_sqlite_db(save_path, json_save_path=json_save_path)


if __name__ == "__main__":
    download_latest()
