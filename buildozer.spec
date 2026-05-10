[app]
title = Oussama-Sat-Pro-AI
package.name = oussama_sat_pro_ai
package.domain = org.oussama
source.dir = .
source.include_exts = py,png,jpg,kv,bin,txt
version = 1.0.0
requirements = python3,kivy==2.3.0,usbserial4a,pillow,plyer,requests,certifi
orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,USB_PERMISSION
android.features = android.hardware.usb.host
entrypoint = main.py

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a,armeabi-v7a
