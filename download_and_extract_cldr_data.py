import os
import urllib.request

from tqdm import tqdm
from zipfile import ZipFile
import shutil


class DownloadProgressBar(tqdm):
    """Progress bar wrapper for downloading"""

    def update_to(self, b=1, bsize=1, tsize=None):
        """Update progress bar"""
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    """https://stackoverflow.com/a/53877507"""
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as bar:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=bar.update_to)


def download_cldr_data(download_path='temp/cldr_data.zip', version='latest'):
    """Download the latest CLDR data from the website"""
    # The zip of very early versions is called cldr.zip not core.zip
    versions_where_zip_is_cldr = ['1.2.0', '1.1.1', '1.1.0']
    zip_name = 'core' if version not in versions_where_zip_is_cldr else 'cldr'
    download_link = f"https://unicode.org/Public/cldr/{version}/{zip_name}.zip"
    os.makedirs('temp', exist_ok=True)
    download_url(download_link, download_path)


def extract_cldr_data(download_path='temp/cldr_data.zip', version='latest'):
    """Extract CLDR data from downloaded zip, only part of the file needs unzipping"""
    # In early versions the main folder is in a different location
    versions_with_no_common = ['1.6.1', '1.6.0', '1.5.1', '1.5.0', '1.4.1', '1.4.0',
                               '1.2.0', '1.1.1', '1.1.0']
    main_path = 'common/' if version not in versions_with_no_common else ''

    with ZipFile(download_path, 'r') as zip_obj:
        list_of_file_names = zip_obj.namelist()
        file_names = list(filter(lambda x: f'{main_path}main/' in x, list_of_file_names))
        zip_obj.extractall(members=file_names, path='temp')
    # Just to make it a little nicer I will move the files
    shutil.rmtree('temp/cldr_data', ignore_errors=True)
    shutil.copytree(f'temp/{main_path}main/', 'temp/cldr_data')
    shutil.rmtree(f'temp/{main_path}main/')


def download_and_extract_cldr_data(download_path='temp/cldr_data.zip', version='latest'):
    """Download latest CLDR data and extract it"""
    download_cldr_data(download_path, version)
    extract_cldr_data(download_path, version)


if __name__ == "__main__":
    download_and_extract_cldr_data()
