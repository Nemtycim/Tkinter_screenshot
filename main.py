import tkinter as tk
import pyautogui
from tkinter import messagebox
from datetime import datetime

class DraggableWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Ekran Görüntüsü Yakalama Uygulaması")

        # Pencereyi sürüklemek için başlık çubuğuna veya pencere içeriğine tıklama işlevlerini bağlama
        self.root.bind("<ButtonPress-1>", self.start_drag)
        self.root.bind("<ButtonRelease-1>", self.stop_drag)
        self.root.bind("<B1-Motion>", self.on_drag)

        # Ekran görüntüsü alma bileşenlerini eklemek
        delay_label = tk.Label(root, text="Bekleme Süresi (saniye):")
        delay_label.pack()

        self.delay_entry = tk.Entry(root)
        self.delay_entry.pack()

        note = tk.Label(root, text="Kutuya süre girmenize gerek yoktur")
        note.pack()

        capture_button = tk.Button(root, text="Yakala", command=self.capture_screenshot)
        capture_button.pack()

        self.dragging = False
        self.start_x = 0
        self.start_y = 0

    def start_drag(self, event):
        if event.y <= 30:  # Başlık çubuğuna tıklama kontrolü
            self.dragging = True
            self.start_x = event.x_root - self.root.winfo_x()
            self.start_y = event.y_root - self.root.winfo_y()

    def stop_drag(self, event):
        self.dragging = False

    def on_drag(self, event):
        if self.dragging:
            x = event.x_root - self.start_x
            y = event.y_root - self.start_y
            self.root.geometry(f"+{x}+{y}")

    def capture_screenshot(self):
        # Ekran görüntüsü alma işlemi başlamadan önce pencereyi gizle
        self.root.withdraw()

        delay = self.delay_entry.get().strip()
        if not delay:
            self.take_screenshot()
        else:
            try:
                delay = int(delay)
                messagebox.showinfo("Bekleme Başladı", f"{delay} saniye bekleniyor...")
                self.root.update()
                self.root.after(delay * 1000, self.take_screenshot)
            except ValueError:
                messagebox.showerror("Hata", "Geçerli bir süre giriniz.")

    def take_screenshot(self):
        try:
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-d_%H-%M-%S")
            screenshot_filename = f"screenshot_{timestamp}.png"
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_filename)
            messagebox.showinfo("Başarılı", f"Ekran görüntüsü başarıyla kaydedildi: {screenshot_filename}")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

        # Ekran görüntüsü alma işlemi tamamlandığında pencereyi tekrar görünür yap
        self.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = DraggableWindow(root)
    root.mainloop()
