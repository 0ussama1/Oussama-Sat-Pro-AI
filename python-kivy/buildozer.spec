[app]

# App metadata
title = OUSSAMA SAT PRO AI
package.name = oussamasatproai
package.domain = org.oussama.sat

# Source
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
source.exclude_dirs = tests, bin, .buildozer, __pycache__, .git

# Version
version = 1.0

# Requirements — core Kivy stack + Android USB serial
requirements =
    python3,
    kivy==2.3.0,
    kivymd==1.2.0,
    plyer,
    pyserial,
    usb4a,
    usbserial4a,
    android

# Orientation
orientation = portrait

# Fullscreen (0 = show status bar)
fullscreen = 0

# Icon & presplash (place icon.png / presplash.png next to main.py to use)
#icon.filename = %(source.dir)s/icon.png
#presplash.filename = %(source.dir)s/presplash.png

[buildozer]

# Log level: 0 = error, 1 = info, 2 = debug
log_level = 2

# Warn on root
warn_on_root = 1

[android]

# Android API & build tools
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.build_tools_version = 33.0.2

# Accept licenses automatically
android.accept_sdk_license = True

# Architectures — build both arm variants for widest device support
android.archs = arm64-v8a, armeabi-v7a

# Gradle dependencies for USB Host support
android.gradle_dependencies = androidx.appcompat:appcompat:1.6.1

# Permissions
android.permissions =
    INTERNET,
    READ_EXTERNAL_STORAGE,
    WRITE_EXTERNAL_STORAGE,
    android.permission.USB_PERMISSION

# USB Host hardware feature declaration
android.features = android.hardware.usb.host

# Enable USB host in the manifest
android.add_src = usb_host_support

# Use Python-for-Android branch compatible with KivyMD 1.2
p4a.branch = master

# Release vs debug APK (change to release for signed production build)
android.debug = True

# Keep the app running in background (useful for long flash operations)
android.wakelock = True
