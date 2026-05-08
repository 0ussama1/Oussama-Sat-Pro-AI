[app]
title = Oussama Sat Pro AI
package.name = oussamasatpro
package.domain = org.oussama.pro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# المتطلبات الأساسية
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pyserial,usb4a,usbserial4a

orientation = portrait
android.permissions = USB_PERMISSION, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET

# تغيير الأساسات التقنية
android.api = 34
android.minapi = 21
android.ndk = 26b
android.build_tools_version = 34.0.0
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
