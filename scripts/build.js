const fs = require('fs');
const path = require('path');
const { Liquid } = require('liquidjs');
const yaml = require('js-yaml');

const root = path.resolve(__dirname, '..');
const engine = new Liquid({
  root: [root, path.join(root, '_includes'), path.join(root, '_layouts')],
  extname: '.html',
  dynamicPartials: false,
  strictFilters: false,
  strictVariables: false,
});

// Load _data/*.yml into site.data
const dataDir = path.join(root, '_data');
const siteData = {};
if (fs.existsSync(dataDir)) {
  for (const file of fs.readdirSync(dataDir)) {
    if (file.endsWith('.yml') || file.endsWith('.yaml')) {
      const key = path.basename(file, path.extname(file));
      siteData[key] = yaml.load(fs.readFileSync(path.join(dataDir, file), 'utf8'));
    }
  }
}

// Load _config.yml
let config = {};
const configPath = path.join(root, '_config.yml');
if (fs.existsSync(configPath)) {
  config = yaml.load(fs.readFileSync(configPath, 'utf8')) || {};
}

const site = { ...config, data: siteData };

// Read index.html
const indexPath = path.join(root, 'index.html');
let indexContent = fs.readFileSync(indexPath, 'utf8');

// Extract front matter
let frontMatter = {};
const fmMatch = indexContent.match(/^---\r?\n([\s\S]*?)\r?\n---/);
if (fmMatch) {
  frontMatter = yaml.load(fmMatch[1]) || {};
  indexContent = indexContent.slice(fmMatch[0].length);
}

const page = { ...frontMatter };

// Render content
async function build() {
  let rendered = await engine.parseAndRender(indexContent, { site, page });

  // Apply layout if specified
  if (frontMatter.layout) {
    const layoutPath = path.join(root, '_layouts', frontMatter.layout + '.html');
    if (fs.existsSync(layoutPath)) {
      let layoutContent = fs.readFileSync(layoutPath, 'utf8');
      // Strip layout front matter
      const lfm = layoutContent.match(/^---\r?\n([\s\S]*?)\r?\n---/);
      if (lfm) layoutContent = layoutContent.slice(lfm[0].length);
      rendered = await engine.parseAndRender(layoutContent, { site, page, content: rendered });
    }
  }

  // Write output
  const outDir = path.join(root, '_site');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  // Copy assets
  const assetsSrc = path.join(root, 'assets');
  const assetsDst = path.join(outDir, 'assets');
  copyRecursive(assetsSrc, assetsDst);

  fs.writeFileSync(path.join(outDir, 'index.html'), rendered, 'utf8');
  console.log('Build complete -> _site/index.html generated.');
}

function copyRecursive(src, dst) {
  if (!fs.existsSync(src)) return;
  if (!fs.existsSync(dst)) fs.mkdirSync(dst, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const dstPath = path.join(dst, entry.name);
    if (entry.isDirectory()) {
      copyRecursive(srcPath, dstPath);
    } else {
      fs.copyFileSync(srcPath, dstPath);
    }
  }
}

build().catch(err => { console.error(err); process.exit(1); });
