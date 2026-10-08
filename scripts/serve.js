const http = require('http');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const PORT = 3000;
const root = path.resolve(__dirname, '..');
const siteDir = path.join(root, '_site');

// Initial build
console.log('Building site...');
execSync('node scripts/build.js', { cwd: root, stdio: 'inherit' });

// MIME types
const mimeTypes = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.webp': 'image/webp',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
};

const server = http.createServer((req, res) => {
  let filePath = path.join(siteDir, req.url === '/' ? 'index.html' : req.url);

  // Fallback to root assets if not in _site
  if (!fs.existsSync(filePath)) {
    filePath = path.join(root, req.url);
  }

  if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
    res.writeHead(404);
    res.end('Not Found');
    return;
  }

  const ext = path.extname(filePath).toLowerCase();
  const mime = mimeTypes[ext] || 'application/octet-stream';
  res.writeHead(200, { 'Content-Type': mime });
  fs.createReadStream(filePath).pipe(res);
});

server.listen(PORT, () => {
  console.log(`Dev server running at http://localhost:${PORT}`);
  console.log('Watching for changes...');
});

// Watch and rebuild
const watchDirs = ['_includes', '_data', '_layouts'].map(d => path.join(root, d));
const watchFiles = [path.join(root, 'index.html')];

for (const dir of watchDirs) {
  if (fs.existsSync(dir)) {
    fs.watch(dir, { recursive: true }, debounce(() => rebuild(), 300));
  }
}
for (const file of watchFiles) {
  if (fs.existsSync(file)) {
    fs.watch(file, debounce(() => rebuild(), 300));
  }
}

function rebuild() {
  console.log('\nFile changed, rebuilding...');
  try {
    execSync('node scripts/build.js', { cwd: root, stdio: 'inherit' });
    console.log('Rebuild complete. Refresh your browser.');
  } catch (e) {
    console.error('Build error:', e.message);
  }
}

function debounce(fn, ms) {
  let timer;
  return () => { clearTimeout(timer); timer = setTimeout(fn, ms); };
}
