# تطبيق OUSSAMA SAT PRO AI v3.6
# يحتوي على كل الأزرار والوظائف: Browse, Scan USB, Read Flash, Erase Chip, Start Flash
# + Save Logs, Ping Device, Device Info, Stop Process

from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.filemanager import MDFileManager
from android.permissions import request_permissions, Permission
from usbserial4a import serial4a
import os, threading

KV = '''
MDScreen:
    md_bg_color: [0.05, 0.1, 0.15, 1]
    MDBoxLayout:
        orientation: 'vertical'
        padding: "15dp"
        spacing: "10dp"
        
        MDLabel:
            text: "OUSSAMA SAT PRO AI v3.6"
            halign: "center"
            theme_text_color: "Custom"
            text_color: [0, 0.8, 1, 1]
            size_hint_y: None
            height: "40dp"

        MDCard:
            size_hint_y: None
            height: "60dp"
            md_bg_color: [0.1, 0.15, 0.2, 1]
            MDLabel:
                id: status_label
                text: "Status: Ready"
                halign: "center"

        MDRaisedButton:
            text: "📁 BROWSE INTERNAL STORAGE"
            size_hint_x: 1
            on_release: app.file_manager_open()

        MDGridLayout:
            cols: 2
            spacing: "10dp"
            size_hint_y: None
            height: "150dp"
            MDRaisedButton:
                text: "SCAN USB PORTS"
                on_release: app.scan_usb_ports()
            MDRaisedButton:
                text: "START FLASH"
                on_release: app.start_flash()
            MDRaisedButton:
                text: "READ FLASH"
                on_release: app.read_flash()
            MDRaisedButton:
                text: "ERASE CHIP"
                on_release: app.erase_chip()

        MDGridLayout:
            cols: 2
            spacing: "10dp"
            size_hint_y: None
            height: "150dp"
            MDRaisedButton:
                text: "SAVE LOGS"
                on_release: app.save_logs()
            MDRaisedButton:
                text: "PING DEVICE"
                on_release: app.ping_device()
            MDRaisedButton:
                text: "DEVICE INFO"
                on_release: app.device_info()
            MDRaisedButton:
                text: "STOP PROCESS"
                on_release: app.stop_process()

        MDCard:
            md_bg_color: [0, 0, 0, 0.4]
            ScrollView:
                MDLabel:
                    id: log_output
                    text: "--- Log System ---"
                    font_style: "Caption"
                    size_hint_y: None
                    height: self.texture_size[1]
'''

class OussamaSatApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=lambda x: self.file_manager.close(),
            select_path=self.select_path,
            ext=['.bin', '.abs', '.cfg', '.dmp']
        )
        self.selected_file = None
        self.running = False
        self.baudrate = 115200

    def build(self):
        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
        return Builder.load_string(KV)

    def file_manager_open(self):
        self.file_manager.show("/storage/emulated/0")

    def select_path(self, path):
        self.file_manager.close()
        self.selected_file = path
        self.update_log(f"Selected File: {os.path.basename(path)}")

    def scan_usb_ports(self):
        try:
            ports = serial4a.get_serial_ports()
            if ports:
                self.root.ids.status_label.text = f"✅ Found: {len(ports)} Port(s)"
                for p in ports: self.update_log(f"Found: {p}")
                self.selected_port = ports[0]
            else:
                self.update_log("❌ No USB Ports detected. Check OTG!")
        except Exception as e:
            self.update_log(f"Error: {str(e)}")

    def start_flash(self):
        if not self.selected_file:
            self.update_log("⚠️ No file selected")
            return
        if not hasattr(self, "selected_port"):
            self.update_log("⚠️ No USB port selected")
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
                    self.update_log("⏹ Process stopped")
                    break
                chunk = data[i:i+chunk_size]
                ser.write(chunk)
                sent += len(chunk)
                self.root.ids.status_label.text = f"Sent {sent}/{total} bytes"
                self.update_log(f"Chunk {i//chunk_size}: {len(chunk)} bytes")
            ser.close()
            self.update_log("🚀 Flash completed successfully!")
        except Exception as e:
            self.update_log(f"⚠️ Flash error: {str(e)}")

    def read_flash(self):
        if not hasattr(self, "selected_port"):
            self.update_log("⚠️ No USB port selected")
            return
        try:
            ser = serial4a.Serial(port=self.selected_port, baudrate=self.baudrate, timeout=1)
            data = ser.read(256)
            self.update_log(f"📖 Read: {data}")
            ser.close()
        except Exception as e:
            self.update_log(f"⚠️ Read error: {str(e)}")

    def erase_chip(self):
        if not hasattr(self, "selected_port"):
            self.update_log("⚠️ No USB port selected")
            return
        try:
            ser = serial4a.Serial(port=self.selected_port, baudrate=self.baudrate, timeout=1)
            ser.write(b"ERASE\n")
            self.update_log("🧹 Erase command sent")
            ser.close()
        except Exception as e:
            self.update_log(f"⚠️ Erase error: {str(e)}")

    def save_logs(self):
        try:
            with open("logs.txt", "w") as f:
                f.write(self.root.ids.log_output.text)
            self.update_log("💾 Logs saved to logs.txt")
        except Exception as e:
            self.update_log(f"⚠️ Save error: {str(e)}")

    def ping_device(self):
        if not hasattr(self, "selected_port"):
            self.update_log("⚠️ No USB port selected")
            return
        try:
            ser = serial4a.Serial(port=self.selected_port, baudrate=self.baudrate, timeout=1)
            ser.write(b"PING\n")
            reply = ser.read(64)
            self.update_log(f"📡 Reply: {reply}")
            ser.close()
        except Exception as e:
            self.update_log(f"⚠️ Ping error: {str(e)}")

    def device_info(self):
        self.update_log("ℹ️ Device Info (simulation): Version 1.0, Flash 4MB")

    def stop_process(self):
        self.running = False
        self.update_log("⏹ Process stopped by user")

    def update_log(self, msg):
        self.root.ids.log_output.text += f"\n> {msg}"

if __name__ == "__main__":
    OussamaSatApp().run()
