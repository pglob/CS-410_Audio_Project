# processing.py

import numpy as np
import scipy.signal as sig


def bandpass_filter(samples, sample_rate, bandpass_low, bandpass_high, bandpass_order):
    low = bandpass_low / (sample_rate / 2)
    high = bandpass_high / (sample_rate / 2)
    coefficients = sig.iirfilter(N=bandpass_order, Wn=[low, high], btype='bandpass', ftype='butter', output='sos')
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


def trim_silence(samples, silence_tolerance):
    start = np.where(np.abs(samples) > silence_tolerance)[0][0]
    end = np.where(np.abs(samples) > silence_tolerance)[0][-1]

    return samples[start:end+1]


def subdivide_samples(samples, frame_size):
    num_samples = len(samples)
    num_subdivisions = num_samples // frame_size

    subdivided_samples = [samples[i*frame_size:(i+1)*frame_size] for i in range(num_subdivisions)]

    return subdivided_samples


def smooth_values(values, smoothing_window):
    smoothed = []

    for i in range(len(values)):
        start = max(i - smoothing_window // 2, 0)
        end = min(i + smoothing_window // 2 + 1, len(values))
        smoothed.append(sum(values[start:end]) / (end - start))

    return smoothed


def smooth_vowel_list(vowel_results, window_size=5):
    if window_size % 2 == 0:
        window_size += 1

    half_window = window_size // 2
    smoothed_vowels = []

    for i in range(len(vowel_results)):
        start_index = max(i - half_window, 0)
        end_index = min(i + half_window + 1, len(vowel_results))

        window_elements = vowel_results[start_index:end_index]

        if window_elements:
            most_frequent = max(set(window_elements), key=window_elements.count)
            smoothed_vowels.append(most_frequent)
        else:
            smoothed_vowels.append(None)

    return smoothed_vowels
