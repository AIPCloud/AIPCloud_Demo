#!/usr/bin/env sh


python3 -m grpc_tools.protoc -I protos/ --python_out=. --grpc_python_out=. protos/sentence_intent/sentence_intent.proto

python3 -m grpc_tools.protoc -I protos/ --python_out=. --grpc_python_out=. protos/sentence_sentiment/sentence_sentiment.proto

python3 -m grpc_tools.protoc -I protos/ --python_out=. --grpc_python_out=. protos/speaker_emotion/speaker_emotion.proto

python3 -m grpc_tools.protoc -I protos/ --python_out=. --grpc_python_out=. protos/speaker_change_detection/speaker_change_detection.proto

python3 -m grpc_tools.protoc -I protos/ --python_out=. --grpc_python_out=. protos/speech_to_text/speech_to_text.proto
