from extractor.extractor import Extractor
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

EPS = 1e-16

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
#             y = 20*np.log10(np.abs(y))        
            #fs = freqs[idx_f-CUT-1:idx_f+CUT+2]
            fs = freqs[idx_f-CUT:idx_f+CUT+1]
#             idx = np.argmax(y)
            idx = 1
            alph = y[idx-1]
            beta = y[idx]
            gamm = y[idx+1]
            p = .5*(alph-gamm)/(alph-2*beta+gamm)
            f_a = fs[idx-1]
            f_b = fs[idx]
            f_g = fs[idx+1]
            f = (f_g-f_a)*p/2+f_b #tmp
#             f = (alph * f_a + beta * f_b + gamm * f_g)/(alph+beta+gamm)
            enf[t] = f #tmp
        return enf, self.Fs/(self.n_w-self.n_ol)

    '''
    def extract_freq(self, freq, cut_window = 3): # window size (sec)
        # extract target frequency with QIFFT
        # freq: target frequency
        # cut_window: number of referring bins

        freqs = self.freqs.reshape(-1)
        idx = np.argmin(np.abs(freqs-freq))
        idx = np.arange(idx-cut_window,idx+cut_window+1) # -cut_window ~ +cut_window

        import pdb
        pdb.set_trace()

        mat = np.log(np.abs(self.spec[idx,:]))
        mat[0,:] = mat[1,:]-1e-10
        mat[-1,:] = mat[-2,:]-1e-10
        freqs_filt = freqs[idx]

        am_mat = np.argmax(mat, axis=0)
        adj_mat = np.array([am_mat-1,am_mat,am_mat+1])
        var_mat  = mat[adj_mat,:][:,0,:]
        alph = var_mat[0,:]
        beta = var_mat[1,:]
        lmbd = var_mat[2,:]

        p = .5*(alph-lmbd)/(alph-2*beta+lmbd)/20

        base_f = freqs_filt[adj_mat][0,:]
        last_f = freqs_filt[adj_mat][2,:]
        f = (last_f-base_f)*p+base_f

        tdmf_idx = abs(p)>np.std(p)

        f[tdmf_idx] = freqs_filt[adj_mat][1,tdmf_idx] #tmp

        return f, self.Fs/(self.n_w-self.n_ol)
    '''
