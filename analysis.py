# analysis.py

import numpy as np
import librosa
import processing


def fft(frames):
    fft_outputs = [np.fft.rfft(frame) for frame in frames]

    magnitudes = [np.abs(fft_output) for fft_output in fft_outputs]

    return magnitudes


def calculate_frequencies(sample_rate, frame_size):
    freq_resolution = sample_rate / frame_size

    frequencies = [i * freq_resolution for i in range(frame_size // 2 + 1)]

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


def compute_lpc(frames, lpc_order):
    coefficients = []

    for frame in frames:
        windowed_frame = frame * np.hamming(len(frame))  # Window input samples to reduce edge effects

        # Represent samples as a linear combination of previous samples
        lpc = librosa.lpc(windowed_frame, order=lpc_order)
        coefficients.append(lpc)

    return coefficients


def find_formants(coefficients, sample_rate):
    formants = []

    for coefficient in coefficients:
        roots = np.roots(coefficient)
        roots = [r for r in roots if np.imag(r) >= 0]  # Only need positive part of each conjugate pair

        phase = np.angle(roots)
        frequencies = phase * (sample_rate / (2 * np.pi))  # (Rad / sample) * (sample / second / Rad) = Hz

        formants.append(np.sort(frequencies))

    return formants


def refine_formants(formants, num_formants=3):
    refined_formants = []

    for frequencies in formants:
        refined = [f for f in frequencies if 90 <= f <= 4000]  # This range allows for F1-F3 formants
        refined_formants.append(np.sort(refined)[:num_formants])  # Take F1-F3. F3 is currently unused

    return refined_formants


def match_vowel_patterns(refined_formants, vowel_formants):
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
    coefficients = compute_lpc(frames, lpc_order)
    raw_formants = find_formants(coefficients, sample_rate)
    refined_formants = refine_formants(raw_formants)
    vowel_matches = match_vowel_patterns(refined_formants, vowel_formants)

    return refined_formants, vowel_matches


def detect_vowels(frames, zcr, energy, zcr_modifier, e_modifier, smoothing_window, vowel_matches):
    smooth_zcr = processing.smooth_values(zcr, smoothing_window)
    smooth_energy = processing.smooth_values(energy, smoothing_window)

    zcr_threshold = min(smooth_zcr) + (max(smooth_zcr) - min(smooth_zcr)) * zcr_modifier
    energy_threshold = min(smooth_energy) + (max(smooth_energy) - min(smooth_energy)) * e_modifier

    results = []
    for i in range(len(frames)):
        score = 0
        if smooth_zcr[i] < zcr_threshold:
            score += 1
        if smooth_energy[i] > energy_threshold:
            score += 1

        detected_vowel = vowel_matches[i]
        if detected_vowel:
            score += 1

        results.append(detected_vowel if score >= 2 else None)

    return results
