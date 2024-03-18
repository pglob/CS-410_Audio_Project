# parameters.py

frame_size = 200

# While some F2 frequencies approach 3000, increasing bandpass_high results in degradation of results, likely due to
# higher frequency noise and artifacts.
bandpass_high = 3000
# As long as bandpass_low is around 50Hz, it will have minimal effect on most speech.
bandpass_low = 50
bandpass_order = 4

silence_tolerance = 0.1

zcr_modifier = 1  # Increasing zcr_modifier increases tolerance for determining voiced speech
e_modifier = 0.1  # Decreasing e_modifier increases tolerance for determining voiced speech

smoothing_window = 3
vowel_smoothing = 10

lpc_order = 10  # A good order varies on sample rate. For 44100 samples per second, 10 seems to work well

# Values are from page 154 of "A Practical Introduction to Phonetics"
# https://linc2018.files.wordpress.com/2018/06/a-practical-lntroduction-to-phonetics.pdf
vowel_formants = {
    'i': {'F1': 240, 'F2': 2400},  # 'heed'
    'e': {'F1': 390, 'F2': 2300},  # 'head'
    'a': {'F1': 850, 'F2': 1610},  # 'had'
    'o': {'F1': 360, 'F2': 640},   # 'hoed'
    'u': {'F1': 250, 'F2': 595},   # 'mood'
}

vowel_colors = {
    'i': 'blue',  # 'heed'
    'e': 'green',  # 'head'
    'a': 'red',  # 'had'
    'o': 'yellow',  # 'hoed'
    'u': 'purple',  # 'mood'
}
