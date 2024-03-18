# detect_vowels.py

import sys

import input_output
import processing
import analysis
import parameters


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python detect_vowels.py <path_to_wav_file>")
        # sys.exit(1)

    # wav_file_path = sys.argv[1]
    wav_file_path = 'Wav/heed.wav'

    sample_rate, samples, length = input_output.read_wav(name=wav_file_path)

    processed_samples = processing.normalize(samples=samples)
    processed_samples = processing.trim_silence(samples=processed_samples,
                                                silence_tolerance=parameters.silence_tolerance)
    processed_samples = processing.bandpass_filter(samples=processed_samples,
                                                   sample_rate=sample_rate,
                                                   bandpass_low=parameters.bandpass_low,
                                                   bandpass_high=parameters.bandpass_high,
                                                   bandpass_order=parameters.bandpass_order)

    # Split the samples array into a list of smaller arrays for processing
    frames = processing.subdivide_samples(samples=processed_samples,
                                          frame_size=parameters.frame_size)

    # The idea for using zcr and energy is from
    # "Separation of Voiced and Unvoiced using Zero crossing rate and Energy of the Speech Signal"
    # https://monolith.asee.org/documents/zones/zone1/2008/student/ASEE12008_0044_paper.pdf
    zcr = analysis.zero_crossing_rate(frames=frames)
    energy = analysis.short_term_energy(frames=frames)
    formants, vowel_matches = analysis.calculate_formants(frames=frames,
                                                          sample_rate=sample_rate,
                                                          lpc_order=parameters.lpc_order,
                                                          vowel_formants=parameters.vowel_formants)

    # Formants may be noisy, so remove some erroneous vowel matches
    smoothed_vowel_matches = processing.smooth_vowel_list(vowel_results=vowel_matches,
                                                          window_size=10)

    # Unvoiced consonants are matched by analysis.calculate_formants, so remove them.
    result = analysis.remove_unvoiced_consonants(frames=frames,
                                                 zcr=zcr,
                                                 energy=energy,
                                                 zcr_modifier=parameters.zcr_modifier,
                                                 e_modifier=parameters.e_modifier,
                                                 smoothing_window=parameters.smoothing_window,
                                                 vowel_matches=smoothed_vowel_matches)

    input_output.plot_vowels(samples=processed_samples,
                             sample_rate=sample_rate,
                             detected_vowels=result,
                             frame_size=parameters.frame_size,
                             vowel_colors=parameters.vowel_colors)
