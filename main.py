# -*- coding: utf-8 French -*-
# Developpé par Oussama - Edition 2026

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
import threading

try:
    from usb4a import usb
    from usbserial4a import serial4a
except ImportError:
    usb = None

class OussamaSatApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_file("gui.kv")

    def on_start(self):
        # Surveillance des ports USB en arrière-plan
        threading.Thread(target=self.monitor_usb, daemon=True).start()

    def monitor_usb(self):
        while True:
            if usb:
                dev_list = usb.get_usb_device_list()
                if dev_list:
                    for dev in dev_list:
                        msg = f"Appareil Detecté: {dev.getProductName()}"
                        Clock.schedule_once(lambda dt: self.set_status(msg))
            Clock.tick(2)

    def set_status(self, text):
        self.root.ids.status_label.text = text

    def action_flash(self, type_box):
        self.set_status(f"Flash {type_box} en cours...")

if __name__ == "__main__":
    OussamaSatApp().run()
