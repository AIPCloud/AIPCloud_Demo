#!/usr/bin/env sh

source ./.env/bin/activate

python3 sentence_intent/server.py
python3 sentence_sentiment/server.py
python3 speaker_change_detection/server.py
python3 speaker_emotion/server.py
python3 speech_to_text/server.py
