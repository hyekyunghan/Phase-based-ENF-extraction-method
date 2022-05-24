import numpy as np
from scipy.signal import medfilt

class Extractor(object):

    TDMF_TH = 2

    def __init__(self, y, Fs):
        self.y = y
        self.Fs = Fs

    def harmonics(self, enfs, f_tgt, fts):
        # Harmonics signals
        # enfs: (ENF x # of harmonics)
        # f_tgt: target frequency
        # fts: frequencies of variable 'enfs'
        scale = fts/f_tgt

        #corr_mat = np.corrcoef(enfs.T+np.random.normal())
        #idx = np.sum(corr_mat>0.5,0)>1
        #enfs = enfs[:,idx]
        #scale = scale[idx]
        #fts = fts[idx]
        #import matplotlib.pyplot as plt
        #plt.imshow(corr_mat)
        #plt.show()

        #plt.plot(enfs/scale)
        #plt.show()
        #import pdb
        #pdb.set_trace()
        #return (enfs-np.mean(enfs,0))/scale+f_tgt, fts
        return enfs/scale, fts

    def tdmf(self, enfs, fts):
        # Threshold Dependent median filter
        idx = np.std(enfs, axis=0)<self.TDMF_TH # standard deviation under TDMF_TH is filtered
        return enfs[:,idx], fts[idx]

    def mle(self, enfs, fts):
        # Maximum Likelihood Estimation
        # enfs: filtered target data
        if len(fts)==0:
            return np.array([])
        elif len(fts)==1:
            return np.squeeze(enfs)
        return np.mean(enfs, axis=1)

    def extract(self, f_tgt, fts):
        # f_tgt: target frequency (in case of U.S : 60Hz)
        # fts: target frequnecies (Harmonics of 60Hz: 60, 120, 180, ... )
        if isinstance(fts, list):
            fts = np.array(fts)

        if not isinstance(fts, np.ndarray) :
            fts = np.array([fts])

        freqs = None
        for ft in fts:
            #import pdb
            #pdb.set_trace()
            f, fs = self.extract_freq(ft)
            if freqs is None:
                freqs = f[:,np.newaxis]
            else:
                freqs = np.hstack((freqs,f[:,np.newaxis]))
        #import pdb
        #pdb.set_trace()
        freqs, fts = self.harmonics(freqs, f_tgt, fts)
        #import matplotlib.pyplot as plt
        #plt.plot(freqs)
        #plt.show()
        freqs, fts = self.tdmf(freqs, fts)
        freqs = self.mle(freqs, fts)

        return freqs, fs

    def compute_autocovariance(self,x,M):
        # For other extraction techinques, not used yet
        N=x.shape[0]
        x_vect=np.transpose(np.matrix(x))
        yn=x_vect[M-1::-1]
        R=yn*yn.H
        for indice in range(1,N-M):
            yn=x_vect[M-1+indice:indice-1:-1]
            R=R+yn*yn.H
        R=R/(N)

        return R

    #def extract(self, y, fs):
    #    y,fe = algorithm(y,fs)
    #    return enf,fe
