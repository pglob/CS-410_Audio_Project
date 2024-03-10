# main.py

import input_output
import processing
import analysis


if __name__ == '__main__':
    sample_rate, samples, length = input_output.read_wav('hello.wav')

    processed_samples = processing.normalize(samples)
    processed_samples = processing.bandpass_filter(processed_samples, sample_rate)

    #frequencies = analysis.fft(processed_samples, sample_rate)

    #input_output.write_wav(processed_samples, sample_rate, 'test')

    #zcr = analysis.zero_crossing_rate(samples)
    #energy = analysis.short_term_energy(samples)

    #result = analysis.detect_vowels(processed_samples, frequencies, zcr, energy)
