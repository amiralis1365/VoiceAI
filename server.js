const express = require('express');
const cors = require('cors');
const { AccessToken } = require('livekit-server-sdk');
const { v4: uuidv4 } = require('uuid');

const app = express();
const port = 3001;

// Enable CORS for Vite dev server
app.use(cors());

const createToken = async () => {
  // If this room doesn't exist, it'll be automatically created when the first
  // participant joins
  const roomName = `quickstart-room-${uuidv4()}`;
  // Identifier to be used for participant.
  // It's available as LocalParticipant.identity with livekit-client SDK
  const participantName = 'quickstart-username';

  const at = new AccessToken("devkey", "secret", {
    identity: participantName,
    // Token to expire after 24 hours for development
    ttl: '24h',
  });
  at.addGrant({ roomJoin: true, room: roomName });

  return await at.toJwt();
};

app.get('/getToken', async (req, res) => {
    res.send(await createToken());
});

app.listen(port, () => {
    console.log(`Token server running at http://localhost:${port}`);
    console.log('This server only handles LiveKit token generation');
});
