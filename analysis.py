# analysis.py


import numpy as np
import scipy.signal as sig
import math

import processing


def fft(frames):
    fft_outputs = [np.fft.rfft(frame) for frame in frames]

    magnitudes = [np.abs(fft_output) for fft_output in fft_outputs]

    return magnitudes


def calculate_frequencies(frame_length, sample_rate):
    freq_resolution = sample_rate / frame_length

    frequencies = [i * freq_resolution for i in range(frame_length // 2 + 1)]

    return frequencies


def zero_crossing_rate(frames):
    zcr = np.zeros(len(frames))

    for i in range(0, len(frames)):
        # This cool one-liner was found at
        # https://stackoverflow.com/questions/44319374/how-to-calculate-zero-crossing-rate-with-pyaudio-stream-data
        zcr[i] = np.nonzero(np.diff(frames[i] > 0))[0].size

    return zcr


def short_term_energy(frames):
    energy = np.zeros(len(frames))

    for i in range(0, len(frames)):
        energy[i] = np.sum(np.square(frames[i])) / len(frames)

    return energy


def detect_vowels(frames, fft_result, zcr, energy):
    # check for vowel formants in frequencies
    # check for regions of low zcr and high energy to find voiced speech (includes vowels)
    # checkout https://monolith.asee.org/documents/zones/zone1/2008/student/ASEE12008_0044_paper.pdf
    fft_magnitudes, fft_frequencies = fft_result

    smooth_zcr = processing.smooth_values(zcr)
    smooth_energy = processing.smooth_values(energy)

    zcr_threshold = min(smooth_zcr) + (max(smooth_zcr) - min(smooth_zcr)) * 0.4
    energy_threshold = min(smooth_energy) + (max(smooth_energy) - min(smooth_energy)) * 0.5

    results = []
    for i in range(len(smooth_zcr)):
        score = 0
        if smooth_zcr[i] < zcr_threshold:
            score += 1
        if smooth_energy[i] > energy_threshold:
            score += 1

        results.append(score >= 2)

    return results
