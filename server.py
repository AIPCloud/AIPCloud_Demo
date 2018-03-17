#!/usr/bin/env python3

import threading
import tensorflow as tf
from keras import backend as K

from sentence_intent.server import serve as serve_sentence_intent
from sentence_sentiment.server import serve as serve_sentence_sentiment
from speaker_change_detection.server import serve as serve_speaker_change_detection
from speaker_emotion.server import serve as serve_speaker_emotion
from speech_to_text.server import serve as serve_speech_to_text

if __name__ == '__main__':

    t1 = threading.Thread(target=serve_sentence_intent)
    t2 = threading.Thread(target=serve_sentence_sentiment)
    t3 = threading.Thread(target=serve_speaker_change_detection)
    t4 = threading.Thread(target=serve_speaker_emotion)
    t5 = threading.Thread(target=serve_speech_to_text)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
