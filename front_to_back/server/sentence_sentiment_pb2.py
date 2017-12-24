# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sentence_sentiment.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='sentence_sentiment.proto',
  package='sentence_sentiment',
  syntax='proto3',
  serialized_pb=_b('\n\x18sentence_sentiment.proto\x12\x12sentence_sentiment\"\x1b\n\x07Request\x12\x10\n\x08sentence\x18\x01 \x01(\t\"G\n\tSentiment\x12\x12\n\npositivity\x18\x01 \x01(\x02\x12\x12\n\nneutrality\x18\x02 \x01(\x02\x12\x12\n\nnegativity\x18\x03 \x01(\x02\"O\n\x08Response\x12\x30\n\tsentiment\x18\x01 \x01(\x0b\x32\x1d.sentence_sentiment.Sentiment\x12\x11\n\texec_time\x18\x02 \x01(\x02\x32[\n\x11SentenceSentiment\x12\x46\n\x07\x41nalyze\x12\x1b.sentence_sentiment.Request\x1a\x1c.sentence_sentiment.Response\"\x00\x62\x06proto3')
)




_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='sentence_sentiment.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sentence', full_name='sentence_sentiment.Request.sentence', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=48,
  serialized_end=75,
)


_SENTIMENT = _descriptor.Descriptor(
  name='Sentiment',
  full_name='sentence_sentiment.Sentiment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='positivity', full_name='sentence_sentiment.Sentiment.positivity', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='neutrality', full_name='sentence_sentiment.Sentiment.neutrality', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='negativity', full_name='sentence_sentiment.Sentiment.negativity', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=77,
  serialized_end=148,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='sentence_sentiment.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sentiment', full_name='sentence_sentiment.Response.sentiment', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='exec_time', full_name='sentence_sentiment.Response.exec_time', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=150,
  serialized_end=229,
)

_RESPONSE.fields_by_name['sentiment'].message_type = _SENTIMENT
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Sentiment'] = _SENTIMENT
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'sentence_sentiment_pb2'
  # @@protoc_insertion_point(class_scope:sentence_sentiment.Request)
  ))
_sym_db.RegisterMessage(Request)

Sentiment = _reflection.GeneratedProtocolMessageType('Sentiment', (_message.Message,), dict(
  DESCRIPTOR = _SENTIMENT,
  __module__ = 'sentence_sentiment_pb2'
  # @@protoc_insertion_point(class_scope:sentence_sentiment.Sentiment)
  ))
_sym_db.RegisterMessage(Sentiment)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSE,
  __module__ = 'sentence_sentiment_pb2'
  # @@protoc_insertion_point(class_scope:sentence_sentiment.Response)
  ))
_sym_db.RegisterMessage(Response)



_SENTENCESENTIMENT = _descriptor.ServiceDescriptor(
  name='SentenceSentiment',
  full_name='sentence_sentiment.SentenceSentiment',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=231,
  serialized_end=322,
  methods=[
  _descriptor.MethodDescriptor(
    name='Analyze',
    full_name='sentence_sentiment.SentenceSentiment.Analyze',
    index=0,
    containing_service=None,
    input_type=_REQUEST,
    output_type=_RESPONSE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SENTENCESENTIMENT)

DESCRIPTOR.services_by_name['SentenceSentiment'] = _SENTENCESENTIMENT

# @@protoc_insertion_point(module_scope)
