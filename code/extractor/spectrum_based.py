from extractor.extractor import Extractor
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

class Extractor(Extractor):

    def __init__(self, *args, **kwargs): # initialize
        super().__init__(*args)
        # w_t : time of window 
        # n_ol: number of overlap 

        nFFT = kwargs['nFFT'] if 'nFFT' in kwargs.keys() else None
        w_t = kwargs['w_t'] if 'w_t' in kwargs.keys() else None
        n_ol = kwargs['n_ol'] if 'n_ol' in kwargs.keys() else None

        if nFFT is not None:
            n_w = nFFT
        elif w_t is not None:
            n_w = int(self.Fs*w_t)
        else:
            n_w = 2**10

        if n_ol is None:
            n_ol = int(np.floor(n_w*.9))

        freqs, ts, spec = signal.spectrogram(self.y, self.Fs, nperseg = n_w, noverlap = n_ol)
        self.spec = spec
        self.freqs = freqs
        self.ts = ts
        self.n_w = n_w
        self.n_ol = n_ol
        #self.plot_spec()

    def plot_spec(self):
        plt.rcParams["figure.figsize"] = (10,6)
        plt.pcolormesh(self.ts, self.freqs, np.log(np.abs(self.spec)))
        plt.show()

