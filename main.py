# كود التطبيق مع كل الأزرار والوظائف
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from usbserial4a import serial4a
import threading

class FlashUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        self.add_widget(Label(text="OUSSAMA SAT PRO AI v3.3", font_size=22))

        # أزرار أساسية
        self.add_btn("BROWSE ALL FILES", self.browse_files)
        self.add_btn("SCAN USB", self.scan_usb)
        self.add_btn("READ FLASH", self.read_flash)
        self.add_btn("ERASE CHIP", self.erase_chip)
        self.add_btn("START FLASH", self.start_flash)

        # أزرار إضافية
        self.add_btn("SAVE LOGS", self.save_logs)
        self.add_btn("PING DEVICE", self.ping_device)
        self.add_btn("CONNECTION SETTINGS", self.connection_settings)
        self.add_btn("DEVICE INFO", self.device_info)
        self.add_btn("STOP PROCESS", self.stop_process)

        self.status = Label(text="USB Status: Waiting...")
        self.add_widget(self.status)

        self.progress = ProgressBar(max=100, value=0)
        self.add_widget(self.progress)

        self.log = TextInput(readonly=True, size_hint=(1,0.3))
        self.add_widget(self.log)

        self.selected_port = None
        self.selected_file = None
        self.running = False
        self.baudrate = 115200

    def add_btn(self, text, func):
        btn = Button(text=text)
        btn.bind(on_press=func)
        self.add_widget(btn)

    def browse_files(self, instance):
        chooser = FileChooserIconView()
        popup = Popup(title="اختر ملف BIN", content=chooser, size_hint=(0.9,0.9))
        chooser.bind(on_submit=lambda chooser, selection, touch: self.set_file(selection, popup))
        popup.open()

    def set_file(self, selection, popup):
        if selection:
            self.selected_file = selection[0]
            self.add_log(f"📂 ملف مختار: {self.selected_file}")
        popup.dismiss()

    def scan_usb(self, instance):
        ports = serial4a.get_serial_ports()
        if ports:
            self.selected_port = ports[0]
            self.status.text = f"✅ USB détecté: {self.selected_port}"
            self.add_log(f"Port trouvé: {self.selected_port}")
        else:
            self.status.text = "❌ Aucun périphérique USB"
            self.add_log("USB non détecté")

    def read_flash(self, instance):
        if not self.selected_port:
            self.add_log("⚠️ Aucun port USB sélectionné")
            return
        try:
            ser = serial4a.Serial(port=self.selected_port, baudrate=self.baudrate, timeout=1)
            data = ser.read(256)
            self.add_log(f"📖 Données lues: {data}")
            ser.close()
        except Exception as e:
            self.add_log(f"⚠️ Erreur lecture: {e}")

    def erase_chip(self, instance):
        if not self.selected_port:
            self.add_log("⚠️ Aucun port USB sélectionné")
            return
        try:
            ser = serial4a.Serial(port=self.selected_port, baudrate=self.baudrate, timeout=1)
            ser.write(b"ERASE\n")
            self.add_log("🧹 Effacement demandé")
            ser.close()
        except Exception as e:
            self.add_log(f"⚠️ Erreur effacement: {e}")

    def start_flash(self, instance):
        if not self.selected_file or not self.selected_port:
            self.add_log("⚠️ Sélectionner fichier et port USB d'abord")
            return
        self.running = True
        threading.Thread(target=self.flash_process).start()

    def flash_process(self):
        try:
            ser = serial4a.Serial(port=self.selected_port, baudrate=self.baudrate, timeout=1)
            with open(self.selected_file, "rb") as f:
                data = f.read()
            total = len(data)
            chunk_size = 1024
            sent = 0
            for i in range(0, total, chunk_size):
                if not self.running:
                    self.add_log("⏹ عملية توقفت")
                    break
                chunk = data[i:i+chunk_size]
                ser.write(chunk)
                sent += len(chunk)
                self.progress.value = int((sent/total)*100)
                self.add_log(f"Envoyé {sent}/{total} octets")
            ser.close()
            self.add_log("🚀 Fichier envoyé avec succès")
        except Exception as e:
            self.add_log(f"⚠️ Erreur: {e}")

    def save_logs(self, instance):
        try:
            with open("logs.txt", "w") as f:
                f.write(self.log.text)
            self.add_log("💾 Logs sauvegardés dans logs.txt")
        except Exception as e:
            self.add_log(f"⚠️ Erreur sauvegarde: {e}")

    def ping_device(self, instance):
        if not self.selected_port:
            self.add_log("⚠️ Aucun port USB sélectionné")
            return
        try:
            ser = serial4a.Serial(port=self.selected_port, baudrate=self.baudrate, timeout=1)
            ser.write(b"PING\n")
            reply = ser.read(64)
            self.add_log(f"📡 Réponse: {reply}")
            ser.close()
        except Exception as e:
            self.add_log(f"⚠️ Erreur ping: {e}")

    def connection_settings(self, instance):
        self.add_log(f"⚙️ Baudrate actuel: {self.baudrate}")

    def device_info(self, instance):
        self.add_log("ℹ️ Info device (simulation): Version 1.0, Flash 4MB")

    def stop_process(self, instance):
        self.running = False
        self.add_log("⏹ عملية الإرسال توقفت")

    def add_log(self, message):
        self.log.text += message + "\n"

class MyApp(App):
    def build(self):
        return FlashUI()

if __name__ == "__main__":
    MyApp().run()
