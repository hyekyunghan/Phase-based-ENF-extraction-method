import cv2
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from scipy import io
import config
import os

SEP = os.path.sep
MAX_FRAME_N = 100 #tmp

class Video(object):

    cnt = 0
    mat = None

    def __init__(self, filename):
        self.filename = filename
        cap = cv2.VideoCapture(filename)
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.n_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.n_c = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.n_r = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.n_t = (self.n_r, self.n_c)[self.get_axis_t()]
        self.f_st = 0
        self.f_ed = 0
        print('File  Name : '+ str(self.filename))
        print('Total Frame: '+ str(self.n_frame))
        print('Frame Size : %d x %d' % (self.n_c, self.n_r))
        print('FPS        : %f' % (self.fps))

    def set_frame(self, f_st, f_ed):
        self.f_st = int(f_st)
        self.f_ed = int(f_ed)

    def press(self, event):
        if event.key == 'c':
            if self.f_st==0:
                self.f_st = self.cnt
            else:
                self.f_ed = self.cnt
        else:
            pass

    def show_video(self):
        filename = self.filename
        cap = cv2.VideoCapture(filename)

        cnt_frame = 0
        tmp_frame = np.zeros((self.n_r, self.n_c, 3))

        print('Skipping the video to frame '+str(self.f_st)) #tmp change skipping internal function
        for i in tqdm(range(self.f_st)):
            ret, frame = cap.read()
            tmp_frame = frame
            cnt_frame += 1

        while(self.f_ed==0 or cnt_frame<self.f_ed):
            ret, frame = cap.read()
            if ret == True:
                plt.clf()
                figure = abs(frame.astype('float64').mean(2)-tmp_frame.mean(2)) #tmp

                figure = figure*1*1 #tmp
                figure = figure.astype('uint8')

                plt.imshow(figure)
                plt.title(cnt_frame)
                #plt.imshow(frame)
                plt.pause(1/self.fps)

            tmp_frame = frame

            cnt_frame += 1

        return

        while(self.f_st==0 or self.f_ed==0):
            ret, frame = cap.read()

            if ret == True:
                plt.clf()
                ax = plt.gca()
                ax.figure.canvas.mpl_connect('key_press_event', self.press)
                figure = abs(frame.astype('float64').mean(2)-tmp_frame.mean(2)) #tmp

                figure = figure*1*5 #tmp
                figure = figure.astype('uint8')

                plt.imshow(frame)
                if self.f_st==0:
                    plt.title('Press C to capture: '+str(self.cnt), color='black')
                else:
                    plt.title('Capturing: '+str(self.cnt), color='red')

                plt.pause(1/self.fps)
                self.cnt += 1

                if self.f_st!=0:
                    if self.mat is None:
                        self.mat = np.zeros((MAX_FRAME_N,) + frame.shape)
                        #self.mat = frame1
                    #else:
                        #self.mat = np.vstack((self.mat, frame1))
                    self.mat[cnt_frame,:] = frame
                    cnt_frame = cnt_frame + 1
                        #mat = np.stack((mat, frame), axis=0)

                tmp_frame = frame

        self.mat = self.mat[self.f_st:self.f_ed,:]
        plt.close()
        plt.figure(1)
        self.cnt = 0

    def show_video_set_vector(self): #tmp -> do not change f_st, f_ed
        filename = self.filename
        cap = cv2.VideoCapture(filename)

        fig1 = plt.figure()

        cnt_frame = 0

        tmp_frame = np.zeros((self.n_r, self.n_c, 3))

        while(self.f_st==0 or self.f_ed==0):
            ret, frame = cap.read()

            if ret == True:
                plt.clf()
                ax = plt.gca()
                ax.figure.canvas.mpl_connect('key_press_event', self.press)
                figure = abs(frame.astype('float64').mean(2)-tmp_frame.mean(2)) #tmp
                #figure = figure+3*5
                figure = figure*1*5 #tmp
                figure = figure.astype('uint8')
                #plt.imshow(figure) #tmp
                plt.imshow(frame)
                if self.f_st==0:
                    plt.title('Press C to capture: '+str(self.cnt), color='black')
                else:
                    plt.title('Capturing: '+str(self.cnt), color='red')

                #plt.show()
                #plt.show(block=False)
                plt.pause(1/self.fps)
                self.cnt += 1

                if self.f_st!=0:
                    #frame1 = np.expand_dims(frame,0)
                    if self.mat is None:
                        self.mat = np.zeros((MAX_FRAME_N,) + frame.shape)
                        #self.mat = frame1
                    #else:
                        #self.mat = np.vstack((self.mat, frame1))
                    self.mat[cnt_frame,:] = frame
                    cnt_frame = cnt_frame + 1
                        #mat = np.stack((mat, frame), axis=0)

                tmp_frame = frame

        self.mat = self.mat[self.f_st:self.f_ed,:]
        plt.close()
        plt.figure(1)
        self.cnt = 0

    def set_frame_offset(self, f_st, f_ed):
        if f_st > self.n_frame:
            self.f_st = 0
            print('Start Frame doesn\'t exist')
        else:
            self.f_st = f_st

        if self.n_frame < f_ed:
            self.f_ed = self.n_frame
            print('End Frame doesn\'t exist')
        else:
            self.f_ed = f_ed
        return self.f_st, self.f_ed

    def set_video(self, f_st, f_ed):
        f_st, f_ed = self.set_frame_offset(f_st, f_ed)
        filename = self.filename
        cap = cv2.VideoCapture(filename)

        cap.set(cv2.CAP_PROP_POS_FRAMES,f_st-1)

        cnt_frame = 0

        self.mat = np.zeros((f_ed-f_st,) + (self.n_r, self.n_c,3), dtype='float')
        for f_n in np.arange(f_st, f_ed):
            ret, frame = cap.read()
            self.mat[cnt_frame,:] = frame
            cnt_frame = cnt_frame + 1


    def set_vector(self, f_st, f_ed):
        f_st, f_ed = self.set_frame_offset(f_st, f_ed)
        filename = self.filename
        cap = cv2.VideoCapture(filename)

        cap.set(cv2.CAP_PROP_POS_FRAMES,f_st)

        cnt_frame = 0

        axis_t = self.get_axis_t()
        n_t = self.n_t
        self.vec = np.zeros((f_ed-f_st,) + (n_t,), dtype='float') # N x row
        print('Reading frame')
        #print('get_axis_m:',self.get_axis_m())

        for f_n in tqdm(np.arange(f_st, f_ed)):
            ret, frame = cap.read()
            if ret:
                self.vec[cnt_frame,:] = np.mean(frame, axis=(self.get_axis_m(),2))
                cnt_frame = cnt_frame + 1
            else:
                break

    def set_vector_with_motion(self, f_st, f_ed):
        f_st, f_ed = self.set_frame_offset(f_st, f_ed)
        filename = self.filename
        cap = cv2.VideoCapture(filename)

        cap.set(cv2.CAP_PROP_POS_FRAMES,f_st)

        cnt_frame = 0

        axis_t = self.get_axis_t()
        n_t = self.n_t
        self.vec = np.zeros((f_ed-f_st,) + (n_t,), dtype='float') # N x row
        print('Reading frame')
        #print('get_axis_m:',self.get_axis_m())

        for f_n in tqdm(np.arange(f_st, f_ed)):
            ret, frame = cap.read()
            #import pdb
            #pdb.set_trace()
            D = frame.shape[1]
            #frame = frame[:,:int(D/2),:] # object at right
            frame = frame[:,int(D/2):,:] #object at left
            #import pdb
            #pdb.set_trace()
            if ret:
                self.vec[cnt_frame,:] = np.mean(frame, axis=(self.get_axis_m(),2))
                cnt_frame = cnt_frame + 1
            else:
                break


    def set_vector_with_motion_advance(self, f_st, f_ed):
        f_st, f_ed = self.set_frame_offset(f_st, f_ed)
        filename = self.filename
        cap = cv2.VideoCapture(filename)

        cap.set(cv2.CAP_PROP_POS_FRAMES,f_st)

        cnt_frame = 0

        axis_t = self.get_axis_t()
        n_t = self.n_t
        n_c = self.n_c
        #self.vec = np.zeros((f_ed-f_st,) + (n_t,), dtype='float') # N x row
        self.vec = np.zeros((f_ed-f_st,) + (n_t,)+ (n_c,), dtype='float') # N x row x column
        print('Reading frame')
        #print('get_axis_m:',self.get_axis_m())

        for f_n in tqdm(np.arange(f_st, f_ed)):
            ret, frame = cap.read()
            if ret:
                self.vec[cnt_frame,:,:] = np.mean(frame, axis=2)
                cnt_frame = cnt_frame + 1
            else:
                break

        vec = self.vec
        for n in tqdm(np.arange(f_st, f_ed)):
            vec_cp = np.delete(vec, n, axis=0) # Remaining frames except for the nth frame
            vec_stc = np.where(vec_cp==vec[n,:,:], vec_cp, 0) # Select only static regions having the same pixels with the n-th frame
            self.vec[n,:,:] = self.vec[n,:,:] - np.mean(vec_stc, axis=0)

        self.vec = np.mean(self.vec, axis=(2))

    def get_vector_path(self):
        fname = self.filename.split(SEP)[-1]
        return config.DIR_OUTPUT+config.DIR_VIDEO_VEC+fname+'.npy'

    def get_vector_path_with_motion(self):
        fname = self.filename.split(SEP)[-1]
        return config.DIR_OUTPUT+config.DIR_VIDEO_VEC_MOTION+fname+'.npy'

    def save_vector(self): #tmp F_ST, F_ED as input
        if self.vec is None:
            print('video vector is empty')
        else:
            io.savemat(self.get_vector_path(), {'vec':self.vec, 'Fs':self.fps})
            print('video vector is saved')

    def save_vector_with_motion(self): #tmp F_ST, F_ED as input
        if self.vec is None:
            print('video vector is empty')
        else:
            io.savemat(self.get_vector_path_with_motion(), {'vec':self.vec, 'Fs':self.fps})
            print('video vector is saved')

    def load_vector(self): #tmp: F_ST, F_ED should be included in inputs
        try:
            item = io.loadmat(self.get_vector_path())
            self.vec = item['vec']
            self.fps = item['fps']
        except Exception:
            print('File cannot be loaded')

    def load_vector_with_motion(self): #tmp: F_ST, F_ED should be included in inputs
        try:
            item = io.loadmat(self.get_vector_path_with_motion())
            self.vec = item['vec']
            self.fps = item['fps']
        except Exception:
            print('File cannot be loaded')

    def get_axis_t(self): # time axis, smaller
        axis_t = 0 if self.n_r < self.n_c else 1
        return axis_t

    def get_axis_m(self): # opposite of time axis
        axis_m = 1 if self.n_r < self.n_c else 0
        return axis_m

