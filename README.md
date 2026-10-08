# Personal Portfolio Site

A single-page portfolio: About / Resume / Portfolio / Toolbox / Contact.
Static output, no framework runtime. Layout adapted from
[codewithsadee/vcard-personal-portfolio](https://github.com/codewithsadee/vcard-personal-portfolio),
rebuilt on a small Node + Liquid pipeline that suits GitHub Pages.

## Local development

```bash
npm install
npm run dev      # http://localhost:3000, rebuilds on change
npm run build    # writes _site/index.html
```

## How the site is put together

- `index.html` only lists which sections to include.
- `_layouts/default.html` is the page shell (sidebar + navbar + content).
- `_includes/sections/*.html` is one file per section.
- `_data/*.yml` holds all the content. **This is where normal edits go** — no HTML needed.

| File | Controls |
|---|---|
| `_data/profile.yml` | Name, titles, avatar, bio paragraphs, contacts, social links |
| `_data/experience.yml` | Resume → Experience timeline |
| `_data/education.yml` | Resume → Education timeline |
| `_data/strengths.yml` | Resume → Core Strengths |
| `_data/services.yml` | About page → "What i'm doing" cards |
| `_data/projects.yml` | Portfolio grid and its filter categories |
| `_data/skills.yml` | Toolbox page groups |

### Editing project filters

The filter buttons compare their own label, lowercased, against each project's
`category_slug`. So for a category named `Trading UI` the slug must be exactly
`trading ui`. If they drift, that category silently matches nothing. `All` is a
special case.

### Project images

`assets/images/projects/*.svg` are placeholder wireframes, not real work. Replace
them by pointing the `image` field at real exports. Keep roughly 16:10 and under
about 200 KB each.

## Assets, all self-hosted

Nothing loads from an external CDN, which matters if visitors are in mainland China
where Google Fonts and unpkg are unreliable.

- `assets/fonts/` — Poppins latin subsets, 300/400/500/600 (~32 KB total)
- `assets/vendor/ionicons/` — the icon runtime plus only the icon SVGs this site uses

If you add an `<ion-icon name="...">`, download that icon's SVG into
`assets/vendor/ionicons/svg/`.

## Deploying

Pushing to `main` triggers `.github/workflows/deploy.yml`, which builds the site on
Node 22 and publishes `_site` through GitHub Pages.

One-time setup in the repository: **Settings → Pages → Build and deployment →
Source: GitHub Actions**.

Note the URL depends on the repository name:

- repo `front-prj-code.github.io` → `https://front-prj-code.github.io/`
- repo `william.github.io` → `https://front-prj-code.github.io/william.github.io/`

All asset paths are relative, so both work without changes.

## Before publishing

- Replace the placeholder project images.
- Check that the birthday shown in the sidebar is what you want public.
