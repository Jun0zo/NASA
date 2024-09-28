# main.py

import os
import argparse
import logging
from datetime import datetime, timedelta
from downloader import SEISDownloader, TWINSDownloader, PSDownloader
from utils import sols_to_earth_date


def main():
    # 로깅 설정
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # 인자 파서 설정
    parser = argparse.ArgumentParser(description='SEIS 및 TWINS 데이터 다운로드 스크립트')

    # 시작점을 지정하는 상호 배타적인 그룹 생성
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--start_sol', type=int, help='시작 sol 번호')
    group.add_argument('--start_date', type=str, help='시작 날짜 (YYYY-MM-DD)')
    group.add_argument('--start_doy', type=int, help='시작 DOY (1-366)')

    parser.add_argument('--year', type=int,
                        help='시작 DOY를 사용하는 경우 연도 지정 (예: 2019)')
    parser.add_argument('--range', type=int, default=1,
                        help='데이터를 다운로드할 일수 또는 sol 수')
    parser.add_argument('--output_dir', type=str,
                        default='../data/downloads', help='다운로드할 디렉토리')

    args = parser.parse_args()

    # 출력 디렉토리 설정
    seis_dir = os.path.join(args.output_dir, 'seis')
    twins_dir = os.path.join(args.output_dir, 'twins')
    os.makedirs(seis_dir, exist_ok=True)
    os.makedirs(twins_dir, exist_ok=True)

    # 날짜 범위 계산
    landing_date = datetime(2018, 11, 26)  # InSight 착륙일

    if args.start_sol is not None:
        start_sol = args.start_sol
        start_date = sols_to_earth_date(start_sol)
    elif args.start_date is not None:
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        start_sol = (start_date - landing_date).days
    elif args.start_doy is not None:
        # 연도를 지정하지 않으면 현재 연도로 가정
        if args.year is not None:
            year = args.year
        else:
            year = datetime.now().year
        try:
            start_date = datetime.strptime(f'{year}-{args.start_doy}', '%Y-%j')
        except ValueError:
            logging.error('DOY의 범위는 1에서 366 사이여야 합니다.')
            return
        start_sol = (start_date - landing_date).days
    else:
        logging.error('시작 sol 번호, 시작 날짜 또는 시작 DOY를 입력해야 합니다.')
        return

    # end_date 및 end_sol 계산
    end_sol = start_sol + args.range - 1
    end_date = start_date + timedelta(days=args.range - 1)

    logging.info(f'SEIS 데이터 다운로드: {start_date.date()}부터 {end_date.date()}까지')
    logging.info(f'TWINS 데이터 다운로드: sol {start_sol}부터 sol {end_sol}까지')

    # 다운로드 객체 생성
    seis_downloader = SEISDownloader()
    twins_downloader = TWINSDownloader()
    ps_downloader = PSDownloader()

    # SEIS 데이터 다운로드
    # seis_downloader.crawl_and_download(
    #     start_date=start_date,
    #     end_date=end_date,
    #     directory=seis_dir
    # )

    # # TWINS 데이터 다운로드
    # twins_downloader.download_range(
    #     start_sol=start_sol,
    #     end_sol=end_sol,
    #     directory=twins_dir
    # )
    
    # PS 데이터 다운로드
    ps_downloader.download_range(
        start_sol=start_sol,
        end_sol=end_sol,
        directory=twins_dir
    )

if __name__ == '__main__':
    main()

    # 사용 예시:
    # python crawling.py --start_sol 237 --range 3 --output_dir ../data/downloads
    # python crawling.py --start_date 2020-01-31 --range 3 --output_dir ../data/downloads
    # python crawling.py --start_doy 31 --year 2020 --range 3 --output_dir ../data/downloads
