# input_output.py


import scipy.io as io
import numpy as np
from pydub import AudioSegment


def read_wav(name: str):
    mysound = AudioSegment.from_wav(name)

    mysound_mono = mysound.set_channels(1)

    samples = np.array(mysound_mono.get_array_of_samples())
    sample_rate = mysound.frame_rate

    return sample_rate, samples, samples.shape[0] / sample_rate


def write_wav(samples, sample_rate, name):
    io.wavfile.write(name + '.wav', sample_rate, samples)
