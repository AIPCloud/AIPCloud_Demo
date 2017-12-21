#!/usr/bin/env sh

python3 -m grpc_tools.protoc -I protos/ --python_out=./sentence_sentiment --grpc_python_out=./sentence_sentiment protos/sentence_sentiment.proto

python3 -m grpc_tools.protoc -I protos/ --python_out=./speaker_emotion --grpc_python_out=./speaker_emotion protos/speaker_emotion.proto

python3 -m grpc_tools.protoc -I protos/ --python_out=./speech_to_text --grpc_python_out=./speech_to_text protos/speech_to_text.proto
