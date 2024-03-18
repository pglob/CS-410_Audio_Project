# processing.py

import numpy as np
import scipy.signal as sig


def bandpass_filter(samples, sample_rate, bandpass_low, bandpass_high, bandpass_order):
    """
    Apply a Butterworth bandpass filter to the input samples.

    Args:
        samples (np.ndarray): An array of audio samples to be filtered.
        sample_rate (int): The sample rate of the audio signal in Hz.
        bandpass_low (int): The lower bound of the frequency range to allow through the filter (in Hz).
        bandpass_high (int): The upper bound of the frequency range to allow through the filter (in Hz).
        bandpass_order (int): The order of the bandpass filter (the higher the order, the steeper the drop-off).

    Returns:
        np.ndarray: The bandpass-filtered audio samples.
    """
    low = bandpass_low / (sample_rate / 2)
    high = bandpass_high / (sample_rate / 2)
    coefficients = sig.iirfilter(N=bandpass_order, Wn=[low, high], btype='bandpass', ftype='butter', output='sos')
    filtered_samples = sig.sosfilt(coefficients, samples)

    return filtered_samples


def normalize(samples):
    """
    Convert input samples to 32-bit float and normalize to a range between -1 and 1.

    Args:
        samples (np.ndarray): An array of audio samples, typically integers.

    Returns:
        np.ndarray: The normalized audio samples as floating-point numbers ranging from -1 to 1.
    """
    samples_float = samples.astype(np.float32)
    max_value = np.max(np.abs(samples_float))

    if max_value > 0:
        normalized_samples = samples_float / max_value
    else:
        normalized_samples = samples_float

    return normalized_samples


def trim_silence(samples, silence_tolerance):
    """
    Trim the silence from the beginning and end of the input samples.

    Args:
        samples (np.ndarray): An array of audio samples.
        silence_tolerance (float): The amplitude level below which samples are considered silent.

    Returns:
        np.ndarray: The trimmed audio samples, with silence removed from the beginning and end.
    """
    start = np.where(np.abs(samples) > silence_tolerance)[0][0]
    end = np.where(np.abs(samples) > silence_tolerance)[0][-1]

    return samples[start:end+1]


def subdivide_samples(samples, frame_size):
    """
    Subdivide an array of samples into smaller frames.

    Args:
        samples (np.ndarray): An array of audio samples to be subdivided.
        frame_size (int): The size of each frame to which the samples are to be subdivided.

    Returns:
        List[np.ndarray]: A list of the subdivided sample frames.
    """
    num_samples = len(samples)
    num_subdivisions = num_samples // frame_size

    subdivided_samples = [samples[i*frame_size:(i+1)*frame_size] for i in range(num_subdivisions)]

    return subdivided_samples


def smooth_values(values, smoothing_window):
    """
    Smooth a sequence of values using a moving average.

    Args:
        values (np.ndarray): The sequence of values to be smoothed.
        smoothing_window (int): The size of the window used for the moving average, must be a positive odd integer.

    Returns:
        List[float]: A list of the smoothed values.
    """
    smoothed = []

    for i in range(len(values)):
        start = max(i - smoothing_window // 2, 0)
        end = min(i + smoothing_window // 2 + 1, len(values))
        smoothed.append(sum(values[start:end]) / (end - start))

    return smoothed


def smooth_vowel_list(vowel_results, window_size):
    """
    Smooth a list of vowel results over a specified window size to improve consistency.

    Args:
        vowel_results (List[str]): A list of vowel identifications, where each element is a vowel label or None.
        window_size (int): The size of the window over which to smooth the vowel results.

    Returns:
        List[str]: A list of the smoothed vowel results.
        """
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
