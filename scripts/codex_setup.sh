#!/bin/bash
set -euo pipefail

if ! command -v pnpm >/dev/null 2>&1; then
  npm install -g pnpm
fi

pnpm install --frozen-lockfile || pnpm install

if [ -f requirements.txt ]; then
  pip install --upgrade pip
  pip install -r requirements.txt
fi
