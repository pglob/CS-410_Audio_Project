# main.py

import input_output
import processing
import analysis
import numpy as np


if __name__ == '__main__':
    sample_rate, samples, length = input_output.read_wav('hello.wav')

    processed_samples = processing.normalize(samples)
    processed_samples = processing.trim_silence(processed_samples)
    processed_samples = processing.bandpass_filter(processed_samples, sample_rate)

    frames = processing.subdivide_samples(processed_samples, 200)

    fft_magnitudes = analysis.fft(frames)
    fft_frequencies = analysis.calculate_frequencies(200, sample_rate)

    zcr = analysis.zero_crossing_rate(frames)
    energy = analysis.short_term_energy(frames)

    result = analysis.detect_vowels(frames, (fft_magnitudes, fft_frequencies), zcr, energy)

    input_output.plot_vowels(processed_samples, sample_rate, result)
