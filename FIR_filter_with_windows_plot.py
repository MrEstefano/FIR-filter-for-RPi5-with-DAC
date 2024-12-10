import time
import numpy as np
from scipy.signal import lfilter
from scipy.io import wavfile
from pydub import AudioSegment
import sounddevice as sd  # Replace with sounddevice
import matplotlib.pyplot as plt  # For plotting

# Function to compute and plot frequency spectrum
def plot_spectrum(signal, sampling_rate, title):
    # Compute the FFT
    fft_signal = np.fft.fft(signal)
    freq = np.fft.fftfreq(len(signal), 1 / sampling_rate)
    
    # Only use the positive frequencies
    idx = np.where(freq >= 0)
    freq = freq[idx]
    magnitude = np.abs(fft_signal[idx])
    
    # Plot the spectrum
    plt.figure(figsize=(10, 6))
    plt.plot(freq, magnitude)
    plt.title(title)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid()
    plt.show()

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

# Apply the filter to the signal
def apply_fir_filter(signal, filter_coefficients):
    return lfilter(filter_coefficients, 1.0, signal)

# Load MP3 and convert to WAV
def load_mp3_to_wav(mp3_file):
    audio = AudioSegment.from_mp3(mp3_file)
    audio = audio.set_frame_rate(44100)  # Set to 8000 Hz sampling frequency
    wav_file = "temp.wav"
    audio.export(wav_file, format="wav")
    return wav_file

def play_audio_mono_sounddevice(signal, sampling_rate, duration):
    # Normalize the signal to 16-bit signed integer (-32768 to 32767)
    signal = np.int16(signal / np.max(np.abs(signal)) * 32767)

    # Ensure the signal length is sufficient for the duration
    num_samples = int(sampling_rate * duration)
    repeated_signal = np.tile(signal, num_samples // len(signal) + 1)[:num_samples]

    # Play the audio through sounddevice
    sd.play(repeated_signal, samplerate=sampling_rate)
    sd.wait()  # Wait until the audio finishes playing

# Main code
def main(mp3_file):
    
    # Load and preprocess the MP3 file
    wav_file = load_mp3_to_wav(mp3_file)
    sampling_rate, signal = wavfile.read(wav_file)
    signal = signal.astype(float)  # Convert to float for processing
     
    # Convert stereo to mono by averaging the left and right channels
    mono_signal = np.mean(signal, axis=1)  # Average the left and right channels
    beta = 8.6
    # FIR filter parameters 15000 is fine
    n_taps = 101
    cutoff_freq = 9600  # Cutoff frequency in Hz, maximum half of sampling Fs 44100/2 = 22050
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
    
    
    
    # Playback options and Plot the original and filtered signal spectra
    print("Playing Original Mono Signal...")
    play_audio_mono_sounddevice(mono_signal, sampling_rate, 17)
    plot_spectrum(mono_signal, sampling_rate, "Original Signal Spectrum")   
    # 3-second break between each
    time.sleep(1)
    
    print("Playing ideal filter Mono Signal...")
    play_audio_mono_sounddevice(filtered_origin_signal, sampling_rate, 17)
    plot_spectrum(mono_signal, sampling_rate, "Ideal filter Signal Spectrum")      
    # 3-second break between each
    time.sleep(1)
    print("Playing Signal Filtered with Hamming Window...")
    play_audio_mono_sounddevice(filtered_mono_hamming, sampling_rate, 17)
    plot_spectrum(filtered_mono_hamming, sampling_rate, "Filtered Signal Spectrum (Hamming Window)")
    # 3-second break between each
    time.sleep(1)
   
    print("Playing Signal Filtered with Hanning Window...")
    play_audio_mono_sounddevice(filtered_mono_hanning, sampling_rate, 17)
    plot_spectrum(filtered_mono_hanning, sampling_rate, "Filtered Signal Spectrum (Hanning Window)")
    # 3-second break between each
    time.sleep(1)
   
    print("Playing Signal Filtered with Blackman Window...")
    play_audio_mono_sounddevice(filtered_mono_blackman, sampling_rate, 17)
    plot_spectrum(filtered_mono_blackman, sampling_rate, "Filtered Signal Spectrum (Blackman Window)")
    # 3-second break between each
    time.sleep(1)
    
    print("Playing Signal Filtered with Kaiser Window...")
    play_audio_mono_sounddevice(filtered_mono_kaiser, sampling_rate, 17)
    plot_spectrum(filtered_mono_kaiser, sampling_rate, "Filtered Signal Spectrum (Kaiser Window)")
# Run the progra
if __name__ == "__main__":
    mp3_file = "/home/pi/Downloads/DawnXYZ.mp3"  # Replace with your MP3 file path
    main(mp3_file)

