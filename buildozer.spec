[app]
title = Oussama Sat Pro AI
package.name = oussamasat
package.domain = org.oussama
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 3.6

requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,android,usbserial4a

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE,USB_PERMISSION
android.features = android.hardware.usb.host

android.api = 33
android.minapi = 21
android.sdk = 33

log_level = 2
entrypoint = main.py
