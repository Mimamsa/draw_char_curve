import numpy as np
import h5py
from .TimeSeries import TimeSeries


def response_data_reader(file_path, pt_loc):
    """ """
    f = h5py.File(file_path, 'r')
    ret = TimeSeries()
    pressure_maps = np.array(f['pressure'])
    pressure_s = list(pressure_maps[:, pt_loc[0], pt_loc[1]])

    # TODO: Do not access attribute directly.
    ret.time = list(f['ts'])
    ret.value = pressure_s
    f.close()
    return ret
