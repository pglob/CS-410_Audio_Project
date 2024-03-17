# main.py

import input_output
import processing
import analysis
import parameters


if __name__ == '__main__':
    sample_rate, samples, length = input_output.read_wav('heed.wav')

    processed_samples = processing.normalize(samples)
    processed_samples = processing.trim_silence(processed_samples, parameters.silence_tolerance)
    processed_samples = processing.bandpass_filter(processed_samples, sample_rate, parameters.bandpass_low, parameters.bandpass_high, parameters.bandpass_order)

    input_output.write_wav(processed_samples, sample_rate, 'out.wav')

    frames = processing.subdivide_samples(processed_samples, parameters.frame_size)

    # The idea for using zcr and energy is from
    # "Separation of Voiced and Unvoiced using Zero crossing rate and Energy of the Speech Signal"
    # https://monolith.asee.org/documents/zones/zone1/2008/student/ASEE12008_0044_paper.pdf
    zcr = analysis.zero_crossing_rate(frames)
    energy = analysis.short_term_energy(frames)
    formants, vowel_matches = analysis.calculate_formants(frames, sample_rate, parameters.lpc_order, parameters.vowel_formants)

    result = analysis.detect_vowels(frames, zcr, energy, parameters.zcr_modifier, parameters.e_modifier, parameters.smoothing_window, vowel_matches)

    input_output.plot_vowels(processed_samples, sample_rate, result, parameters.frame_size, parameters.vowel_colors)
