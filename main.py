# main.py

import input_output
import processing
import analysis


if __name__ == '__main__':
    sample_rate, samples = input_output.read_wav('test.wav')

    processed_samples = processing.bandpass_filter(samples)
    # processed_samples = processing.normalize(samples)

    frequencies = analysis.fft(processed_samples)
    zcr = analysis.zero_crossing_rate(samples)
    energy = analysis.short_term_energy(samples)

    result = analysis.detect_vowels(processed_samples, frequencies, zcr, energy)
