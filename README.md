# Plumber Voice Assistant

A React-based video conferencing application using LiveKit.

## Setup and Running

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Create virtual env**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install LiveKit**
   ```bash
   brew update && brew install livekit

   ```

5. **Run LiveKit Server**
   ```bash
   livekit-server --dev
   ```

6. **Run Agent**
   ```bash
   source venv/bin/activate
   python agent.py dev     
   ```

7. **Start the development server:**
   ```bash
   npm run dev:all
   ``` 

8. **Open your browser:**
   Navigate to `http://localhost:3000`

## Files

- `app.js` - Main React component with LiveKit video conferencing functionality
- `index.html` - HTML page that loads the React app
- `server.js` - Express server to serve the application
- `package.json` - Project dependencies and scripts

## Dependencies

- React 18
- LiveKit Client and Components
- LiveKit Server
- Express (for development server)
