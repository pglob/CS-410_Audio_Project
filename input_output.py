# input_output.py

import scipy.io as io
import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt


def read_wav(name):
    """
    Read a WAV file and convert it to mono.

    Args:
        name (str): The file name or path to the WAV file to be read.

    Returns:
        int: The sample rate of the audio in Hz.
        np.ndarray: The audio samples in a numpy array.
        float: The duration of the audio in seconds.
    """
    wav = AudioSegment.from_wav(name)

    wav_mono = wav.set_channels(1)

    samples = np.array(wav_mono.get_array_of_samples())
    sample_rate = wav.frame_rate

    return sample_rate, samples, samples.shape[0] / sample_rate


def write_wav(samples, sample_rate, name):
    """
    Write audio samples to a WAV file.

    Args:
        samples (np.ndarray): An array of audio samples to be written to the file.
        sample_rate (int): The sample rate of the audio in Hz.
        name (str): The file name or path for the output WAV file.
    """
    io.wavfile.write(name, sample_rate, samples)


def plot_vowels(samples, sample_rate, detected_vowels, frame_size, vowel_colors):
    """
    Plot the waveform of audio samples and shade the regions corresponding to different vowels.

    Args:
        samples (np.ndarray): The audio samples to be plotted.
        sample_rate (int): The sample rate of the audio in Hz.
        detected_vowels (List[str]): A list of the detected vowels corresponding to each frame.
        frame_size (int): The size of each frame in samples.
        vowel_colors (dict): A dictionary mapping vowels to colors.
    """
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
