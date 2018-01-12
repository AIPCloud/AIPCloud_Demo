var grpc = require('grpc');
var new_demo_portal = grpc.load(PROTO_PATH).new_demo_portal;
var client = new new_demo_portal.NewDemoPortal('localhost:50050',
  grpc.credentials.createInsecure());
