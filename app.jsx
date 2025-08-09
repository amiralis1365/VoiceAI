import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import {
  LiveKitRoom,
  VideoConference,
  ControlBar,
  useTracks,
  useRoomContext,
} from '@livekit/components-react';
import '@livekit/components-styles';

function App() {
  const [token, setToken] = useState('');
  const [isConnecting, setIsConnecting] = useState(false);

  useEffect(() => {
    // Fetch token from the backend
    fetch('http://localhost:3001/getToken')
      .then(response => response.text())
      .then(token => {
        setToken(token);
      })
      .catch(error => {
        console.error('Error fetching token:', error);
      });
  }, []);

  if (!token) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <LiveKitRoom
      token={token}
      serverUrl="ws://localhost:7880"
      connect={true}
      onConnected={() => {
        console.log('Connected to LiveKit');
        setIsConnecting(false);
      }}
      onDisconnected={() => {
        console.log('Disconnected from LiveKit');
      }}
    >
      <VideoConference />
      <ControlBar />
    </LiveKitRoom>
  );
}

// Initialize the app
const root = createRoot(document.getElementById('root'));
root.render(<App />);