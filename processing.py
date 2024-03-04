# processing.py


import numpy as np
import scipy.signal as sig


def bandpass_filter(samples):
    coefficients = sig.iirfilter(N=4, Wn=(50, 3000), btype='bandpass', ftype='butter', output='sos')
    filtered_samples = sig.sosfilt(coefficients, samples)

    return filtered_samples


def normalize():
    pass
