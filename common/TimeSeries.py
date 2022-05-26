import numpy as np


class TimeSeries(object):

    def __init__(self):
        self.time = []
        self.value = []

    def __str__(self):
        return '{}, {}'.format(self.time, self.value)

    def append(self, t, v):
        self.time.append(t)
        self.value.append(v)

    def extend(self, ts):
        self.time.extend(ts.time)
        self.value.extend(ts.value)
        
    def get_time(self):
        return np.array(self.time)
        
    def get_value(self):
        return np.array(self.value)
        
    def align_time(self, time_diff):
        self.time = list(map(lambda x: x+time_diff, self.time))

    def find_nearest_index(self, value):
        """
        See https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
        """
        array = np.asarray(self.time)
        idx = (np.abs(array - value)).argmin()
        return idx

    def get_index_within_time_range(self, i, radius):
        t = self.time[i]

        j = 0
        while self.time[i+j] < t+radius:
            u = i+j
            j+=1
            if i+j >= len(self.time):
                break

        j = 0
        while self.time[i+j] >= t-radius:
            l = i+j
            j-=1
            if i+j <= 0:
                break

        return l, u