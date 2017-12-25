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

var grpc = require('grpc');
var new_demo_portal = grpc.load(PROTO_PATH).new_demo_portal;
var client = new new_demo_portal.NewDemoPortal('localhost:50050',
  grpc.credentials.createInsecure());


app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

nsp.on('connection', function(socket){
  var call = client.analyze();
  call.on('data', function(res) {
    console.log("Response arrived: ", res);
    socket.emit('analysis_response', res)
  })
  socket.on('audio_buffer', function(data){
    console.log('Socket received.');
    data.signal = Object.values(data.signal)
    call.write(data)
  })
  socket.on('disconnect', function() {
    call.end();
  })
});

http.listen(5001, function(){
  console.log('listening on *:5001');
});
