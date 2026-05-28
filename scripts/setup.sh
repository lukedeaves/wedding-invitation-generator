#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "Setting up Wedding Invitation Generator..."
if python3 -m venv .venv 2>/dev/null; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
else
  echo "Note: could not create a virtual environment; using system Python."
fi
python3 -m pip install --upgrade pip
pip install -r requirements.txt

if [[ ! -f config.yaml ]]; then
  cp config.example.yaml config.yaml
  echo "Created config.yaml from the example — please edit it with your details."
fi

echo ""
echo "Setup complete. Run: ./scripts/generate.sh"
