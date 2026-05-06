[app]
title = OUSSAMA SAT PRO AI
package.name = oussamasatproai
package.domain = org.oussama.sat
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
source.exclude_dirs = tests, bin, .buildozer, __pycache__, .git

# تم تغيير الإصدار إلى 1.3 لإلغاء التخزين المؤقت (Cache)
version = 1.3

requirements = python3, kivy==2.3.0, kivymd==1.2.0, pyjnius, plyer, pyserial, usb4a, usbserial4a, android
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
# تثبيت النسخة المستقرة من أدوات البناء
android.build_tools_version = 33.0.2
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.gradle_dependencies = androidx.appcompat:appcompat:1.6.1
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, android.permission.USB_PERMISSION
android.features = android.hardware.usb.host
p4a.branch = master

# إعدادات التوقيع
android.debug = False
android.keystore = release.keystore
android.keyalias = oussama_sat
android.keystore_passwd = %(environ.get('KEYSTORE_PASSWORD', ''))s
android.keyalias_passwd = %(environ.get('KEY_PASSWORD', ''))s

# --- ملاحظة: لا تقم بإضافة سطر release_artifact ---
android.wakelock = True
