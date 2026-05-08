import os, sys
from kivymd.app import MDApp
from kivy.lang import Builder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from usb_handler import monitor_usb_ports
    from flash_engine import perform_flash
except ImportError:
    pass

class OussamaSatApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_file("gui.kv")

    def on_start(self):
        import threading
        threading.Thread(target=monitor_usb_ports, args=(self,), daemon=True).start()

if __name__ == "__main__":
    OussamaSatApp().run()
