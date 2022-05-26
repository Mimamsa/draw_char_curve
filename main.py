import numpy as np
import matplotlib.pyplot as plt
import math
from common.TimeSeries import TimeSeries
from common.ForceDataReader import force_data_read
from common.ResponseDataReader import response_data_reader
from scipy.signal import find_peaks


# CSV_FILE = '../../driver/Mike/insole1_rb_p8-0.csv'
# HDF5_FILE = '../../driver/2021_design/Tactile_Sensor_Recording/recordings/rec_2022-05-20_16-19-37_p8-0/touch.hdf5'

CSV_FILE = '../../driver/Mike/insole1_rt_p10-26.csv'
HDF5_FILE = '../../driver/2021_design/Tactile_Sensor_Recording/recordings/rec_2022-05-20_16-40-31_p10-26/touch.hdf5'

# CSV_FILE = '../../driver/Mike/insole1_lb_p3-1.csv'
# HDF5_FILE = '../../driver/2021_design/Tactile_Sensor_Recording/recordings/rec_2022-05-20_16-27-03_p3-1/touch.hdf5'

# CSV_FILE = '../../driver/Mike/insole1_lt_p2-26.csv'
# HDF5_FILE = '../../driver/2021_design/Tactile_Sensor_Recording/recordings/rec_2022-05-20_17-43-02_p2-26/touch.hdf5'

# CSV_FILE = '../../driver/Mike/insole1_lt_p5-16.csv'
# HDF5_FILE = '../../driver/2021_design/Tactile_Sensor_Recording/recordings/rec_2022-05-20_17-32-55_p5-16/touch.hdf5'


PT_LOC = [10, 26]


def find_avg_diff(f_ts, r_ts):
    """Find average time difference (sec) between 2 time series """
    f_peaks, _ = find_peaks(f_ts.value, distance=2000, prominence=10)
    r_peaks, _ = find_peaks(r_ts.value, distance=130, prominence=5)

    # TODO: Check if f_peaks and r_peaks are empty

    ret = []
    for i in range(10):
        time_diff = r_ts.time[r_peaks[i]]-f_ts.time[f_peaks[i]]
        ret.append(time_diff)

    # Debug
    print('Time difference of 10 peaks: {}'.format(ret))

    return np.median(ret)


def resample(time_series, window_size=0.5, period=0.5):
    """
    """
    i = 0
    time_elapsed = math.floor(time_series.time[i])

    ret = TimeSeries()

    while time_elapsed+period < time_series.time[-1]:

        n_i = time_series.find_nearest_index(time_elapsed)
        lo_i, up_i = time_series.get_index_within_time_range(n_i, radius=window_size)
        
        avg_val = sum(time_series.value[lo_i:up_i+1])/(up_i-lo_i+1)
        ret.append(time_elapsed, avg_val)

        i += 1
        time_elapsed += period

    return ret


def main():

    f_ts = force_data_read(CSV_FILE)
    r_ts = response_data_reader(HDF5_FILE, pt_loc=PT_LOC)

    # Align two time series by peaks
    time_diff = find_avg_diff(f_ts, r_ts)
    print('Average time difference: {}'.format(time_diff))
    f_ts.align_time(time_diff)

    # print(f_ts.time[0], r_ts.time[0])
    plt.plot(f_ts.time, f_ts.value, "-", color="gray")
    plt.plot(r_ts.time, r_ts.value, "-", color="blue")
    plt.show()

    # Resampling
    re_r_ts = resample(r_ts)
    re_f_ts = resample(f_ts)

    # print(re_f_ts.time[0], re_r_ts.time[0])
    plt.plot(re_f_ts.time, re_f_ts.value, "-", color="gray")
    plt.plot(re_r_ts.time, re_r_ts.value, "-", color="blue")
    plt.show()


    i = re_r_ts.find_nearest_index(re_f_ts.time[0])

    print(len(re_f_ts.value))
    print(re_r_ts.time[i], re_f_ts.time[0])
    plt.plot(re_r_ts.value[i:400+i], re_f_ts.value[0:400], "-", color="blue")
    plt.show()


if __name__=='__main__':
    main()