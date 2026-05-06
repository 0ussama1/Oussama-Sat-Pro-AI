[app]

# (str) Titre de l'application
title = OUSSAMA SAT PRO AI

# (str) Nom du package
package.name = oussamasatproai

# (str) Domaine du package
package.domain = org.oussama.sat

# (str) Source directory
source.dir = .

# (list) Extensions à inclure
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) Répertoires à exclure
source.exclude_dirs = tests, bin, .buildozer, __pycache__, .git

# (str) Version de l'application
version = 1.0.1

# (list) Dépendances (Ajout de pyjnius pour le support USB/Android)
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pyjnius, plyer, pyserial, usb4a, usbserial4a, android

# (str) Orientation
orientation = portrait

# (int) Fullscreen (0 = show status bar)
fullscreen = 0

[buildozer]

# (int) Log level (2 = debug)
log_level = 2

# (int) Warn on root
warn_on_root = 1

[android]

# (int) API Android cible (Stable)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

# --- FIX CRITIQUE: Fixer la version des build-tools pour éviter l'erreur AIDL ---
android.build_tools_version = 33.0.2

# (bool) Accepter les licences SDK automatiquement
android.accept_sdk_license = True

# (list) Architectures
android.archs = arm64-v8a, armeabi-v7a

# (list) Dépendances Gradle pour USB Host
android.gradle_dependencies = androidx.appcompat:appcompat:1.6.1

# (list) Permissions
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, android.permission.USB_PERMISSION

# Caractéristiques matérielles USB
android.features = android.hardware.usb.host

# Branche p4a
p4a.branch = master

# ── Configuration de Signature ──────────────────────────────────────────────

# (bool) False pour un build Release
android.debug = False

# Fichiers Keystore
android.keystore = release.keystore
android.keyalias = oussama_sat

# Récupération des mots de passe depuis GitHub Secrets
android.keystore_passwd = %(environ.get('KEYSTORE_PASSWORD', ''))s
android.keyalias_passwd = %(environ.get('KEY_PASSWORD', ''))s

# ── Fix Sortie Artifact ─────────────────────────────────────────────────────
# Commenté pour permettre à GitHub Actions de localiser l'APK automatiquement
# android.release_artifact = apk

# ── Runtime ──────────────────────────────────────────────────────────────────
android.wakelock = True
