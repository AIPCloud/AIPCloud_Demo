import AudioContext from './AudioContext';
import toBuffer from 'blob-to-buffer';
import createBuffer from 'audio-buffer-from';

import io from 'socket.io-client';

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

const constraints = { audio: true, video: false }; // constraints - only audio needed

navigator.getUserMedia = (navigator.getUserMedia ||
                          navigator.webkitGetUserMedia ||
                          navigator.mozGetUserMedia ||
                          navigator.msGetUserMedia);

export class MicrophoneRecorder {
  constructor(onStart, onStop, options) {
    onStartCallback= onStart;
    onStopCallback= onStop;
    mediaOptions= options;
  }

  startRecording=() => {

    startTime = Date.now();

    if(mediaRecorder) {

      if(audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume();
      }

      if(mediaRecorder && mediaRecorder.state === 'paused') {
        mediaRecorder.resume();
        return;
      }

      if(audioCtx && mediaRecorder && mediaRecorder.state === 'inactive') {
        mediaRecorder.start(10);
        const source = audioCtx.createMediaStreamSource(stream);
        source.connect(analyser);
        console.log("Has media recorder.");
        if(onStartCallback) { onStartCallback() };
      }
    } else {
      console.log("Has not media recorder.");
      if (navigator.mediaDevices) {
        console.log('getUserMedia supported.');

        navigator.mediaDevices.getUserMedia(constraints).then((str) => {
          stream = str;

          if(MediaRecorder.isTypeSupported(mediaOptions.mimeType)) {
            mediaRecorder = new MediaRecorder(str, mediaOptions);
          } else {
            mediaRecorder = new MediaRecorder(str);
          }

          if(onStartCallback) { onStartCallback() };
          const socket = io("http://192.168.0.10:5001/new_demo_portal")
          mediaRecorder.onstop = this.onStop;
          mediaRecorder.ondataavailable = (event) => {
            // Convert to AudioBuffer
            toBuffer(event.data, (err, buffer) => {
              if (err) throw err;
              let b = createBuffer(buffer, {context: audioCtx})
              socket.emit("audio_buffer", {
                sample_rate: b.sampleRate,
                signal: b.getChannelData(0)
              })

              // Stream to socket.io server

            })
            chunks.push(event.data);
          }

          audioCtx = AudioContext.getAudioContext();
          analyser = AudioContext.getAnalyser();
          console.log(analyser);

          mediaRecorder.start(1000);

          const source = audioCtx.createMediaStreamSource(stream);
          source.connect(analyser);
        });
      } else {
        alert('Your browser does not support audio recording');
      }
    }

  }

  stopRecording() {
    if(mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
      audioCtx.suspend();
    }
  }

  onStop(evt) {
    const blob = new Blob(chunks, { 'type' : mediaOptions.mimeType });
    chunks = [];

    const blobObject =  {
      blob      : blob,
      startTime : startTime,
      stopTime  : Date.now(),
      options   : mediaOptions,
      blobURL   : window.URL.createObjectURL(blob)
    }

    if(onStopCallback) { onStopCallback(blobObject) };

  }

}
