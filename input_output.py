# input_output.py

import scipy.io as io
import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt


def read_wav(name: str):
    wav = AudioSegment.from_wav(name)

    wav_mono = wav.set_channels(1)

    samples = np.array(wav_mono.get_array_of_samples())
    sample_rate = wav.frame_rate

    return sample_rate, samples, samples.shape[0] / sample_rate


def write_wav(samples, sample_rate, name):
    io.wavfile.write(name, sample_rate, samples)


def plot_vowels(samples, sample_rate, detected_vowels, frame_size, vowel_colors):
    plt.figure(figsize=(14, 6), dpi=120)
    time_samples = np.linspace(0, len(samples) / sample_rate, len(samples))
    plt.plot(time_samples, samples, label='Waveform', linewidth=0.5)

    legend_handles = [plt.Line2D([0], [0], color=color, lw=4, label=vowel) for vowel, color in vowel_colors.items()]

    start_vowel = None
    current_vowel = None
    for i, vowel in enumerate(detected_vowels):
        if vowel and start_vowel is None:
            start_vowel = i
            current_vowel = vowel
        elif vowel != current_vowel and start_vowel is not None:
            start_time = (start_vowel * frame_size) / sample_rate
            end_time = (i * frame_size) / sample_rate

            if current_vowel in vowel_colors:
                plt.axvspan(start_time, end_time, color=vowel_colors[current_vowel], alpha=0.3)

            start_vowel = None
            current_vowel = None
            if vowel:
                start_vowel = i
                current_vowel = vowel

    if start_vowel is not None:
        start_time = (start_vowel * frame_size) / sample_rate
        end_time = (len(detected_vowels) * frame_size) / sample_rate
        if current_vowel in vowel_colors:
            plt.axvspan(start_time, end_time, color=vowel_colors[current_vowel], alpha=0.3)

    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Vowel Detection')
    plt.legend(handles=legend_handles)
    plt.grid(True)
    plt.show()


