
import time
import numpy as np
from scipy.signal import lfilter
from scipy.io import wavfile
from pydub import AudioSegment
import sounddevice as sd  # Replace with sounddevice

# High-pass FIR filter design function
def highpass_FIR(n_taps, normalized_cutoff):
    n = np.arange(0, n_taps)
    center = (n_taps - 1) / 2
    center = int(center) # Convert center to integer index
    # Create the ideal low-pass filter using sinc
    h_lowpass = np.sinc(2 * normalized_cutoff * (n - center))
    # Make it a high-pass filter by subtracting the low-pass response from delta function
    h_highpass = -h_lowpass
    # Correct the DC component to have a high-pass response
    h_highpass[center] += 1
    # Normalize the filter coefficients
    h_highpass = h_highpass / np.sum(h_highpass)  
    return h_highpass

# FIR filter subfunctions
def lowpass_FIR(n_taps, normalized_cutoff):
    n = np.arange(0, n_taps)
    center = (n_taps - 1) / 2
    h = np.sinc(2 * normalized_cutoff * (n - center))
    return h

def hamming_window(n_taps):
    n = np.arange(0, n_taps)
    return 0.54 - 0.46 * np.cos(2 * np.pi * n / (n_taps - 1))

def hanning_window(n_taps):
    n = np.arange(0, n_taps)
    return 0.5 - 0.5 * np.cos(2 * np.pi * n / (n_taps - 1))

def blackman_window(n_taps):
    n = np.arange(0, n_taps)
    return 0.42 - 0.5 * np.cos(2 * np.pi * n / (n_taps - 1)) + \
                     0.08 * np.cos(4 * np.pi * n / (n_taps - 1))

# Function to create a Kaiser window
def kaiser_window(n_taps, beta):
    return np.kaiser(n_taps, beta)
    # Convert stereo to mono by averaging the left and right channels
    mono_signal = np.mean(signal, axis=1)  # Average the left and right channels
    beta = 8.6
    # FIR filter parameters 15000 is fine
    n_taps = 101
    cutoff_freq = 10000  # Cutoff frequency in Hz, maximum half of sampling Fs 44100/2 = 22050
    normalized_cutoff = cutoff_freq / sampling_rate
   
    # Design FIR filters with different windows
    #ideal_filter = highpass_FIR(n_taps, normalized_cutoff)
    ideal_filter = lowpass_FIR(n_taps, normalized_cutoff)
    hamming_filter = ideal_filter * hamming_window(n_taps)
    hanning_filter = ideal_filter * hanning_window(n_taps)
    blackman_filter = ideal_filter * blackman_window(n_taps)
    kaiser_filter = ideal_filter * kaiser_window(n_taps, beta)
   
    # Apply filters to the mono signal
    filtered_origin_signal = apply_fir_filter(mono_signal, ideal_filter)
    filtered_mono_hamming = apply_fir_filter(mono_signal, hamming_filter)
    filtered_mono_hanning = apply_fir_filter(mono_signal, hanning_filter)
    filtered_mono_blackman = apply_fir_filter(mono_signal, blackman_filter)
    filtered_mono_kaiser = apply_fir_filter(mono_signal, kaiser_filter)  
    # Playback options
    print("Playing Original Mono Signal...")
    play_audio_mono_sounddevice(mono_signal, sampling_rate, 17)
   
    # 3-second break between each
    time.sleep(1)
   
    print("Playing ideal filter Mono Signal...")
    play_audio_mono_sounddevice(filtered_origin_signal, sampling_rate, 17)
   
    # 3-second break between each
    time.sleep(1)
    print("Playing Signal Filtered with Hamming Window...")
    play_audio_mono_sounddevice(filtered_mono_hamming, sampling_rate, 17)
   
    # 3-second break between each
    time.sleep(1)
   
    print("Playing Signal Filtered with Hanning Window...")
    play_audio_mono_sounddevice(filtered_mono_hanning, sampling_rate, 17)
   
    # 3-second break between each
    time.sleep(1)
   
    print("Playing Signal Filtered with Blackman Window...")
    play_audio_mono_sounddevice(filtered_mono_blackman, sampling_rate, 17)
   
    # 3-second break between each
    time.sleep(1)
   
    print("Playing Signal Filtered with Kaiser Window...")
    play_audio_mono_sounddevice(filtered_mono_kaiser, sampling_rate, 17)
   
# Run the progra
if __name__ == "__main__":
    mp3_file = "/home/pi/Downloads/DawnXYZ.mp3"  # Replace with your MP3 file path
    main(mp3_file)
