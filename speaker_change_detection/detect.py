# Property of Junior Data Consulting - Copyright (c) 2017
# Do not distribute the source code
# Author : Maxime Jumelle

import os
import sys
import math
import pandas as pd
import numpy as np
from keras.models import model_from_json, Model
from keras import backend as K
import tensorflow as tf
import configparser
import soundfile as sf
import librosa
# import librosa.display
from sklearn import mixture
#import matplotlib.mlab as mlab
from scipy.stats import norm
from .signal_proc import ShortTermEnergy, SpectralCentroids

cfg = configparser.ConfigParser()
cfg.read(os.path.join(os.path.dirname(__file__), './config.cfg'))

# We load all the parameters
PARAM_HAMMING_LENGTH = int(cfg.get("FEATURE", "win_length"))
PARAM_HAMMING_HOP = int(cfg.get("FEATURE", "win_hop"))
PARAM_CONCATENATION_COUNT = int(cfg.get("FEATURE", "concatenation_count"))
PARAM_CONCATENATION_HOP = int(cfg.get("FEATURE", "concatenation_hop"))
NB_SPEAKERS = int(cfg.get("TRAINING", "nb_speakers"))
NB_FRAMES = int(cfg.get("PREDICTION", "nb_frames"))
FRAME_LENGTH = int(cfg.get("PREDICTION", "frame_length"))
FRAME_HOP = int(cfg.get("PREDICTION", "frame_hop"))
DETECTION_THRESHOLD = float(cfg.get("PREDICTION", "detection_threshold"))
CHANGES_EPSILON = float(cfg.get("PREDICTION", "changes_epsilon"))

# The p-norm used to calculates distance. Default is Euclidian norm
def pNorm(x, p=2):
	if p <= 0:
		assert("The parameter p must be greater than 0.")
	return sum([ v**p for v in x ])**(1 / p)

# Returns the mean of a matrix (mean for each vector)
def mean(mat):
	return np.asarray([ sum(v) / len(v) for v in mat ])

# A simple riemann sum to computes numerical integrals
# IT IS UGLY : Replace it with a powerfull method without much more time wasting
def riemannSum(f, I):
	res = 0
	h = I[1] - I[0]
	for i in range(len(I)):
		res += f(I[i])
	res *= h
	return res

