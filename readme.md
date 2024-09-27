🚀 Mars Data Explorer

Mars Data Explorer는 NASA의 InSight 미션에서 제공하는 SEIS(Seismic Experiment for Interior Structure)와 TWINS(Temperature and Wind for InSight) 데이터를 손쉽게 다운로드하고 처리할 수 있는 Python 기반 도구입니다. 이 도구를 사용하여 화성의 지진 데이터와 기상 데이터를 수집하고, 분석 및 시각화할 수 있습니다.

🌟 주요 기능
데이터 다운로드 자동화: 명령줄 인수를 통해 원하는 기간의 데이터를 자동으로 다운로드합니다.
유연한 시작점 지정: 솔 번호, 지구 날짜, DOY(Day of Year) 중 원하는 방식으로 데이터의 시작점을 지정할 수 있습니다.
데이터 처리 및 시각화: 다운로드한 데이터를 필터링하고, 파형 및 스펙트로그램을 생성합니다.
주파수 범위 설정: 최소 및 최대 주파수를 설정하여 관심 주파수 대역의 데이터를 처리합니다.
🛠️ 설치 방법
1. 리포지토리 클론
bash
코드 복사
git clone https://github.com/yourusername/mars-data-explorer.git
cd mars-data-explorer
2. 가상환경 생성 및 활성화
bash
코드 복사
# 가상환경 생성 (Python 3.7 이상 필요)
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate
3. 필요한 패키지 설치
bash
코드 복사
pip install -r requirements.txt
🚴 사용 방법
명령줄 인수 설명
bash
코드 복사
python main.py [OPTIONS]
--start_sol: 시작 솔(Sol) 번호 (예: --start_sol 237)
--start_date: 시작 지구 날짜 (형식: YYYY-MM-DD, 예: --start_date 2020-01-31)
--start_doy: 시작 DOY(Day of Year) (예: --start_doy 31)
--year: --start_doy 사용 시 연도 지정 (예: --year 2020)
--range: 데이터를 처리할 솔 수 또는 일수 (기본값: 3)
--channel: SEIS 채널 (기본값: BHU, 예: --channel BHU)
--minfreq: 최소 주파수 (기본값: 0.1 Hz)
--maxfreq: 최대 주파수 (기본값: 10 Hz)
사용 예시
1. 솔 번호로 데이터 처리
bash
코드 복사
python main.py --start_sol 237 --range 3 --channel BHU
2. 지구 날짜로 데이터 처리
bash
코드 복사
python main.py --start_date 2020-01-31 --range 3 --channel BHU
3. DOY와 연도로 데이터 처리
bash
코드 복사
python main.py --start_doy 31 --year 2020 --range 3 --channel BHU
4. 주파수 범위 설정하여 데이터 처리
bash
코드 복사
python main.py --start_sol 237 --range 3 --minfreq 0.5 --maxfreq 5.0 --channel BHU
📁 디렉토리 구조
css
코드 복사
mars-data-explorer/
├── data/
│   ├── downloads/
│   │   ├── seis/
│   │   └── twins/
│   └── results/
├── src/
│   ├── main.py
│   ├── data_model.py
│   ├── utils.py
│   ├── seis_downloader.py
│   └── twins_downloader.py
├── requirements.txt
├── README.md
└── .gitignore
data/: 데이터 관련 디렉토리
downloads/: 다운로드된 원본 데이터 저장
seis/: SEIS 데이터
twins/: TWINS 데이터
results/: 처리된 데이터 및 시각화 결과 저장
src/: 소스 코드 디렉토리
main.py: 프로그램의 진입점
data_model.py: 데이터 처리 클래스 정의
utils.py: 유틸리티 함수 모음
seis_downloader.py: SEIS 데이터 다운로드 모듈
twins_downloader.py: TWINS 데이터 다운로드 모듈
requirements.txt: 필요한 Python 패키지 목록
README.md: 프로젝트 설명서
.gitignore: Git에 포함시키지 않을 파일 및 디렉토리 목록
🔍 주요 모듈 설명
1. main.py
프로그램의 시작점으로, 명령줄 인수를 파싱하고 데이터를 다운로드 및 처리하는 작업을 수행합니다.

2. data_model.py
SEISData 클래스: SEIS 데이터를 처리하는 기능을 제공합니다.
TWINSData 클래스: TWINS 데이터를 처리하는 기능을 제공합니다.
3. utils.py
날짜 변환 등 여러 곳에서 사용되는 유틸리티 함수를 제공합니다.
4. seis_downloader.py & twins_downloader.py
각각 SEIS와 TWINS 데이터를 다운로드하는 기능을 제공합니다.
🎨 결과 예시
파형 플롯


스펙트로그램


바람 속도 그래프


🤝 기여 방법
이 리포지토리를 포크합니다.
새로운 브랜치를 생성합니다. (git checkout -b feature/your-feature-name)
변경 사항을 커밋합니다. (git commit -m 'Add some feature')
브랜치에 푸시합니다. (git push origin feature/your-feature-name)
Pull Request를 생성합니다.
📝 라이선스
이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참고하세요.

📞 문의
프로젝트와 관련된 문의 사항이나 제안 사항이 있으시면 아래의 이메일로 연락주세요.

Email: your.email@example.com
Made with ❤️ by Your Name