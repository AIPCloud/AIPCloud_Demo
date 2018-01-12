from sentence_intent.server import serve as serve_sentence_intent
from sentence_sentiment.server import serve as serve_sentence_sentiment
from speaker_change_detection.server import serve as serve_speaker_change_detection
from speaker_emotion.server import serve as serve_speaker_emotion
from speech_to_text.server import serve as serve_speech_to_text

if __name__ == '__main__':
    serve_sentence_intent()
    serve_sentence_sentiment
    serve_speaker_change_detection()
    serve_speaker_emotion
    serve_speech_to_text
