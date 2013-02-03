"""@package smooth
@author: Neuza Nunes"""

import numpy as np
import doctest
import numpy


def smooth(input_signal, window_len = 10, window ='hanning'):
    """
    @brief: Smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    @param: input_signal: array-like
                               the input signal 
                 window_len: int
                             the dimension of the smoothing window. the default is 10.
                 window: string. 
                         the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 
                         'blackman'. flat window will produce a moving average smoothing. the 
                         default is 'hanning'.

    @return: signal_filt: array-like
                the smoothed signal.
        
    @example:
                time = linspace(-2,2,0.1)
                input_signal = sin(t)+randn(len(t))*0.1
                signal_filt = smooth(x)
                
                
    @see also:  numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
                scipy.signal.lfilter
 
 
    @todo: the window parameter could be the window itself if an array instead of a string
    
    @bug: if window_len is equal to the size of the signal the returning signal is smaller.
    """ 
     
    if input_signal.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if input_signal.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."
        
    if window_len < 3:
        return input_signal
    
    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    sig = np.r_[2*input_signal[0]-input_signal[window_len:1:-1], input_signal, 
                   2*input_signal[-1]-input_signal[-1:-window_len:-1]]
    
    if window == 'flat': #moving average
        win = np.ones(window_len,'d')
    else:
        win = eval('np.'+window+'(window_len)')
    
    sig_conv = np.convolve(win/win.sum(), sig, mode='same')
    return sig_conv[window_len-1:-window_len+1]

# Todo compose a demo and test files

if __name__ == '__main__':

    from scipy.signal import lfilter, butter
    from scipy import sin, arange, pi, randn
    from filtfilt import filtfilt

    from pylab import plot, legend, show, hold 

    TIME = arange(-1, 1, .01)
    INPUT_SIGNAL = sin(2*pi*TIME*.5+2)
    INPUT_SIGNAL_N = INPUT_SIGNAL+randn(len(TIME))*0.05

    [COEFF_B, COEFF_A] = butter(3, 0.05)

    SIGNAL_LOWFILT = lfilter(COEFF_B, COEFF_A, INPUT_SIGNAL_N)
    SIGNAL_FILT = filtfilt(COEFF_B, COEFF_A, INPUT_SIGNAL_N)


    plot(INPUT_SIGNAL,'c')
    hold(True)
    plot(INPUT_SIGNAL_N,'k')
    plot(SIGNAL_LOWFILT,'r')
    plot(SIGNAL_FILT,'g')
    legend(('original', 'noisy signal', 
            'lfilter - butter 3 order', 'filtfilt - butter 3 order'))
    hold(False)
    show()
doctest.testmod()
