import os
import requests
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
from utils import sols_to_earth_date

sol_ranges = [
            (0, 122),
            (123, 210),
            (211, 300),
            (301, 389),
            (390, 477),
            (478, 566),
            (567, 668),
            (669, 745),
            (746, 832),
            (833, 921),
            (922, 1010),
            (1011, 1100),
            (1101, 1188),
            (1189, 1276),
            (1277, 1366)
        ]

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
                logging.info(f"[*] Crawling URL: {url}")
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


# twins_downloader.py

# twins_downloader.py


class TWINSDownloader:
    def __init__(self, base_url='https://atmos.nmsu.edu/PDS/data/PDS4/InSight/twins_bundle/data_derived/'):
        self.base_url = base_url
        self.session = requests.Session()

    def get_directory_for_sol(self, sol):
        for start, end in sol_ranges:
            if start <= sol <= end:
                return f'sol_{start:04d}_{end:04d}/'
        return None

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

            dir_name = self.get_directory_for_sol(sol)
            if dir_name is None:
                logging.error(f'sol 번호 {sol}에 해당하는 디렉토리를 찾을 수 없습니다.')
                continue

            # 디렉토리의 파일 목록 가져오기
            dir_url = f"{self.base_url}{dir_name}"
            try:
                response = self.session.get(dir_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # 해당 sol 번호의 파일들 중 버전 번호를 추출하여 최신 버전 찾기
                version_numbers = []
                file_urls = {}
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href.endswith('.csv') and f'twins_model_{sol_str}_' in href:
                        version_str = href.split(
                            '_')[-1].split('.')[0]  # 예: '02'
                        if version_str.isdigit():
                            version = int(version_str)
                            version_numbers.append(version)
                            file_urls[version] = dir_url + href

                if not version_numbers:
                    logging.error(f'sol 번호 {sol}에 대한 파일을 찾을 수 없습니다.')
                    continue

                latest_version = max(version_numbers)
                latest_file_url = file_urls[latest_version]

                # 파일 다운로드
                self.download_file(latest_file_url, directory)

            except requests.HTTPError as e:
                logging.error(f'디렉토리 접근 실패: {dir_url}, 에러: {e}')


class PSDownloader:
    def __init__(self, base_url='https://atmos.nmsu.edu/PDS/data/PDS4/InSight/ps_bundle/data_calibrated/'):
        self.base_url = base_url
        self.session = requests.Session()
        
    def get_directory_for_sol(self, sol):
        for start, end in sol_ranges:
            if start <= sol <= end:
                return f'sol_{start:04d}_{end:04d}/'
        return None
            
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
            logging.error(f'[!] 파일 다운로드 실패: {url}, 에러: {e}')
            
    def download_range(self, start_sol, end_sol, directory):
        for sol in range(start_sol, end_sol + 1):
            sol_str = f"{sol:04d}"

            dir_name = self.get_directory_for_sol(sol)
            if dir_name is None:
                logging.error(f'[!] sol 번호 {sol}에 해당하는 디렉토리를 찾을 수 없습니다.')
                continue

            # 디렉토리의 파일 목록 가져오기
            dir_url = f"{self.base_url}{dir_name}"
            try:
                response = self.session.get(dir_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # 해당 sol 번호의 파일들 중 버전 번호를 추출하여 최신 버전 찾기
                version_numbers = []
                file_urls = {}
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href.endswith('.csv') and f'ps_calib_{sol_str}_' in href:
                        version_str = href.split(
                            '_')[-1].split('.')[0]  # 예: '02'
                        if version_str.isdigit():
                            version = int(version_str)
                            version_numbers.append(version)
                            file_urls[version] = dir_url + href

                if not version_numbers:
                    logging.error(f'sol 번호 {sol}에 대한 파일을 찾을 수 없습니다.')
                    continue

                latest_version = max(version_numbers)
                latest_file_url = file_urls[latest_version]

                # 파일 다운로드
                self.download_file(latest_file_url, directory)

            except requests.HTTPError as e:
                logging.error(f'디렉토리 접근 실패: {dir_url}, 에러: {e}')