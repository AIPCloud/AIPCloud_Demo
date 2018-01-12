import React, {Component}          from 'react';
import { render }                  from 'react-dom';
import { FloatingActionButton,
        MuiThemeProvider }         from 'material-ui';
import injectTapEventPlugin        from 'react-tap-event-plugin';
import MicrophoneOn                from 'material-ui/svg-icons/av/mic';
import MicrophoneOff               from 'material-ui/svg-icons/av/stop';

import { ReactMic, saveRecording } from '../../src';
import sampleAudio                 from './sample_audio.webm';
import io from 'socket.io-client';

const socket = io("http://localhost:5001/new_demo_portal")
socket.on('analysis_response', (data) => {
    console.log(data);
})
socket.emit('start_demo')

require ('./styles.scss');

injectTapEventPlugin();

export default class Demo extends Component {
  constructor(props){
    super(props);
    this.state = {
      record: false,
      blobObject: null,
      isRecording: false
    }
  }

  componentDidMount() {
  }

  startRecording= () => {
    this.setState({
      record: true,
      isRecording: true
    });
  }

  stopRecording= () => {
    this.setState({
      record: false,
      isRecording: false
    });
  }

  dataCallback=(b) => {
    socket.emit("audio_buffer", {
      sample_rate: b.sampleRate,
      signal: b.getChannelData(0)
    })
  }

  onStart=() => {
    console.log('You can tap into the onStart callback');
  }

  onStop= (blobObject) => {
    this.setState({
      blobURL : blobObject.blobURL
    });
  }

  render() {
    const { isRecording } = this.state;

    return(
      <MuiThemeProvider>
        <div>
          <h1>React-Mic</h1>
          <ReactMic
            className="oscilloscope"
            record={this.state.record}
            backgroundColor="#000000"
            visualSetting="sinewave"
            audioBitsPerSecond= {128000}
            onStop={this.onStop}
            onStart={this.onStart}
            dataCallback={this.dataCallback}
            strokeColor="#FFFFFF" />
          <div>
            <audio ref="audioSource" controls="controls" src={this.state.blobURL}></audio>
          </div>
          <br />
          <br />
          <FloatingActionButton
            className="btn"
            secondary={true}
            disabled={isRecording}
            onClick={this.startRecording}>
            <MicrophoneOn />
          </FloatingActionButton>
          <FloatingActionButton
            className="btn"
            secondary={true}
            disabled={!isRecording}
            onClick={this.stopRecording}>
            <MicrophoneOff />
          </FloatingActionButton>
        </div>
    </MuiThemeProvider>
    );
  }
}

render(<Demo/>, document.querySelector('#demo'))
