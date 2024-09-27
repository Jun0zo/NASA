import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 경로
csv_file = 'downloads/twins/twins_model_0237_02.csv'

# 데이터 읽기
df = pd.read_csv(
    csv_file,
    delimiter=','
)

# 데이터 확인
print(df.head())
print(df.columns)

# UTC 필드를 datetime 형식으로 변환
df['UTC'] = pd.to_datetime(df['UTC'], format='%Y-%jT%H:%M:%S.%fZ')

# 변환된 시간 확인
print(df['UTC'].head())

# 시각화할 필드 선택
fields_to_plot = [
    'HORIZONTAL_WIND_SPEED'
]

# ------------------ 1. 라인 그래프 (Line Plot) ------------------

# 플롯 크기 설정
plt.figure(figsize=(15, 8))

# 라인 그래프 그리기
for field in fields_to_plot:
    plt.plot(df['UTC'], df[field], label=field)

# 그래프 제목 및 레이블 설정
plt.title('InSight APSS TWINS - Wind Speed (Line Plot)')
plt.xlabel('UTC Time')
plt.ylabel('Wind Speed (meter/second)')
plt.legend()
plt.grid(True)
plt.tight_layout()

# 라인 그래프 저장
plt.savefig('results/twins_wind_speed_line.png')

# 그래프 표시
plt.show()

# ------------------ 2. 점 그래프 (Scatter Plot) ------------------

# 플롯 크기 설정
plt.figure(figsize=(15, 8))

# 점 그래프 그리기
for field in fields_to_plot:
    plt.scatter(df['UTC'], df[field], label=field, s=10)  # s=10은 점 크기

# 그래프 제목 및 레이블 설정
plt.title('InSight APSS TWINS - Wind Speed (Scatter Plot)')
plt.xlabel('UTC Time')
plt.ylabel('Wind Speed (meter/second)')
plt.legend()
plt.grid(True)
plt.tight_layout()

# 점 그래프 저장
plt.savefig('results/twins_wind_speed_scatter.png')

# 그래프 표시
plt.show()
