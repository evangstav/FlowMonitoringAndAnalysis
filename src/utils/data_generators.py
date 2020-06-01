import numpy as np


class PRBS_GEN:
    def __init__(self, length, channels):
        self.length = length
        self.channels = channels
        self.amp = np.random.randint(-5, 5, (length, channels))
        self.freq = np.random.randint(10, 100, (length, channels))

        for i in range(1, length):
            self.freq[i, :] = self.freq[i - 1, :] + self.freq[i, :]

    def random_signal(self):
        random_signal = np.zeros((self.length, self.channels))
        for j in range(self.channels):
            i = 0
            while self.freq[i, j] < self.length:
                k = self.freq[i, j]
                random_signal[k:, j] = self.amp[i, j]
                i += 1

        return random_signal

    def prbs(self):
        bins = np.zeros((self.length, self.channels))
        prbs = np.zeros((self.length, self.channels))
        for j in range(self.channels):
            i = 0
            l = 0
            while l < self.length:
                bins[l, j] = 1
                bins[l + 1, j] = 0
                l += 2
            while self.freq[i, j] < self.length:
                k = self.freq[i, j]
                prbs[k:, j] = bins[i, j]
                i += 1

        return prbs
