[app]
title = Oussama Sat Pro AI
package.name = oussamasatpro
package.domain = org.oussama
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.3.0,hostpython3==3.11.0,requests,certifi
orientation = portrait
android.archs = arm64-v8a
android.api = 34
android.minapi = 21
android.ndk = 26b
android.build_tools_version = 34.0.0
android.accept_sdk_license = True
android.enable_androidx = True
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
