#!/usr/bin/env sh

python3 -m grpc_tools.protoc -I protos/ --python_out=./sentence_sentiment --grpc_python_out=./sentence_sentiment protos/sentence_sentiment.proto

python3 -m grpc_tools.protoc -I protos/ --python_out=./speaker_emotion --grpc_python_out=./speaker_emotion protos/speaker_emotion.proto

python3 -m grpc_tools.protoc -I protos/ --python_out=./speech_to_text --grpc_python_out=./speech_to_text protos/speech_to_text.proto

python3 -m grpc_tools.protoc -I protos/ --python_out=./new_demo_portal --grpc_python_out=./new_demo_portal protos/new_demo_portal.proto
grpc_tools_node_protoc --js_out=import_style=commonjs,binary:./new_demo_portal/client/demo/src --grpc_out=./new_demo_portal/client/demo/src --plugin=protoc-gen-grpc=`which grpc_tools_node_protoc_plugin` protos/new_demo_portal.proto
