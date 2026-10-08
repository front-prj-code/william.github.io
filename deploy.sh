#!/usr/bin/env bash
#
# One-shot deploy helper.
#
# Run this yourself - it pushes to GitHub. The remote is
#   git@github.com:front-prj-code/william.github.io.git
# and the published URL will be
#   https://front-prj-code.github.io/william.github.io/
#
set -euo pipefail

REMOTE_URL="git@github.com:front-prj-code/william.github.io.git"
REPO_PATH="front-prj-code/william.github.io"
PAGES_URL="https://front-prj-code.github.io/william.github.io/"

cd "$(dirname "$0")"

echo "==> Checking working tree"
if [ -n "$(git status --porcelain)" ]; then
  echo "    Uncommitted changes present:"
  git status --short
  echo
  echo "    Commit them first, then re-run this script."
  exit 1
fi
echo "    clean"

echo "==> Checking remote"
if ! git remote get-url origin >/dev/null 2>&1; then
  git remote add origin "$REMOTE_URL"
  echo "    added origin -> $REMOTE_URL"
fi

echo "==> Checking that $REPO_PATH exists on GitHub"
if curl -sf -o /dev/null "https://api.github.com/repos/$REPO_PATH"; then
  echo "    exists"
else
  echo "    NOT created yet."
  echo
  echo "    Create it here first (leave it completely empty - no README,"
  echo "    no .gitignore, no license):"
  echo
  echo "      https://github.com/organizations/front-prj-code/repositories/new?name=william.github.io"
  echo
  echo "    Then re-run this script."
  exit 1
fi

echo "==> Pushing"
git push -u origin main

echo
echo "Pushed. Remaining one-time setup, in the repository:"
echo
echo "  1. Settings -> Pages -> Build and deployment"
echo "     Source: GitHub Actions"
echo
echo "  2. Actions tab -> 'Deploy to GitHub Pages' should already be running."
echo "     First run takes a couple of minutes."
echo
echo "  3. Site will be live at:"
echo "     $PAGES_URL"
echo
