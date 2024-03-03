# input.py
# This file was created using documentation found at
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html

import scipy.io
import matplotlib as plt
import numpy as np


def read_wav(name: str):
    samplerate, data = scipy.wavfile.read(name)
    length = data.shape[0]
    pass
