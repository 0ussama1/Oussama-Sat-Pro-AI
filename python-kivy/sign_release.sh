#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# OUSSAMA SAT PRO AI — APK Release Signing Script
#
# This script signs the unsigned release APK produced by Buildozer using
# apksigner (bundled with the Android SDK that Buildozer downloads).
#
# Run from inside python-kivy/ AFTER `buildozer android release` completes.
# ─────────────────────────────────────────────────────────────────────────────
set -e

# Load keystore credentials
if [ -f ".keystore.env" ]; then
    export $(grep -v '^#' .keystore.env | xargs)
else
    echo "ERROR: .keystore.env not found. Cannot sign APK." >&2
    exit 1
fi

# Locate apksigner inside the Buildozer-managed Android SDK
ANDROID_SDK="$HOME/.buildozer/android/platform/android-sdk"
APKSIGNER=$(find "$ANDROID_SDK/build-tools" -name "apksigner" 2>/dev/null | sort -V | tail -1)

if [ -z "$APKSIGNER" ]; then
    echo "ERROR: apksigner not found. Run 'buildozer android release' first so the SDK is downloaded." >&2
    exit 1
fi

# Find the unsigned APK produced by buildozer
UNSIGNED_APK=$(find bin/ -name "*-release-unsigned.apk" 2>/dev/null | head -1)
if [ -z "$UNSIGNED_APK" ]; then
    echo "ERROR: No unsigned release APK found in bin/. Run 'buildozer android release' first." >&2
    exit 1
fi

SIGNED_APK="${UNSIGNED_APK/-unsigned/}"
echo "==> Signing: $UNSIGNED_APK"
echo "==> Output:  $SIGNED_APK"

"$APKSIGNER" sign \
    --ks "$KEYSTORE_FILE" \
    --ks-key-alias "$KEYSTORE_ALIAS" \
    --ks-pass "pass:$KEYSTORE_PASSWORD" \
    --key-pass "pass:$KEY_PASSWORD" \
    --out "$SIGNED_APK" \
    "$UNSIGNED_APK"

echo ""
echo "==> Verifying signature..."
"$APKSIGNER" verify --verbose "$SIGNED_APK"

echo ""
echo "✅ Signed APK ready: $SIGNED_APK"
echo ""
echo "==> To install on a connected Android device:"
echo "    adb install \"$SIGNED_APK\""
