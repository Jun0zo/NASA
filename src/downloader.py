import os
import requests
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
from utils import sols_to_earth_date


class SEISDownloader:
    def __init__(self, base_url='https://pds-geosciences.wustl.edu'):
        self.base_url = base_url
        self.session = requests.Session()

    def download_file(self, url, directory):
        file_name = url.split('/')[-1]
        file_path = os.path.join(directory, file_name)

        try:
            response = self.session.get(url)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                f.write(response.content)
            logging.info(f'{file_name} 다운로드 완료')
        except requests.HTTPError as e:
            logging.error(f'파일 다운로드 실패: {url}, 에러: {e}')

    def crawl_and_download(self, start_date, end_date, directory):
        date = start_date
        while date <= end_date:
            year = date.year
            doy = date.timetuple().tm_yday

            for station in ['elyh0', 'elyhk', 'elys0', 'elyse']:
                url = f'{self.base_url}/insight/urn-nasa-pds-insight_seis/data/xb/continuous_waveform/{station}/{year}/{doy:03d}/'

                try:
                    response = self.session.get(url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')

                    for link in soup.find_all('a'):
                        href = link.get('href')
                        if href.endswith('.mseed'):
                            file_url = self.base_url + href
                            self.download_file(file_url, directory)
                except requests.HTTPError as e:
                    logging.error(f'페이지 크롤링 실패: {url}, 에러: {e}')
                date += timedelta(days=1)

# twins_downloader.py


class TWINSDownloader:
    def __init__(self, base_url='https://atmos.nmsu.edu/PDS/data/PDS4/InSight/twins_bundle/data_derived/'):
        self.base_url = base_url
        self.session = requests.Session()

    def download_file(self, url, directory):
        file_name = url.split('/')[-1]
        file_path = os.path.join(directory, file_name)

        try:
            response = self.session.get(url)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                f.write(response.content)
            logging.info(f'{file_name} 다운로드 완료')
        except requests.HTTPError as e:
            logging.error(f'파일 다운로드 실패: {url}, 에러: {e}')

    def download_range(self, start_sol, end_sol, directory):
        for sol in range(start_sol, end_sol + 1):
            sol_str = f"{sol:04d}"
            file_name = f'twins_model_{sol_str}_02.csv'
            url = self.base_url + \
                f'sol_0{(sol // 100) * 100 + 1:03d}_{(sol // 100 + 1) * 100:04d}/{file_name}'

            self.download_file(url, directory)
