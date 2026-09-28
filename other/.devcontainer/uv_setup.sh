#!/usr/bin/env bash
set -euxo pipefail

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install runtime deps into .venv
uv sync

# Activate venv
echo 'source .venv/bin/activate' >> ~/.bashrc