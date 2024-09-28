import argparse
from datetime import datetime, timedelta
from core.data_model import SEISData, TWINSData, PSData
from utils import sols_to_earth_date


def main():
    # 기본값 설정
    DEFAULT_START_SOL = 237
    DEFAULT_SOL_RANGE = 3
    DEFAULT_MIN_FREQ = 0.1
    DEFAULT_MAX_FREQ = 10
    DEFAULT_CHANNEL = 'BHU'
    DEFAULT_DATA_PATHS = {
        'seis': '../data/downloads/seis',
        'twins': '../data/downloads/twins',
        'ps': '../data/downloads/ps',
        'results': '../data/results'
    }

    # 명령줄 인수 파싱
    parser = argparse.ArgumentParser(description='SEIS 및 TWINS 데이터 처리 프로그램')

    # argument group 생성
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--start_sol', type=int, help='시작 sol 번호')
    group.add_argument('--start_date', type=str, help='시작 날짜 (YYYY-MM-DD)')
    group.add_argument('--start_doy', type=int, help='시작 DOY (1-366)')

    parser.add_argument('--year', type=int,
                        help='DOY를 사용하는 경우 연도 지정 (예: 2020)')
    parser.add_argument('--range', type=int, default=DEFAULT_SOL_RANGE,
                        help=f'데이터를 처리할 sol 수 또는 일수 (기본값: {DEFAULT_SOL_RANGE})')
    parser.add_argument('--channel', type=str, default=DEFAULT_CHANNEL,
                        help=f'SEIS 채널 (예: {DEFAULT_CHANNEL})')
    parser.add_argument('--minfreq', type=float, default=DEFAULT_MIN_FREQ,
                        help=f'최소 주파수 (기본값: {DEFAULT_MIN_FREQ} Hz)')
    parser.add_argument('--maxfreq', type=float, default=DEFAULT_MAX_FREQ,
                        help=f'최대 주파수 (기본값: {DEFAULT_MAX_FREQ} Hz)')

    args = parser.parse_args()

    # 시작점 처리
    landing_date = datetime(2018, 11, 26)  # InSight 착륙일

    if args.start_sol is not None:
        start_sol = args.start_sol
        start_date = sols_to_earth_date(start_sol)
        print('start date : ', start_date)
    elif args.start_date is not None:
        try:
            start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        except ValueError:
            print('[!] 시작 날짜의 형식이 올바르지 않습니다. (예: 2020-01-31)')
            return
        start_sol = (start_date - landing_date).days
    elif args.start_doy is not None:
        if args.year is not None:
            year = args.year
        else:
            year = datetime.now().year
        try:
            start_date = datetime.strptime(f'{year}-{args.start_doy}', '%Y-%j')
        except ValueError:
            print('[!] DOY의 범위는 1에서 366 사이여야 합니다.')
            return
        start_sol = (start_date - landing_date).days

    # range 처리
    sol_range = args.range

    # channel 처리
    channel = args.channel

    # 주파수 처리
    minfreq = args.minfreq
    maxfreq = args.maxfreq

    # 데이터 경로 설정
    data_paths = DEFAULT_DATA_PATHS

    # SEIS 데이터 처리
    seis_data = SEISData(start_sol, sol_range, channel, data_paths['seis'])
    seis_data.filter_data(minfreq, maxfreq)
    seis_data.plot_waveform(data_paths['results'] + '/seis_waveform.png')
    seis_data.plot_spectrogram(minfreq, maxfreq, data_paths['results'] + '/seis_spectrogram.png')

    # TWINS 데이터 처리
    twins_data = TWINSData(start_sol, sol_range, data_paths['twins'])
    twins_data.plot_wind_speed(data_paths['results'] + '/twins_wind_speed.png')
    twins_data.plot_temperature(data_paths['results'] + '/twins_temperature.png')
    
    ps_data = PSData(start_sol, sol_range, data_paths['ps'])
    ps_data.plot_pressure(data_paths['results'] + '/ps_pressure.png')
    


if __name__ == '__main__':
    main()

    # 사용 예시:
    # python main.py --start_sol 237 --range 3 --channel BHU
    # python main.py --start_date 2020-01-31 --range 3 --channel BHU
    # python main.py --start_doy 31 --year 2020 --range 3 --channel BHU
