import numpy as np
import librosa

def SignalToFrequencies(signal, sr=16000):
	f = np.fft.fftfreq(len(signal), 1.0 / sr)
	return f[1:]

def Amplitude(signal):
	amp = np.abs(np.fft.fft(signal))
	return amp[1:]

def Energy(signal):
	return [ x**2 for x in signal ]

# Return the short term energy of a signal
def ShortTermEnergy(s):
	return sum([ x**2 for x in s ]) / len(s)

def SpectralCentroids(s):
	return librosa.feature.spectral_centroid(s)
