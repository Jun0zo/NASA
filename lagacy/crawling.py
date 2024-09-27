# 링크가 주어지면 해당 링크의 페이지를 크롤링하여 페이지의 파일들을 전부 다운로드하는 프로그램

import requests
from bs4 import BeautifulSoup
import os
from src.utils import sols_to_earth_date
import argparse

seis_base_url = 'https://pds-geosciences.wustl.edu'

# 다운로드 함수


def download_seis(url, directory):
    # URL에서 파일명 추출
    file_name = url.split('/')[-1]
    file_path = os.path.join(directory, file_name)

    # 이미지 다운로드
    with open(file_path, 'wb') as f:
        f.write(requests.get(url).content)

    print(f'{file_name} 다운로드 완료')


def crawl_seis(url, directory):
    # 페이지 요청
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 페이지의 모든 링크 찾기
    for link in soup.find_all('a'):
        href = link.get('href')
        href = seis_base_url + href
        if href.endswith('.mseed'):
            download_seis(href, directory)


def download_twins(url, directory):
    # URL에서 파일명 추출
    file_name = url.split('/')[-1]
    file_path = os.path.join(directory, file_name)

    # csv
    with open(file_path, 'wb') as f:
        f.write(requests.get(url).content)

    print(f'{file_name} 다운로드 완료')


def main(start_sols=237, sols_range=3):
    # 크롤링 실행
    for station in ['elyh0', 'elyhk', 'elys0', 'elyse']:
        for sols in range(start_sols, start_sols + sols_range):
            date = sols_to_earth_date(sols)
            year = date.year
            doy = date.timetuple().tm_yday

            # make directory
            if not os.path.exists('downloads/seis'):
                os.makedirs('downloads/seis')
            if not os.path.exists('downloads/twins'):
                os.makedirs('downloads/twins')

            crawl_seis(
                f'{seis_base_url}/insight/urn-nasa-pds-insight_seis/data/xb/continuous_waveform/{station}/{year}/{doy}/', 'downloads/seis')

            download_twins(
                f'https://atmos.nmsu.edu/PDS/data/PDS4/InSight/twins_bundle/data_derived/sol_0211_0300/twins_model_0{sols}_02.csv', 'downloads/twins')

    '''
    elyse: 최종 장비 배치 후의 과학 데이터.
    elyhk: 최종 장비 배치 후의 상태 감시 데이터(상태 모니터링).
    elys0: 착륙 후, 장비 배치 전의 과학 데이터.
    elyh0: 착륙 후, 장비 배치 전의 상태 감시 데이터.


    umb ***
    vmb
    '''


if __name__ == "__main__":
    # get params (start_sol, sol_range) (argparse)
    param = argparse.ArgumentParser()
    param.add_argument("--start_sol", type=int, default=237)
    param.add_argument("--sol_range", type=int, default=3)
    args = param.parse_args()

    main(start_sols=args.start_sol, sols_range=args.sol_range)
