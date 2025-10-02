
#!/usr/bin/env bash
set -e
REPO_NAME=${1:-nxs-master-os}
git init
git add .
git commit -m "Initial commit: NXS Master OS"
git branch -M main
echo "Create repo '$REPO_NAME' on GitHub, then:"
echo "  git remote add origin git@github.com:<your-org>/$REPO_NAME.git"
echo "  git push -u origin main"
