# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: speaker_emotion.proto

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
  name='speaker_emotion.proto',
  package='speaker_emotion',
  syntax='proto3',
  serialized_pb=_b('\n\x15speaker_emotion.proto\x12\x0fspeaker_emotion\"2\n\x07Request\x12\x12\n\x06signal\x18\x01 \x03(\x02\x42\x02\x10\x01\x12\x13\n\x0bsample_rate\x18\x02 \x01(\x05\"\x87\x01\n\x07\x45motion\x12\x0f\n\x07neutral\x18\x01 \x01(\x02\x12\x0c\n\x04\x63\x61lm\x18\x02 \x01(\x02\x12\r\n\x05happy\x18\x03 \x01(\x02\x12\x0b\n\x03sad\x18\x04 \x01(\x02\x12\r\n\x05\x61ngry\x18\x05 \x01(\x02\x12\x0f\n\x07\x66\x65\x61rful\x18\x06 \x01(\x02\x12\x10\n\x08surprise\x18\x07 \x01(\x02\x12\x0f\n\x07\x64isgust\x18\x08 \x01(\x02\"H\n\x08Response\x12)\n\x07\x65motion\x18\x01 \x01(\x0b\x32\x18.speaker_emotion.Emotion\x12\x11\n\texec_time\x18\x02 \x01(\x02\x32V\n\x0eSpeakerEmotion\x12\x44\n\x07\x41nalyze\x12\x18.speaker_emotion.Request\x1a\x19.speaker_emotion.Response\"\x00(\x01\x30\x01\x62\x06proto3')
)




_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='speaker_emotion.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='signal', full_name='speaker_emotion.Request.signal', index=0,
      number=1, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001')), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sample_rate', full_name='speaker_emotion.Request.sample_rate', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=42,
  serialized_end=92,
)


_EMOTION = _descriptor.Descriptor(
  name='Emotion',
  full_name='speaker_emotion.Emotion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='neutral', full_name='speaker_emotion.Emotion.neutral', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='calm', full_name='speaker_emotion.Emotion.calm', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='happy', full_name='speaker_emotion.Emotion.happy', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sad', full_name='speaker_emotion.Emotion.sad', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='angry', full_name='speaker_emotion.Emotion.angry', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fearful', full_name='speaker_emotion.Emotion.fearful', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='surprise', full_name='speaker_emotion.Emotion.surprise', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='disgust', full_name='speaker_emotion.Emotion.disgust', index=7,
      number=8, type=2, cpp_type=6, label=1,
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
  serialized_start=95,
  serialized_end=230,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='speaker_emotion.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='emotion', full_name='speaker_emotion.Response.emotion', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='exec_time', full_name='speaker_emotion.Response.exec_time', index=1,
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
  serialized_start=232,
  serialized_end=304,
)

_RESPONSE.fields_by_name['emotion'].message_type = _EMOTION
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Emotion'] = _EMOTION
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'speaker_emotion_pb2'
  # @@protoc_insertion_point(class_scope:speaker_emotion.Request)
  ))
_sym_db.RegisterMessage(Request)

Emotion = _reflection.GeneratedProtocolMessageType('Emotion', (_message.Message,), dict(
  DESCRIPTOR = _EMOTION,
  __module__ = 'speaker_emotion_pb2'
  # @@protoc_insertion_point(class_scope:speaker_emotion.Emotion)
  ))
_sym_db.RegisterMessage(Emotion)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSE,
  __module__ = 'speaker_emotion_pb2'
  # @@protoc_insertion_point(class_scope:speaker_emotion.Response)
  ))
_sym_db.RegisterMessage(Response)


_REQUEST.fields_by_name['signal'].has_options = True
_REQUEST.fields_by_name['signal']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))

_SPEAKEREMOTION = _descriptor.ServiceDescriptor(
  name='SpeakerEmotion',
  full_name='speaker_emotion.SpeakerEmotion',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=306,
  serialized_end=392,
  methods=[
  _descriptor.MethodDescriptor(
    name='Analyze',
    full_name='speaker_emotion.SpeakerEmotion.Analyze',
    index=0,
    containing_service=None,
    input_type=_REQUEST,
    output_type=_RESPONSE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SPEAKEREMOTION)

DESCRIPTOR.services_by_name['SpeakerEmotion'] = _SPEAKEREMOTION

# @@protoc_insertion_point(module_scope)
