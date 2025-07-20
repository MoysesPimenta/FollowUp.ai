#!/bin/bash
set -euo pipefail

# Install system packages
sudo apt-get update
sudo apt-get install -y curl git python3 python3-pip python3-venv

# Install Node and pnpm
curl -fsSL https://get.pnpm.io/install.sh | sh -

# Install python tooling
python3 -m pip install --upgrade pip
pip install flake8 black mypy

# Install JS tooling globally
pnpm add -g eslint prettier flow-bin stylelint
