#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────
# OUSSAMA SAT PRO AI — Buildozer APK build script
# Run this script from inside the python-kivy/ directory.
# ─────────────────────────────────────────────────────────
set -e

echo "==> Checking buildozer..."
if ! command -v buildozer &>/dev/null; then
    echo "==> Installing buildozer + Cython..."
    python3 -m pip install --user buildozer Cython
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "==> Cleaning previous build artifacts..."
buildozer android clean

echo "==> Building debug APK (this takes 10-30 min on first run)..."
echo "    Buildozer will download Android SDK, NDK and python-for-android automatically."
buildozer -v android debug

echo ""
echo "✅ Build complete!"
echo "   APK location: bin/oussamasatproai-1.0-arm64-v8a_armeabi-v7a-debug.apk"
echo ""
echo "==> To install directly on a connected Android device via USB:"
echo "   adb install bin/*.apk"
