#!/bin/bash
# Prépare le kit pour une nouvelle vidéo : installe Remotion, copie le logo.
set -e
cd "$(dirname "$0")"
npm install --silent
cp ../logo.png public/logo.png
pip install faster-whisper opencv-python-headless --break-system-packages -q 2>/dev/null || true
echo "Kit prêt. Navigateur : $(ls /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell 2>/dev/null | head -1)"
