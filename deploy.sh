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

echo "==> Checking that $REPO_PATH is reachable"
# Note: the public REST API returns 404 for private repositories, so it cannot be
# used to test existence. ls-remote goes over SSH with your own credentials and
# works for both public and private repos.
if GIT_SSH_COMMAND="ssh -o ConnectTimeout=15" git ls-remote origin >/dev/null 2>&1; then
  echo "    reachable"
else
  echo "    NOT reachable."
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
echo "  1. GitHub Pages does not work for private repositories on a free plan."
echo "     If the repo is private, either make it public"
echo "     (Settings -> General -> Danger Zone -> Change visibility) or use a"
echo "     paid plan. A portfolio site is normally public anyway."
echo
echo "  2. Settings -> Pages -> Build and deployment"
echo "     Source: GitHub Actions"
echo
echo "  3. Actions tab -> 'Deploy to GitHub Pages'."
echo "     If it already ran and failed, use 'Re-run all jobs'."
echo "     First successful run takes a couple of minutes."
echo
echo "  4. Site will be live at:"
echo "     $PAGES_URL"
echo