# Detect the speaker changes in a signal
# framing : If set to True, the analysis is done with framing
# If set to False, the analysis will be done on the entire input signal without frames
# Returns : Array of time when speaker changes
def detect(signal, samplerate, framing=True, frame_length=FRAME_LENGTH, frame_hop=FRAME_HOP, model=False):
	changes = [] # Will contain all the changes
	#Resample
	# signal = librosa.resample(np.asarray(signal), samplerate, 22050)
	# samplerate = 22050
	# We NEED to perform analysis on mono signals
	signal = librosa.to_mono(np.transpose(signal))

	E = ShortTermEnergy(signal)
	C = SpectralCentroids(signal)

	# print(samplerate)
	# print(np.asarray(C)[0].shape)
	# print(len(signal))
	silenceWindow = int(len(signal) / len(C[0]))
	# print(silenceWindow)

	# cursor = 0
	# Cindex = 0
	# newSignal = []
	# while cursor < len(signal) - silenceWindow:
	# 	if C[0][Cindex] > 800:
	# 		newSignal = np.hstack((newSignal, signal[cursor:(cursor + silenceWindow)]))
	# 	cursor += silenceWindow
	# 	Cindex += 1
	#signal = newSignal
	#librosa.output.write_wav('test/trimmed.wav', newSignal, samplerate)
	#sys.exit()

	#signal, _ = librosa.effects.trim(signal, top_db=6)
	#librosa.output.write_wav("test/trimmed.wav", signal, samplerate)
	# Scaling to maximum amplitude
	maxAmp = max(signal)
	signal /= maxAmp

	# X will be fed to the neural network
	X = []
	# Duration of the signal
	duration = int(np.ceil(len(signal) / samplerate * 1000))
	cursor = 0
	# Contains the 39 MFCC coefficients (MFCC, delta, delta_2) (13 * 3)
	MFCC = []
	while cursor < duration - PARAM_HAMMING_LENGTH:
		# Bounds of hamming window
		a = int(cursor * samplerate / 1000)
		b = int((cursor + PARAM_HAMMING_LENGTH) * samplerate / 1000)
		hammingWindow = signal[a:b]
		#S = librosa.feature.melspectrogram(hammingWindow, sr=samplerate, n_mels=128)
		#log_S = librosa.power_to_db(S, ref=np.max)
		# Extracting MFCC feature
		coefficients = librosa.feature.mfcc(y=hammingWindow, sr=samplerate, n_mfcc=13)
		# Getting delta and double delta
		deltas = np.vstack((librosa.feature.delta(coefficients), librosa.feature.delta(coefficients, order=2)))
		# Stacking the 13 length vectors
		coefficients = np.vstack((coefficients, deltas))
		coefficients = np.asarray([ sum(row) / len(row) for row in coefficients ])
		#m = sum(coefficients) / len(coefficients)
		#std = math.sqrt(sum([ (c - m)**2 for c in coefficients ]) / len(coefficients))
		#coefficients = np.asarray([ (c - m) / std for c in coefficients ])
		MFCC.append(coefficients)
		# Going to next frame
		cursor += PARAM_HAMMING_HOP

	# The MFCC concatenation processing
	cursor = 0
	while cursor < len(MFCC) - PARAM_CONCATENATION_COUNT:
		# We get the vector we want to concatenate
		concatenation = MFCC[cursor:(cursor + PARAM_CONCATENATION_COUNT)]
		# We transform them into a 1-D vector
		concatenation = np.asarray(concatenation).ravel()
		X.append(concatenation)
		cursor += PARAM_CONCATENATION_HOP

	X = np.asarray(X)

	if not model:
		# We load the neural network and weights
		json_file = open('data/model.json', 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		model = model_from_json(loaded_model_json)
		model.load_weights("data/weights.h5")

	# Classification prediction of the concatenated frames
	prediction = model.predict(X)
	# We add 1e-10 to avoid log(0)
	prediction = [ row / max(row) + np.repeat(1e-10, len(row)) for row in prediction ]
	prediction = [ np.log(row) for row in prediction ]
	# Now we start to detect if there are changes looking at distances
	cursor = 0

	def detectInFrame(frame):
		# Calculation of p-norm distances between NB_FRAMES length windows
		distances = [ pNorm(mean(d[t]) - mean(d[t-1])) + pNorm(mean(d[t+1]) - mean(d[t])) for t in range(1,len(d)-1) ]

		if len(distances) == 0:
			return
		# Normalization
		#distances /= max(distances)

		# We fit a gaussian mixture model (GMM) of 2 components with EM algorithm
		#clf = mixture.GaussianMixture(n_components=2, covariance_type='full')
		#clf.fit(np.array([ [ d ] for d in distances ]))

		# Results of the mixture model
		#weights = clf.weights_
		#means = clf.means_
		#covar = clf.covariances_

		# Normalization for our distance histogram
		#histogramWeight = 1. / float(len(distances))

		# The two components of our GMM
		#def p1(x):
		#	return mlab.normpdf(x, means[0][0], math.sqrt(covar[0][0])) * weights[0] * histogramWeight

		#def p2(x):
		#	return mlab.normpdf(x, means[1][0], math.sqrt(covar[1][0])) * weights[1] * histogramWeight

		# We product a linearization of the space
		#I = np.linspace(max(min(distances), 1e-10), max(distances), 600)

		#pdf1 = p1(I)
		#pdf2 = p2(I)
		# We detect the gaussian decision boundary on our GMM
		#x_bound = 0
		#if I[np.where(pdf1 < pdf2)] != [] and I[np.where(pdf1 > pdf2)] != []:
			#x_bound = max(I[np.where(pdf1 < pdf2)][0], I[np.where(pdf1 > pdf2)][0])

		# Returns the Kullback-Leibler (KL) divergence of the 2 components from the GMM
		#def KL(x):
			# One should take care of extreme low values since dom(log)=(0, +Inf)
		#	if p1(x) < 1e-300 or p2(x) < 1e-300:
		#		return 0
		#	return p1(x) * np.log( p1(x) / p2(x) )
		# Returns the Kullback-Leibler (KL) divergence of the 2 components from the GMM
		#def KL_res():
		#	v1 = (weights[0] * histogramWeight)**2 * covar[0][0]
		#	v2 = (weights[1] * histogramWeight)**2 * covar[1][0]
		#	return 0.5 * (v1 / v2 + (means[0][0] - means[1][0])**2 / v2 - 1 + math.log(v2 / v1))
		#print(duration  / len(prediction) / 1000)
		# We calculates the integral of the KL function
		#KL_int = riemannSum(KL, I)
		#KL_int = KL_res()
		#if KL_res() >= DETECTION_THRESHOLD:
		# print("-" * 50)
		x_bound = 13.5 # 19.56
		#if KL_res() >= 0 and max(distances) > x_bound:
		if max(distances) > x_bound:
			# We get all the detected points
			positives = [ cursor + i for i in range(len(distances)) if distances[i] > x_bound]
			#print(positives)
			positive_dist = [ el for el in distances if el > x_bound]
			# print(positive_dist)
			posWeight = [ el / max(positive_dist) for el in positive_dist ]

			#print(positives)
			detectionIndex = np.dot(posWeight, positives) / sum(posWeight)
			# We consider a precision up to 1 ms
			changeTime = round(duration * detectionIndex / len(prediction) / 1000, 3)
			#print(str(changeTime) + " - " + str(KL_int))
			#print(positives)
			changes.append(changeTime)

			#KL_array.append(KL_int)
			#KL_array_X.append(changeTime)


	if framing:
		while cursor < len(prediction) - NB_FRAMES:
			# We slice to get the prediction that are in the frame
			frame_X = prediction[cursor:int(cursor + PARAM_CONCATENATION_HOP * NB_FRAMES * frame_length / 1000)]
			# We pack them producing overlapping
			d = [ frame_X[i:(i+NB_FRAMES)] for i in range(len(frame_X) - NB_FRAMES) ]
			detectInFrame(d)
			# We go on the next frame
			cursor += int(PARAM_CONCATENATION_HOP * NB_FRAMES * frame_hop / 1000)
	else:
		detectInFrame(prediction)

	# We remove changes that at too close (difference inferior to CHANGES_EPSILON)
	if len(changes) >= 2:
		finalChanges = [ changes[0] ]
		for i in range(1,len(changes)):
			if changes[i] - changes[i-1] > CHANGES_EPSILON / 1000:
				finalChanges.append(changes[i])

		return finalChanges
	return changes

if __name__ == '__main__':
	signal, samplerate = librosa.load("sample_1.wav", sr=44100)
	detections = detect(signal, samplerate)
	print(detections)

	#import matplotlib.pyplot as plt

	#plt.figure()
	#plt.plot(KL_array_X, KL_array)
	#plt.show()
