#from extractor.extractor import Extractor
from extractor.spectrum_based import Extractor
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

#EPS = 1e-16

class Extractor(Extractor):

    def extract_freq(self, freq, cut_window = 1): # window size (sec)
        # extract target frequency with QIFFT
        # freq: target frequency
        # cut_window: number of referring bins
        freqs = self.freqs
        ts = self.ts
        spec = self.spec
        CUT = cut_window

        enf = np.zeros((spec.shape[1]))

        #idx_f = np.argmin(np.abs(freqs-freq))
        #y = spec[idx_f-CUT:idx_f+CUT+1,:]
        #y = np.hstack((EPS,np.hstack((y,EPS))))
        #y = np.log10(np.abs(y))
        #fs = freqs[idx_f-CUT-1:idx_f+CUT+2]
        #idx = np.argmax(y)

        for t in range(spec.shape[1]):

            idx_f = np.argmin(np.abs(freqs-freq))
            y = spec[idx_f-CUT:idx_f+CUT+1,t]
            #y = 20*np.log10(np.abs(y))
            y = np.abs(y)

            fs = freqs[idx_f-CUT:idx_f+CUT+1]
            enf[t] = sum(y*fs)/sum(y)

        return enf, self.Fs/(self.n_w-self.n_ol)

