#!/usr/bin/env bash
set -euo pipefail

# 1) Figure out where this script lives (your code root)
CODE_DIR="$(cd "$(dirname "$0")" && pwd)"

# 2) Make sure we have a staging parent
STAGING_PARENT="$CODE_DIR/staging"
mkdir -p "$STAGING_PARENT"

# 3) Build a unique name: YYMMDDhhmmss–salt–gitHash
now="$(date '+%y%m%d%H%M%S')"
# Generate a 6-character lowercase alphanumeric salt, forcing C locale to avoid illegal byte sequences
salt="$(openssl rand -hex 3)"
# if you're not in a git repo this will just say "nogit"
echo "here"
commitid="$(git -C "$CODE_DIR" rev-parse --short HEAD 2>/dev/null || echo nogit)"


# 4) Final staging path
STAGEDIR="$STAGING_PARENT/${now}-${salt}-${commitid}-code"
mkdir -p "$STAGEDIR"

# 5) Copy your entire code tree
echo "▶️  Staging $CODE_DIR → $STAGEDIR"
rsync -av --exclude "/matches" --exclude "/staging" "$CODE_DIR/" "$STAGEDIR/"

echo "✅  Staging complete."

# 6) Loosen permissions (so you don’t hit any weird umask issues)
chmod 777 "$STAGEDIR"
