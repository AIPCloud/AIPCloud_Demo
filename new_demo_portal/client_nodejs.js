var PROTO_PATH = __dirname + '/../protos/new_demo_portal.proto';

var async = require('async');
var fs = require('fs');
var parseArgs = require('minimist');
var path = require('path');
var _ = require('lodash');

var load = require('audio-loader')
var grpc = require('grpc');
var new_demo_portal = grpc.load(PROTO_PATH).new_demo_portal;
var client = new new_demo_portal.NewDemoPortal('localhost:50050',
  grpc.credentials.createInsecure());

/**
 * Run the routeChat demo. Send some chat messages, and print any chat messages
 * that are sent from the server.
 * @param {function} callback Called when the demo is complete
 */

function runAnalyze(callback) {
  var call = client.analyze();
  call.on('data', function(res) {
    console.log("Response arrived: ", res);
  })
  call.on('end', callback);
  load("./sample_1.wav")
  .then(function(buffer){
    var sample = buffer.getChannelData(0);
    var i = 0;
    var length = sample.length;
    var chunkSize = 44100;
    while(i < length){
      var chunk = [];
      for (var j = i; j < i + chunkSize; j++) {
        if(j < length){
          chunk.push(sample[j])
        }
      }
      i += chunkSize
      var req = {
        signal: chunk,
        sample_rate: 44100
      }
      call.write(req)
    }
    call.end();
  })
}

/**
 * Run all of the demos in order
 */
function main() {
  async.series([
    runAnalyze
  ]);
}

if (require.main === module) {
  main();
}

exports.runAnalyze = runAnalyze;
