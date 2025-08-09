const { spawn } = require('child_process');
const path = require('path');

console.log('Starting development servers...\n');

// Start the token server
const tokenServer = spawn('node', ['server.js'], {
  stdio: 'inherit',
  cwd: __dirname
});

// Start Vite dev server
const viteServer = spawn('npm', ['run', 'dev'], {
  stdio: 'inherit',
  cwd: __dirname
});

// Handle process termination
process.on('SIGINT', () => {
  console.log('\nShutting down servers...');
  tokenServer.kill();
  viteServer.kill();
  process.exit();
});

// Handle server exits
tokenServer.on('close', (code) => {
  console.log(`Token server exited with code ${code}`);
  viteServer.kill();
});

viteServer.on('close', (code) => {
  console.log(`Vite server exited with code ${code}`);
  tokenServer.kill();
});
