# processing.py


import numpy as np
import scipy.signal as sig


def bandpass_filter(samples, sample_rate):
    low = 50 / (sample_rate / 2)
    high = 3000 / (sample_rate / 2)
    coefficients = sig.iirfilter(N=4, Wn=[low, high], btype='bandpass', ftype='butter', output='sos')
    filtered_samples = sig.sosfilt(coefficients, samples)

    return filtered_samples


def normalize(samples):
    samples_float = samples.astype(np.float32)
    max_value = np.max(np.abs(samples_float))

    if max_value > 0:
        normalized_samples = samples_float / max_value
    else:
        normalized_samples = samples_float

    return normalized_samples
