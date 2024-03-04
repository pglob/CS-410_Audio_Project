# input_output.py


import scipy.io as io


def read_wav(name: str):
    wav = io.wavfile.read(name)
    return wav


def write_wav(samples, sample_rate):
    io.wavfile.write('output.wav', sample_rate, samples)
