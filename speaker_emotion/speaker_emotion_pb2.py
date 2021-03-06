# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: speaker_emotion/speaker_emotion.proto

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
  name='speaker_emotion/speaker_emotion.proto',
  package='speaker_emotion',
  syntax='proto3',
  serialized_pb=_b('\n%speaker_emotion/speaker_emotion.proto\x12\x0fspeaker_emotion\"2\n\x07Request\x12\x12\n\x06signal\x18\x01 \x03(\x02\x42\x02\x10\x01\x12\x13\n\x0bsample_rate\x18\x02 \x01(\x05\"O\n\x07\x45motion\x12\x0f\n\x07neutral\x18\x01 \x01(\x02\x12\x11\n\tdepleased\x18\x02 \x01(\x02\x12\r\n\x05\x61ngry\x18\x03 \x01(\x02\x12\x11\n\tsurprised\x18\x04 \x01(\x02\"X\n\x08Response\x12*\n\x08\x65motions\x18\x01 \x03(\x0b\x32\x18.speaker_emotion.Emotion\x12\x11\n\texec_time\x18\x02 \x01(\x02\x12\r\n\x05\x65mpty\x18\x03 \x01(\x08\x32T\n\x0eSpeakerEmotion\x12\x42\n\x07\x41nalyze\x12\x18.speaker_emotion.Request\x1a\x19.speaker_emotion.Response\"\x00(\x01\x62\x06proto3')
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
  serialized_start=58,
  serialized_end=108,
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
      name='depleased', full_name='speaker_emotion.Emotion.depleased', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='angry', full_name='speaker_emotion.Emotion.angry', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='surprised', full_name='speaker_emotion.Emotion.surprised', index=3,
      number=4, type=2, cpp_type=6, label=1,
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
  serialized_start=110,
  serialized_end=189,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='speaker_emotion.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='emotions', full_name='speaker_emotion.Response.emotions', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
    _descriptor.FieldDescriptor(
      name='empty', full_name='speaker_emotion.Response.empty', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=191,
  serialized_end=279,
)

_RESPONSE.fields_by_name['emotions'].message_type = _EMOTION
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Emotion'] = _EMOTION
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'speaker_emotion.speaker_emotion_pb2'
  # @@protoc_insertion_point(class_scope:speaker_emotion.Request)
  ))
_sym_db.RegisterMessage(Request)

Emotion = _reflection.GeneratedProtocolMessageType('Emotion', (_message.Message,), dict(
  DESCRIPTOR = _EMOTION,
  __module__ = 'speaker_emotion.speaker_emotion_pb2'
  # @@protoc_insertion_point(class_scope:speaker_emotion.Emotion)
  ))
_sym_db.RegisterMessage(Emotion)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSE,
  __module__ = 'speaker_emotion.speaker_emotion_pb2'
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
  serialized_start=281,
  serialized_end=365,
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
