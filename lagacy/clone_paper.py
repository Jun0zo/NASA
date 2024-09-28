from scipy import signal
from matplotlib import cm
import pandas as pd
import obspy
from scipy.signal import spectrogram
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os
from utils import sols_to_earth_date

start_sol = 238
sol_range = 3

# --------------------------------------
# 기존 함수 (SEIS 파일 및 TWINS 파일 읽기)
# --------------------------------------


def get_seis_file_name(date, channel):
    channel = channel.lower()
    # date to doy
    year = date.year
    doy = date.timetuple().tm_yday
    print(f"year-doy : {year}-{doy}")

    for filename in sorted(os.listdir('../data/downloads/seis')):
        if ".mseed" in filename and \
                str(doy) in filename and \
                str(year) in filename and \
                channel in filename:
            print(f'returning {filename}')
            return filename


def get_twins_file_name(sols):
    for filename in sorted(os.listdir('../data/downloads/twins')):
        if ".csv" in filename and \
                str(sols) in filename:
            return filename

# 파일이름 리스트를 받고 한번에 obspystream으로 읽어오기 함수


def read_obsfiles(file_names):
    combined_stream = obspy.read(file_names[0])
    if len(file_names) > 1:
        for file in file_names[1:]:
            combined_stream += obspy.read(file)
        combined_stream.merge(method=1)
    return combined_stream


# --------------------------
# SEIS 파일 읽고 시각화 처리
# --------------------------

seis_file_names = []
for sol_number in range(start_sol, start_sol + sol_range):
    seis_file_names.append("../data/downloads/seis/" + get_seis_file_name(
        date=sols_to_earth_date(sol_number), channel="BHU"))

print(seis_file_names)
combined_stream = read_obsfiles(seis_file_names)

print(combined_stream[0].stats)

# This is how you get the data and the time, which is in seconds
tr = combined_stream.traces[0].copy()
tr_times = tr.times()
tr_data = tr.data

# 파형 플롯
fig = plt.figure(figsize=(10, 5))
plt.plot(tr_times, tr_data)
plt.xlabel('Time (s)', fontweight='bold')
plt.ylabel('Amplitude', fontweight='bold')
plt.savefig(f"results/waveform_{sol_number}-{sol_number+sol_range}.png")

# ------------------------------------
# 필터링 및 스펙트로그램 생성
# ------------------------------------

minfreq = 0.1
maxfreq = 10

# 필터링 후 분리 및 처리
st_filt = combined_stream.copy()
print('sampling rate : ', st_filt.traces[0].stats.sampling_rate)
print(f"Filtering between {minfreq} and {maxfreq} Hz")
st_filt_split = st_filt.split()

for tr in st_filt_split:
    tr.filter('bandpass', freqmin=minfreq, freqmax=maxfreq)

tr_filt = st_filt.traces[0].copy()
tr_times_filt = tr_filt.times()
tr_data_filt = tr_filt.data

# 스펙트로그램 생성
f, t, sxx = signal.spectrogram(tr_data_filt, tr_filt.stats.sampling_rate)
sxx_min = np.min(sxx)
sxx_max = np.max(sxx)
print(f"min: {sxx_min:.10f}, max: {sxx_max}")

sxx = np.sqrt(sxx + 1e-1000)
sxx = np.log10(sxx + 1e-1000)

# 스펙트로그램 시각화
fig = plt.figure(figsize=(10, 5))  # 사이즈 조정
ax2 = plt.subplot(1, 1, 1)
vals = ax2.pcolormesh(t, f, sxx, cmap=cm.jet)
ax2.set_xlim([min(tr_times_filt), max(tr_times_filt)])
ax2.set_ylim([minfreq, maxfreq])
ax2.set_yscale('log')

ax2.set_yticks([0.1, 1, 10])
ax2.get_yaxis().set_major_formatter(plt.ScalarFormatter())
ax2.set_xlabel(f'Time (Day Hour:Minute)', fontweight='bold')
ax2.set_ylabel('Frequency (Hz)', fontweight='bold')
cbar = plt.colorbar(vals, orientation='horizontal')
cbar.set_label('Power ((m/s)/sqrt(Hz))', fontweight='bold')

plt.savefig(f"results/spectrogram_{sol_number}-{sol_number+sol_range}.png")

# ==============================================
# 바람 데이터(TWINS) 읽기 및 시각화 추가
# ==============================================


# TWINS 파일들을 읽고 데이터를 합치는 부분
all_twins_data = []

# 여러 솔 데이터를 하나로 합침
for sol_number in range(start_sol, start_sol + sol_range):
    twins_file_name = "downloads/twins/" + \
        get_twins_file_name(sol_number)
    print(f"Reading data from: {twins_file_name}")

    # 파일 읽기
    twins_data = pd.read_csv(twins_file_name)

    # UTC 필드를 datetime 형식으로 변환
    twins_data['UTC'] = pd.to_datetime(
        twins_data['UTC'], format='%Y-%jT%H:%M:%S.%fZ')

    # 데이터를 리스트에 추가
    all_twins_data.append(twins_data)

# 모든 데이터를 하나의 DataFrame으로 병합
combined_twins_data = pd.concat(all_twins_data, ignore_index=True)

# 시각화할 필드 선택
fields_to_plot = ['HORIZONTAL_WIND_SPEED']

# ------------------ 1. 라인 그래프 (Line Plot) ------------------

# 플롯 크기 설정
plt.figure(figsize=(15, 8))

# 라인 그래프 그리기
for field in fields_to_plot:
    plt.plot(combined_twins_data['UTC'],
             combined_twins_data[field], label=f'{field} (line)')

# 그래프 제목 및 레이블 설정
plt.title(f'InSight APSS TWINS - Wind Speed (Line Plot for {sol_range} sols)')
plt.xlabel('UTC Time')
plt.ylabel('Wind Speed (meter/second)')
plt.legend()
plt.grid(True)
plt.tight_layout()

# 라인 그래프 저장
plt.savefig(
    f'results/twins_wind_speed_line_{start_sol}-{start_sol + sol_range}.png')
plt.show()

# ------------------ 2. 점 그래프 (Scatter Plot) ------------------

# 플롯 크기 설정
plt.figure(figsize=(15, 8))

# 점 그래프 그리기
for field in fields_to_plot:
    plt.scatter(
        combined_twins_data['UTC'], combined_twins_data[field], label=f'{field} (scatter)', s=10)

# 그래프 제목 및 레이블 설정
plt.title(
    f'InSight APSS TWINS - Wind Speed (Scatter Plot for {sol_range} sols)')
plt.xlabel('UTC Time')
plt.ylabel('Wind Speed (meter/second)')
plt.legend()
plt.grid(True)
plt.tight_layout()

# 점 그래프 저장
plt.savefig(
    f'results/twins_wind_speed_scatter_{start_sol}-{start_sol + sol_range}.png')
plt.show()
