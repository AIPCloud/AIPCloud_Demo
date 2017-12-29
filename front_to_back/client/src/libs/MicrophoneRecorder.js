import toBuffer from 'blob-to-buffer';
import AudioContext from './AudioContext';
import io from 'socket.io-client';

//////////////SOCKET///////////////
const socket = io("http://192.168.0.10:5001/new_demo_portal")
socket.on('analysis_response', (data) => {
    console.log(data);
})
socket.emit('start_demo')
//////////////SOCKET///////////////



let analyser;
let audioCtx;
let mediaRecorder;
let chunks = [];
let startTime;
let stream;
let mediaOptions;
let blobObject;
let onStartCallback;
let onStopCallback;

const constraints = {
  audio: true,
  video: false
}; // constraints - only audio needed

navigator.getUserMedia = (navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia);

export class MicrophoneRecorder {
  constructor(onStart, onStop, options) {
    onStartCallback = onStart;
    onStopCallback = onStop;
    mediaOptions = options;
  }

  startRecording = () => {

    startTime = Date.now();

    if (mediaRecorder) {

      if (audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume();
      }

      if (mediaRecorder && mediaRecorder.state === 'paused') {
        mediaRecorder.resume();
        return;
      }

      if (audioCtx && mediaRecorder && mediaRecorder.state === 'inactive') {
        mediaRecorder.start(10);
        const source = audioCtx.createMediaStreamSource(stream);
        source.connect(analyser);
        if (onStartCallback) {
          onStartCallback()
        };
      }
    } else {
      if (navigator.mediaDevices) {
        console.log('getUserMedia supported.');

        navigator.mediaDevices.getUserMedia(constraints).then((str) => {
          stream = str;

          if (MediaRecorder.isTypeSupported(mediaOptions.mimeType)) {
            mediaRecorder = new MediaRecorder(str, mediaOptions);
          } else {
            mediaRecorder = new MediaRecorder(str);
          }

          if (onStartCallback) {
            onStartCallback()
          };

          mediaRecorder.onstop = this.onStop;
          mediaRecorder.ondataavailable = (event) => {
            chunks.push(event.data);
          }

          audioCtx = AudioContext.getAudioContext();
          analyser = AudioContext.getAnalyser();

          mediaRecorder.start(10);

          const source = audioCtx.createMediaStreamSource(stream);
          source.connect(analyser);
          var processor = audioCtx.createScriptProcessor(1024, 1, 1);
          source.connect(processor);
          processor.connect(audioCtx.destination);

          // var nsp = socks.of('/new_demo_portal');

          processor.onaudioprocess = (e) => {
            let b = e.inputBuffer
            socket.emit("audio_buffer", {
              sample_rate: b.sampleRate,
              signal: b.getChannelData(0)
            })
          }
        });
      } else {
        alert('Your browser does not support audio recording');
      }
    }

  }

  stopRecording() {


    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
      audioCtx.suspend();
    }
  }

  onStop(evt) {
    socket.emit('stop_demo')

    const blob = new Blob(chunks, {'type': mediaOptions.mimeType});
    chunks = [];

    const blobObject = {
      blob: blob,
      startTime: startTime,
      stopTime: Date.now(),
      options: mediaOptions,
      blobURL: window.URL.createObjectURL(blob)
    }

    if (onStopCallback) {
      onStopCallback(blobObject)
    };

  }

}
