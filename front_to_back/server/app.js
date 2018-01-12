var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var nsp = io.of('/new_demo_portal')

var PROTO_PATH = __dirname + '/../../protos/new_demo_portal.proto';

var async = require('async');
var fs = require('fs');
var parseArgs = require('minimist');
var path = require('path');
var _ = require('lodash');

var _SERVER_ADDRESS = 'localhost'
var _PROTO_PATH = path.resolve(__dirname, '../../protos')

var grpc = require('grpc');

var speaker_change_detection = grpc.load(_PROTO_PATH + '/speaker_change_detection.proto').speaker_change_detection;
var SCDclient = new speaker_change_detection.SpeakerChangeDetection(_SERVER_ADDRESS + ':50054',
  grpc.credentials.createInsecure());

var speech_to_text = grpc.load(_PROTO_PATH + '/speech_to_text.proto').speech_to_text;
var S2Tclient = new speech_to_text.SpeechToText(_SERVER_ADDRESS + ':50053',
  grpc.credentials.createInsecure());

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

nsp.on('connect', function(socket){
  var Signal = []
  var sampleRate = -1
  var lastStep = 0
  var SCDcall = SCDclient.analyze();
  console.log("Client connected.");
  SCDcall.on('data', function(res) {
    console.log("Change in speaker detected.")
    console.log(res.change.time)
    // Client definition
    var S2Tcall = S2Tclient.recognition((err, res) => {
      console.log(res)
    })

    var newStep = Math.round(res.change.time * sampleRate)
    var signal = Signal.slice(lastStep, newStep)

    while (signal.length > 0) {
      chunkSize = 44100
      if (signal.length < chunkSize) {
        chunkSize = signal.length
      }
      chunk = signal.splice(0, chunkSize)
      console.log(signal.length);
      data = {
        signal: chunk,
        sample_rate: sampleRate,
        language_code: 'fr-FR'
      }
      S2Tcall.write(data)
    }
    lastStep = newStep
  })
  socket.on('audio_buffer', function(data){
    // console.log('Socket received.');
    data.signal = Object.keys(data.signal).map((e, key) => {
      return data.signal[e]
    })
    Signal = Signal.concat(data.signal)
    SCDcall.write(data)
  })
  socket.on('disconnect', function() {
    console.log("Client disconnected.");
    SCDcall.end();
  })
});

http.listen(5001, function(){
  console.log('listening on *:5001');
});
