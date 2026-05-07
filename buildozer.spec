[app]
title = Oussama Sat Pro AI
package.name = oussamasatpro
package.domain = org.oussama
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
# استخدام نسخ محددة تمنع تعارض الـ autoconf
requirements = python3==3.11.0, hostpython3==3.11.0, kivy==2.3.0, requests, certifi, openssl
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.api = 31
android.minapi = 21
android.ndk = 25b
android.allow_backup = True
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
