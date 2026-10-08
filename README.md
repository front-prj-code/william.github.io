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
| `_data/case-studies.yml` | One entry per project: the detail page that a card links to |
| `_data/skills.yml` | Toolbox page groups |

### How the pages fit together

`index.html` is a single page with five sections that toggle in place. The
portfolio cards open a modal, and the modal's **Read case study** button
navigates to `work/<slug>.html` — a real second page per project, built from
`_layouts/case.html` plus the matching entry in `_data/case-studies.yml`.

Because those pages sit one level down, every asset reference goes through
`{{ page.base }}`: `.` on the index, `..` on the case pages. If you add a
template and hard-code `./assets/...`, it will work on the index and break on
every case study page.

Section toggling also supports URL hashes, which is how a case study page links
back to the right section (`../index.html#portfolio`). Adding a section means
adding a nav button, a `data-page` article, and nothing else.

### Adding a project

Three things have to agree, and the build fails loudly if they do not:

1. An entry in `_data/projects.yml`, with a `slug` matching the image filename.
2. A matching entry in `_data/case-studies.yml` with the same `slug`.
3. Artwork at `assets/images/projects/<slug>.svg`.

`scripts/build.js` errors if a project has no case study (its card would 404) or
a case study has no project (nothing would link to it).

### Project images

`assets/images/projects/*.svg` are 15 generated placeholder mockups, not real
work. Replace them by pointing each `image` field at a real export. Keep roughly
16:9 — the card is `aspect-ratio: 16/9` with `object-fit: cover`, so anything
taller gets cropped — and under about 200 KB each.

To regenerate or add placeholders, `scripts/generate-placeholders.py` draws them
(it validates its own XML output and fails the run rather than emitting a file a
browser will silently refuse).

### Editing project filters

The filter buttons compare their own label, lowercased, against each project's
`category_slug`. So for a category named `Trading UI` the slug must be exactly
`trading ui`. If they drift, that category silently matches nothing. `All` is a
special case, and categories containing `&` keep the `&` in the slug
(`Wallet & Assets` → `wallet & assets`).

Current categories: Trading UI, Mobile, Wallet & Assets, Admin & Risk,
Design System, Brand & Visual, AI Products.

### Project images

`assets/images/projects/*.svg` are 15 hand-drawn placeholder wireframes, not real
work. Replace them by pointing each `image` field at a real export. Keep roughly
16:10 and under about 200 KB each.

Adding a project: drop the file in `assets/images/projects/`, add an entry to
`_data/projects.yml`, and reuse one of the existing `category` / `category_slug`
pairs if it belongs to a category that already exists.

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

The remote is already configured as `front-prj-code/william.github.io`:

```
git remote -v
# origin  git@github.com:front-prj-code/william.github.io.git
```

### First deploy

1. Create the repository (leave it **completely empty** — no README, no
   `.gitignore`, no license):

   https://github.com/organizations/front-prj-code/repositories/new?name=william.github.io

2. **Make it public.** GitHub Pages is not available for private repositories on
   a free plan — the deploy workflow fails with a permissions error. Either set
   the repository to public (**Settings → General → Danger Zone → Change
   repository visibility**), or use a paid plan. A portfolio site is normally
   public anyway.

3. Push, then confirm the repository is reachable:

   ```bash
   ./deploy.sh
   ```

   The script checks the working tree, verifies the remote over SSH, then pushes.

4. In the repository: **Settings → Pages → Build and deployment →
   Source: GitHub Actions**.

5. The **Actions** tab runs `Deploy to GitHub Pages`. If it already ran and
   failed, use **Re-run all jobs**. The first successful run takes a couple of
   minutes.

### The URL

The published address depends on the repository name:

| Repository | URL |
|---|---|
| `front-prj-code/william.github.io` | `https://front-prj-code.github.io/william.github.io/` |
| `front-prj-code/front-prj-code.github.io` | `https://front-prj-code.github.io/` |

All asset paths are relative, so either works with no code changes. If you want a
bare `william.github.io`, that requires a custom domain — a repository name alone
cannot produce it when the owner is the `front-prj-code` organisation.

Note for organisations: Pages must be allowed for the repository by an org owner,
and if the organisation uses a policy restricting GitHub Actions, the workflow may
need approval before its first run.

## Before publishing

- Replace the placeholder project images (15 of them under
  `assets/images/projects/`).
- Check that the birthday shown in the sidebar is what you want public.

