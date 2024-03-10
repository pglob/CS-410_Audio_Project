# analysis.py


import numpy as np
import scipy.signal as sig


def fft(samples, sample_rate):
    fft_output = np.fft.rfft(samples)

    magnitudes = np.abs(fft_output)

    # frequencies = np.fft.rfftfreq(samples.size, d=1 / sample_rate)

    return magnitudes


def zero_crossing_rate(samples):
    pass


def short_term_energy(samples):
    pass


def detect_vowels(samples, frequencies, zcr, energy):
    # check for vowel formants in frequencies
    # check for regions of low zcr and high energy to find voiced speech (includes vowels)
    # checkout https://monolith.asee.org/documents/zones/zone1/2008/student/ASEE12008_0044_paper.pdf
    pass
