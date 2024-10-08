import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# print(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from scipy import signal
import numpy as np
import obspy
import matplotlib.pyplot as plt
import pandas as pd
from utils import sols_to_earth_date



class SEISData:
    def __init__(self, start_sol, sol_range, channel='BHU', data_path='downloads/seis'):
        self.start_sol = start_sol
        self.sol_range = sol_range
        self.data_path = data_path
        self.channel = channel.lower()
        self.file_names = self._get_file_names()
        self.stream = self._load_data()
        
    def _get_file_names(self):
        file_names = []
        for sol_number in range(self.start_sol, self.start_sol + self.sol_range):
            date = sols_to_earth_date(sol_number)
            year = date.year
            doy = date.timetuple().tm_yday
            found = False
            for filename in sorted(os.listdir(self.data_path)):
                if (".mseed" in filename and
                    f"{doy}" in filename and
                    f"{year}" in filename and
                        self.channel in filename.lower()):
                    file_names.append(os.path.join(self.data_path, filename))
                    found = True
                    break
            if not found:
                print(f"SEIS file for sol {sol_number} not found.")
        return file_names

    def _load_data(self):
        if not self.file_names:
            raise FileNotFoundError("No SEIS files found.")
        combined_stream = obspy.read(self.file_names[0])
        for file in self.file_names[1:]:
            combined_stream += obspy.read(file)
        combined_stream.merge(method=1)
        return combined_stream

    def filter_data(self, minfreq, maxfreq):
        self.filtered_stream = self.stream.copy()
        self.filtered_stream = self.filtered_stream.split()
        self.filtered_stream.filter('bandpass', freqmin=minfreq, freqmax=maxfreq)
        return self.filtered_stream

    def plot_waveform(self, output_path):
        tr = self.stream[0]
        tr_times = tr.times()
        tr_data = tr.data

        plt.figure(figsize=(10, 5))
        plt.plot(tr_times, tr_data)
        plt.xlabel('Time (s)', fontweight='bold')
        plt.ylabel('Amplitude', fontweight='bold')
        plt.title('SEIS Waveform')
        plt.savefig(output_path)
        plt.close()

    def plot_spectrogram(self, minfreq, maxfreq, output_path):
        tr = self.filtered_stream[0]
        f, t, sxx = signal.spectrogram(tr.data, tr.stats.sampling_rate)
        sxx = np.sqrt(sxx + 1e-1000)
        sxx = np.log10(sxx + 1e-1000)

        plt.figure(figsize=(10, 5))
        plt.pcolormesh(t, f, sxx, shading='gouraud', cmap='jet')
        plt.ylim([minfreq, maxfreq])
        plt.yscale('log')
        plt.yticks([0.1, 1, 10])
        plt.xlabel('Time (s)', fontweight='bold')
        plt.ylabel('Frequency (Hz)', fontweight='bold')
        plt.title('SEIS Spectrogram')
        cbar = plt.colorbar(orientation='horizontal')
        cbar.set_label('Power ((m/s)/sqrt(Hz))', fontweight='bold')
        plt.savefig(output_path)
        plt.close()


class TWINSData:
    def __init__(self, start_sol, sol_range, data_path):
        self.start_sol = start_sol
        self.sol_range = sol_range
        self.data_path = data_path
        self.file_names = self._get_file_names()
        self.data_frame = self._load_data()

    def _get_file_names(self):
        file_names = []
        for sol_number in range(self.start_sol, self.start_sol + self.sol_range):
            found = False
            for filename in sorted(os.listdir(self.data_path)):
                if ".csv" in filename and f"{sol_number}" in filename:
                    file_names.append(os.path.join(
                        self.data_path, filename))
                    found = True
                    break
            if not found:
                print(f"TWINS file for sol {sol_number} not found.")
        return file_names

    def _load_data(self):
        if not self.file_names:
            raise FileNotFoundError("No TWINS files found.")
        data_frames = []
        for file_name in self.file_names:
            df = pd.read_csv(file_name)
            df['UTC'] = pd.to_datetime(df['UTC'], format='%Y-%jT%H:%M:%S.%fZ')
            data_frames.append(df)
        combined_df = pd.concat(data_frames, ignore_index=True)
        return combined_df

    def plot_wind_speed(self,  output_path, plot_type='line'):
        plt.figure(figsize=(15, 8))
        if plot_type == 'line':
            plt.plot(
                self.data_frame['UTC'], self.data_frame['HORIZONTAL_WIND_SPEED'], label='Wind Speed')
        elif plot_type == 'scatter':
            plt.scatter(
                self.data_frame['UTC'], self.data_frame['HORIZONTAL_WIND_SPEED'], s=10, label='Wind Speed')
        else:
            raise ValueError("plot_type must be 'line' or 'scatter'")
        plt.title(
            f'InSight APSS TWINS - Wind Speed ({plot_type.capitalize()} Plot)')
        plt.xlabel('UTC Time')
        plt.ylabel('Wind Speed (m/s)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()


class PSData:
    def __init__(self, start_sol, sol_range, data_path):
        self.start_sol = start_sol
        self.sol_range = sol_range
        self.data_path = data_path
        self.file_names = self._get_file_names()
        self.data_frame = self._load_data()

    def _get_file_names(self):
        file_names = []
        for sol_number in range(self.start_sol, self.start_sol + self.sol_range):
            found = False
            for filename in sorted(os.listdir(self.data_path)):
                if ".csv" in filename and f"{sol_number}" in filename:
                    file_names.append(os.path.join(self.data_path, filename))
                    found = True
                    break
            if not found:
                print(f"PS file for sol {sol_number} not found.")
        return file_names

    def _load_data(self):
        if not self.file_names:
            raise FileNotFoundError("No PS files found.")
        data_frames = []
        for file_name in self.file_names:
            df = pd.read_csv(file_name)
            # UTC 열을 datetime 형식으로 변환
            df['UTC'] = pd.to_datetime(df['UTC'], format='%Y-%jT%H:%M:%S.%fZ')
            data_frames.append(df)
        combined_df = pd.concat(data_frames, ignore_index=True)
        return combined_df

    def plot_pressure(self, output_path, plot_type='line'):
        plt.figure(figsize=(15, 8))
        if plot_type == 'line':
            plt.plot(
                self.data_frame['UTC'], self.data_frame['PRESSURE'], label='Pressure')
        elif plot_type == 'scatter':
            plt.scatter(
                self.data_frame['UTC'], self.data_frame['PRESSURE'], s=10, label='Pressure')
        else:
            raise ValueError("plot_type must be 'line' or 'scatter'")
        plt.title(
            f'InSight APSS PS - Pressure ({plot_type.capitalize()} Plot)')
        plt.xlabel('UTC Time')
        plt.ylabel('Pressure (Pa)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
