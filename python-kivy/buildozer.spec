[app]

# (str) Titre de votre application
title = OUSSAMA SAT PRO AI

# (str) Nom du package
package.name = oussamasatproai

# (str) Domaine du package
package.domain = org.oussama.sat

# (str) Répertoire source
source.dir = .

# (list) Extensions de fichiers à inclure
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) Répertoires à exclure
source.exclude_dirs = tests, bin, .buildozer, __pycache__, .git

# (str) Version de l'application
# CHANGEMENT : Version 1.2 pour forcer un build propre
version = 1.2

# (list) Dépendances (Core + USB Serial pour matériel SAT)
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pyjnius, plyer, pyserial, usb4a, usbserial4a, android

# (str) Orientation
orientation = portrait

# (int) Plein écran (0 pour afficher la barre d'état)
fullscreen = 0

[buildozer]

# (int) Niveau de log (2 pour le debug)
log_level = 2

# (int) Avertir si Buildozer est lancé en root
warn_on_root = 1

[android]

# (int) API Android cible et SDK (Stable 33)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

# --- FIX CRITIQUE: Fixer les build-tools pour éviter l'erreur AIDL ---
android.build_tools_version = 33.0.2

# (bool) Accepter les licences SDK
android.accept_sdk_license = True

# (list) Architectures supportées
android.archs = arm64-v8a, armeabi-v7a

# (list) Dépendances Gradle
android.gradle_dependencies = androidx.appcompat:appcompat:1.6.1

# (list) Permissions Android
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, android.permission.USB_PERMISSION

# Caractéristiques matérielles USB Host
android.features = android.hardware.usb.host

# Branche Python-for-Android
p4a.branch = master

# ── Configuration de Signature ──────────────────────────────────────────────

# (bool) False pour un build de production (Release)
android.debug = False

# Fichiers Keystore
android.keystore = release.keystore
android.keyalias = oussama_sat

# Récupération des mots de passe (Secrets GitHub)
android.keystore_passwd = %(environ.get('KEYSTORE_PASSWORD', ''))s
android.keyalias_passwd = %(environ.get('KEY_PASSWORD', ''))s

# ── FIX SIGNATURE ──────────────────────────────────────────────────────────
# IMPORTANT: Ne pas définir android.release_artifact pour laisser GitHub trouver l'APK
# android.release_artifact = apk

# ── Comportement au Runtime ──────────────────────────────────────────────────
android.wakelock = True