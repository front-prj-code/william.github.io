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

const outDir = path.join(root, '_site');

function readLayout(name) {
  const layoutPath = path.join(root, '_layouts', name + '.html');
  if (!fs.existsSync(layoutPath)) {
    throw new Error('Missing layout: _layouts/' + name + '.html');
  }
  let content = fs.readFileSync(layoutPath, 'utf8');
  // Strip layout front matter if present
  const fm = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  return fm ? content.slice(fm[0].length) : content;
}

function readPage(file) {
  const full = path.join(root, file);
  if (!fs.existsSync(full)) throw new Error('Missing page: ' + file);
  let content = fs.readFileSync(full, 'utf8');
  let frontMatter = {};
  const fm = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (fm) {
    frontMatter = yaml.load(fm[1]) || {};
    content = content.slice(fm[0].length);
  }
  return { content, frontMatter };
}

function writeOut(relPath, html) {
  const dest = path.join(outDir, relPath);
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.writeFileSync(dest, html, 'utf8');
}

async function buildIndex() {
  const { content, frontMatter } = readPage('index.html');
  // base is "." here and ".." on the case pages; every asset reference is
  // prefixed with it so relative paths keep working from any depth.
  const page = { ...frontMatter, base: '.' };

  let rendered = await engine.parseAndRender(content, { site, page });
  if (frontMatter.layout) {
    const layout = readLayout(frontMatter.layout);
    rendered = await engine.parseAndRender(layout, { site, page, content: rendered });
  }
  writeOut('index.html', rendered);
  return 1;
}

async function buildCaseStudies() {
  const studies = siteData['case-studies'] || [];
  const projects = (siteData.projects && siteData.projects.items) || [];
  const bySlug = {};
  projects.forEach((p) => { bySlug[p.slug] = p; });

  const layout = readLayout('case');
  let count = 0;

  for (let i = 0; i < studies.length; i++) {
    const work = studies[i];
    const project = bySlug[work.slug];

    if (!project) {
      // A case study without a portfolio entry would be unreachable, and a
      // portfolio entry without a case study would link to a 404. Fail loudly.
      throw new Error(
        'No project in _data/projects.yml with slug "' + work.slug + '"'
      );
    }

    const page = {
      base: '..',
      work,
      project,
      prev: studies[i - 1] || null,
      next: studies[i + 1] || null,
    };

    const html = await engine.parseAndRender(layout, { site, page });
    writeOut(path.join('work', work.slug + '.html'), html);
    count++;
  }

  // The reverse check: every project must have a case study, otherwise its
  // card links somewhere that does not exist.
  const studySlugs = new Set(studies.map((s) => s.slug));
  const orphans = projects.filter((p) => !studySlugs.has(p.slug)).map((p) => p.slug);
  if (orphans.length) {
    throw new Error(
      'These projects have no case study, so their cards would 404: ' + orphans.join(', ')
    );
  }

  return count;
}

async function build() {
  fs.mkdirSync(outDir, { recursive: true });

  copyRecursive(path.join(root, 'assets'), path.join(outDir, 'assets'));

  const pages = await buildIndex();
  const cases = await buildCaseStudies();

  // Tell GitHub Pages to serve the files as-is instead of running Jekyll.
  fs.writeFileSync(path.join(outDir, '.nojekyll'), '', 'utf8');

  console.log('Build complete -> _site/index.html + ' + cases + ' case study page(s)');
  return { pages, cases };
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
