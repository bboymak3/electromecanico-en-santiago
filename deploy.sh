#!/bin/bash
# deploy.sh - Deploy Electromecánico en Santiago a Cloudflare Pages
# Combina git push + wrangler deploy en un solo comando
#
# Requiere (solo la primera vez):
#   export CF_TOKEN="cfut_xxx"
#   export CF_ACCOUNT="6fc12c9a..."
#
# Uso: ./deploy.sh "mensaje del commit"

set -e

REPO_DIR="/home/z/my-project/repos/electromecanico-en-santiago"
PROJECT_NAME="electromecanico-en-santiago"

# Credenciales desde env vars
CF_TOKEN="${CF_TOKEN:?Falta CF_TOKEN. Exportalo: export CF_TOKEN=cfut_xxx}"
CF_ACCOUNT="${CF_ACCOUNT:?Falta CF_ACCOUNT. Exportalo: export CF_ACCOUNT=6fc12c9a...}"

cd "$REPO_DIR"

MSG="${1:-update: deploy $(date +%Y-%m-%d_%H:%M)}"

echo "=========================================="
echo "🚀 Deploy: $PROJECT_NAME"
echo "📝 Commit: $MSG"
echo "=========================================="

# 1. git add + commit + push
git add -A
git commit -m "$MSG" || { echo "⚠️  Nada que commitear"; }
git push origin main

# 2. wrangler deploy
echo "--------------------------------------------"
echo "☁️  Subiendo a Cloudflare Pages..."
echo "--------------------------------------------"
CLOUDFLARE_API_TOKEN="$CF_TOKEN" \
CLOUDFLARE_ACCOUNT_ID="$CF_ACCOUNT" \
npx --yes wrangler@latest pages deploy . \
  --project-name="$PROJECT_NAME" \
  --branch=main \
  --commit-dirty=true

echo "=========================================="
echo "✅ Deploy completado"
echo "🌐 https://$PROJECT_NAME.pages.dev"
echo "=========================================="
