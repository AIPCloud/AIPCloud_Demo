// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('grpc');
var protos_new_demo_portal_pb = require('../protos/new_demo_portal_pb.js');

function serialize_new_demo_portal_Request(arg) {
  if (!(arg instanceof protos_new_demo_portal_pb.Request)) {
    throw new Error('Expected argument of type new_demo_portal.Request');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_new_demo_portal_Request(buffer_arg) {
  return protos_new_demo_portal_pb.Request.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_new_demo_portal_Response(arg) {
  if (!(arg instanceof protos_new_demo_portal_pb.Response)) {
    throw new Error('Expected argument of type new_demo_portal.Response');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_new_demo_portal_Response(buffer_arg) {
  return protos_new_demo_portal_pb.Response.deserializeBinary(new Uint8Array(buffer_arg));
}


// Prime factors service definition.
var NewDemoPortalService = exports.NewDemoPortalService = {
  // The stream keyword is specified before both the request type and response
  // type to make it as bidirectional streaming RPC method.
  //
  analyze: {
    path: '/new_demo_portal.NewDemoPortal/Analyze',
    requestStream: false,
    responseStream: false,
    requestType: protos_new_demo_portal_pb.Request,
    responseType: protos_new_demo_portal_pb.Response,
    requestSerialize: serialize_new_demo_portal_Request,
    requestDeserialize: deserialize_new_demo_portal_Request,
    responseSerialize: serialize_new_demo_portal_Response,
    responseDeserialize: deserialize_new_demo_portal_Response,
  },
};

exports.NewDemoPortalClient = grpc.makeGenericClientConstructor(NewDemoPortalService);
// We have a method called `PrimeFactors` which takes
// parameter called `Request` and returns the message `Response`
