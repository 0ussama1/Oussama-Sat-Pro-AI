#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# OUSSAMA SAT PRO AI — Full Release Build Script
# Builds a signed, release-ready APK in one step.
# Run from inside python-kivy/.
# ─────────────────────────────────────────────────────────────────────────────
set -e

echo "==> Checking buildozer..."
if ! command -v buildozer &>/dev/null; then
    echo "==> Installing buildozer + Cython..."
    python3 -m pip install --user buildozer Cython
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "==> Checking keystore..."
if [ ! -f "release.keystore" ]; then
    echo "ERROR: release.keystore not found." >&2
    echo "       Run the keygen script or restore the keystore from backup." >&2
    exit 1
fi

if [ ! -f ".keystore.env" ]; then
    echo "ERROR: .keystore.env not found (contains keystore credentials)." >&2
    exit 1
fi

echo "==> Building release APK..."
buildozer -v android release

echo "==> Signing APK..."
./sign_release.sh

echo ""
echo "✅ Release build complete!"
echo "   Signed APK is in bin/"
