# analysis.py

import numpy as np
import librosa

import processing


def zero_crossing_rate(frames):
    """
    Calculate the zero crossing rate (ZCR) for each frame.

    Args:
        frames (List[np.ndarray]): A list of ndarray frames for which to calculate the ZCR.

    Returns:
        np.ndarray: An array containing the ZCR values for each frame.
    """
    zcr = np.zeros(len(frames))

    for i in range(0, len(frames)):
        # This cool one-liner was found at
        # https://stackoverflow.com/questions/44319374/how-to-calculate-zero-crossing-rate-with-pyaudio-stream-data
        zcr[i] = np.nonzero(np.diff(frames[i] > 0))[0].size

    return zcr


def short_term_energy(frames):
    """
    Calculate the short-term energy for each frame.

    Args:
        frames (List[np.ndarray]): A list of ndarray frames for which to calculate the short-term energy.

    Returns:
        np.ndarray: An array containing the short-term energy values for each frame.
    """
    energy = np.zeros(len(frames))

    for i in range(0, len(frames)):
        energy[i] = np.sum(np.square(frames[i])) / len(frames)

    return energy


def compute_lpc(frames, lpc_order):
    """
    Compute the Linear Predictive Coding (LPC) coefficients for each frame.

    Args:
        frames (List[np.ndarray]): A list of ndarray frames for which to compute the LPC coefficients.
        lpc_order (int): The order of the linear prediction.

    Returns:
        List[np.ndarray]: A list containing the LPC coefficient arrays for each frame.
    """
    coefficients = []

    for frame in frames:
        windowed_frame = frame * np.hamming(len(frame))  # Window input samples to reduce edge effects

        # Represent samples as a linear combination of previous samples
        lpc = librosa.lpc(windowed_frame, order=lpc_order)
        coefficients.append(lpc)

    return coefficients


def find_formants(coefficients, sample_rate):
    """
    Calculate the formant frequencies from the LPC coefficients for each set of coefficients.

    Args:
        coefficients (List[np.ndarray]): A list of arrays, each containing the LPC coefficients for a frame.
        sample_rate (int): The sample rate of the audio signal in Hz.

    Returns:
        List[np.ndarray]: A list of arrays, each containing the sorted formant frequencies for a frame.
    """
    formants = []

    for coefficient in coefficients:
        roots = np.roots(coefficient)
        roots = [r for r in roots if np.imag(r) >= 0]  # Only need positive part of each conjugate pair

        phase = np.angle(roots)
        frequencies = phase * (sample_rate / (2 * np.pi))  # (Rad / sample) * (sample / second / Rad) = Hz

        formants.append(np.sort(frequencies))

    return formants


def refine_formants(formants, num_formants=3):
    """
    Limit the number of formant frequencies for each set of frequencies to the most relevant ones.

    Args:
        formants (List[np.ndarray]): A list of arrays, each containing the formant frequencies for a frame.
        num_formants (int, optional): The number of formants to retain for each frame. Defaults to 3.

    Returns:
        List[np.ndarray]: A list of arrays, each containing the refined formant frequencies for a frame.
    """
    refined_formants = []

    for frequencies in formants:
        refined = [f for f in frequencies if 90 <= f <= 4000]  # This range allows for F1-F3 formants
        refined_formants.append(np.sort(refined)[:num_formants])  # Take F1-F3. F3 is currently unused

    return refined_formants


def match_vowel_patterns(refined_formants, vowel_formants):
    """
    Match each set of refined formant frequencies to the closest vowel based on Euclidean distance.

    Args:
        refined_formants (List[np.ndarray]): A list of arrays, each containing the refined formant frequencies for a frame.
        vowel_formants (dict(dict)): A dictionary mapping vowel names to their corresponding formant frequency values (F1, F2).

    Returns:
        List[str]: A list of the best matching vowels for each set of refined formant frequencies.
    """
    vowel_matches = []

    for formants in refined_formants:
        closest_distance = float('inf')
        best_match = None

        if len(formants) >= 2:
            F1, F2 = formants[0], formants[1]

            for vowel, points in vowel_formants.items():
                # Calculate the error of predicted formants
                distance = np.sqrt((points['F1'] - F1) ** 2 + (points['F2'] - F2) ** 2)

                if distance < closest_distance:
                    closest_distance = distance
                    best_match = vowel

        vowel_matches.append(best_match)

    return vowel_matches


# This usage of LPC was derived from the MATLAB example in "Formant Estimation with LPC Coefficients"
# https://www.mathworks.com/help/signal/ug/formant-estimation-with-lpc-coefficients.html
def calculate_formants(frames, sample_rate, lpc_order, vowel_formants):
    """
    Calculate and match formants from frames to predefined vowel patterns.

    Args:
        frames (List[np.ndarray]): A list of ndarray frames from an audio signal.
        sample_rate (int): The sample rate of the audio signal in Hz.
        lpc_order (int): The order of linear prediction to use when computing LPC coefficients.
        vowel_formants (dict): A dictionary mapping vowel sounds to their respective formant frequency values.

    Returns:
        List[np.ndarray]: The refined formant frequencies for each frame.
        List[str]: The best matching vowels for the refined formant frequencies.
    """
    coefficients = compute_lpc(frames, lpc_order)
    raw_formants = find_formants(coefficients, sample_rate)
    refined_formants = refine_formants(raw_formants)
    vowel_matches = match_vowel_patterns(refined_formants, vowel_formants)

    return refined_formants, vowel_matches


def remove_unvoiced_consonants(frames, zcr, energy, zcr_modifier, e_modifier, smoothing_window, vowel_matches):
    """
    Filter out unvoiced consonants from frames based on zero crossing rate, and short term energy.

    Args:
        frames (List[np.ndarray]): A list of ndarray frames from an audio signal.
        zcr (np.ndarray): An array of zero crossing rates for each frame.
        energy (np.ndarray): An array of energy values for each frame.
        zcr_modifier (float): Modifier to adjust the ZCR threshold.
        e_modifier (float): Modifier to adjust the energy threshold.
        smoothing_window (int): Window size for smoothing ZCR and energy values.
        vowel_matches (List[str]): A list of the best matching vowels for each frame.

    Returns:
        List[str]: A list with the vowel identified for each frame or None for frames identified as unvoiced consonants.
    """
    smooth_zcr = processing.smooth_values(zcr, smoothing_window)
    smooth_energy = processing.smooth_values(energy, smoothing_window)

    zcr_threshold = min(smooth_zcr) + (max(smooth_zcr) - min(smooth_zcr)) * zcr_modifier
    energy_threshold = min(smooth_energy) + (max(smooth_energy) - min(smooth_energy)) * e_modifier

    results = []
    for i in range(len(frames)):
        score = 0

        # Voiced speech tends to be low zcr, high energy
        if smooth_zcr[i] < zcr_threshold:
            score += 1
        if smooth_energy[i] > energy_threshold:
            score += 1

        detected_vowel = vowel_matches[i]

        results.append(detected_vowel if score >= 2 else None)

    return results
