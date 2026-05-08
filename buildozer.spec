[app]
title = Oussama Sat Pro AI
package.name = oussamasatpro
package.domain = org.oussama.pro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pyserial,plyer,usb4a,usbserial4a
orientation = portrait
fullscreen = 0
android.permissions = USB_PERMISSION, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET, MANAGE_EXTERNAL_STORAGE

# الإصدارات المستقرة لتفادي خطأ Aidl
android.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 33.0.0
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

android.manifest.intent_filters = [ {"action": "android.hardware.usb.action.USB_DEVICE_ATTACHED"} ]

[buildozer]
log_level = 2
warn_on_root = 1
