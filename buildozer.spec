[app]
title = Oussama Sat Pro AI
package.name = oussamasatpro
package.domain = org.oussama
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
# نسخ متناغمة جداً لمنع تعارض المكتبات
requirements = python3==3.11.0,kivy==2.3.0,requests,certifi
orientation = portrait
android.archs = arm64-v8a
android.api = 31
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 31.0.0
android.accept_sdk_license = True
android.enable_androidx = True
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
