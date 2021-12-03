import requests
import gzip
import json
from tqdm import tqdm
from pathlib import Path

DEFAULT_DATA_FILENAME = 'data.json.gzip'

def download_data(filename=DEFAULT_DATA_FILENAME):
    if Path(filename).exists():
        return

    url = 'http://bulk.openweathermap.org/sample/weather_14.json.gz'
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))

    with open(filename, 'wb') as file, tqdm(
            desc='Downloading data',
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

def get_data(filename=DEFAULT_DATA_FILENAME):
    if Path(filename).exists() is False:
        download_data()

    result = []

    with gzip.open(filename, 'rt') as f:
        for city in f.readlines():
            result.append(json.loads(city))

    return result
