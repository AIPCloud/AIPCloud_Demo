var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var nsp = io.of('/new_demo_portal')


var async = require('async');
var fs = require('fs');
var parseArgs = require('minimist');
var path = require('path');
var _ = require('lodash');
var caller = require('grpc-caller');
var Promise = require('bluebird');

var _SERVER_ADDRESS = 'localhost'
var _PROTO_PATH = path.resolve(__dirname, '../../protos')

var grpc = require('grpc');

var speaker_change_detection = grpc.load(_PROTO_PATH + '/speaker_change_detection/speaker_change_detection.proto').speaker_change_detection;
var SCDclient = new speaker_change_detection.SpeakerChangeDetection(_SERVER_ADDRESS + ':50053',
  grpc.credentials.createInsecure());

var S2Tclient = caller(_SERVER_ADDRESS + ':50055', _PROTO_PATH + '/speech_to_text/speech_to_text.proto', 'SpeechToText')
var SEclient = caller(_SERVER_ADDRESS + ':50054', _PROTO_PATH + '/speaker_emotion/speaker_emotion.proto', 'SpeakerEmotion')
var SSclient = caller(_SERVER_ADDRESS + ':50052', _PROTO_PATH + '/sentence_sentiment/sentence_sentiment.proto', 'SentenceSentiment')
var SIclient = caller(_SERVER_ADDRESS + ':50051', _PROTO_PATH + '/sentence_intent/sentence_intent.proto', 'SentenceIntent')

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

nsp.on('connect', function(socket){
  var index = 0;
  var Signal = []
  var sampleRate = -1
  var lastStep = 0
  var SCDcall = SCDclient.analyze();
  console.log("Client connected.");
  SCDcall.on('data', function(resSCD) {
    index += 1
    console.log("Change in speaker detected.")
    console.log(resSCD.change.time)
    // Client definition
    a = S2Tclient.recognition()
    S2Tcall = a.call
    S2Tres = a.res
    a = SEclient.analyze()
    SEcall = a.call
    SEres = a.res

    console.log("Starting the chunk streaming.");
    var newStep = Math.round(resSCD.change.time * sampleRate)
    var signal = Signal.slice(lastStep, newStep)

    while (signal.length > 0) {
      chunkSize = 1024
      if (signal.length < chunkSize) {
        chunkSize = signal.length
      }
      chunk = signal.splice(0, chunkSize)
      data = {
        signal: chunk,
        sample_rate: sampleRate,
      }
      SEcall.write({
        signal: chunk,
        sample_rate: sampleRate,
      })
      S2Tcall.write({
        signal: chunk,
        sample_rate: sampleRate,
        language_code: 'fr-FR'
      })
    }
    SEcall.end()
    S2Tcall.end()
    lastStep = newStep

    //
    //
    // S2Tres.then(function(res){
    //   console.log("S2T: ", res);
    // })
    // SEres.then(function(res){
    //   console.log("SE: ", res);
    // })

    Promise.all([S2Tres, SEres]).then(function(results){
      S2T_res = results[0]
      SE_res = results[1]

      SSpromises = []
      SIpromises = []

      for (var speech in S2T_res.speeches) {
        var sentence = speech.transcript
        SSpromises.push(SSclient.analyze({sentence: sentence}))
        SIpromises.push(SIclient.analyze({sentence: sentence}))
      }

      SSpromise = Promise.all(SSpromises)
      SIpromise = Promise.all(SIpromises)

      Promise.all([SSpromise, SIpromise]).then(function(values){
        for (var j = 0; j < values[0].length; j++) {
          S2T_res.speeches[j].sentiment = values[0][j].sentiment
          S2T_res.speeches[j].intent = values[1][j].intent
        }
        var response_data = {
          emotions: SE_res.emotions,
          speeches: S2T_res.speeches
        }
        console.log(response_data);
      })

    })
  })
  socket.on('audio_buffer', function(data){
    // console.log('Socket received.');
    data.signal = Object.keys(data.signal).map((e, key) => {
      return data.signal[e]
    })
    Signal = Signal.concat(data.signal)
    sampleRate = data.sample_rate
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
