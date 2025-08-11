# Plumber Voice Assistant

A React-based video conferencing application using LiveKit.

## Setup and Running

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Create virtual environment:**

   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install LiveKit:**

   **macOS:**
   ```bash
   brew update && brew install livekit
   ```

   **Linux:**
   ```bash
   curl -sSL https://get.livekit.io | bash
   ```

   **Windows:**
   ```bash
   # Download the latest release from GitHub
   # Visit: https://github.com/livekit/livekit/releases/latest
   # Download & Install
   # Add the directory to your PATH or run from the download location
   ```

5. **Run LiveKit Server:**
   ```bash
   livekit-server --dev
   ```

6. **Environment variables:**
   Copy `.env.example` file into `.env` file and update `OPENAI_API_KEY` with your own API key.

7. **Run Agent:**

   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   python agent.py dev
   ```

   **Windows:**
   ```bash
   venv\Scripts\activate
   python agent.py dev
   ```

8. **Start the development server:**
   ```bash
   npm run dev:all
   ```

9. **Open your browser:**
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
