# analysis.py


import numpy as np
import scipy.signal as sig


def fft(samples):
    frequencies = np.fft.rfft(samples)

    return frequencies


def zero_crossing_rate(samples):
    pass


def short_term_energy(samples):
    pass


def detect_vowels(samples, frequencies, zcr, energy):
    # check for vowel formants in frequencies
    # check for regions of low zcr and high energy to find voiced speech (includes vowels)
    # checkout https://monolith.asee.org/documents/zones/zone1/2008/student/ASEE12008_0044_paper.pdf
    pass
