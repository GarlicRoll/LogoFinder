import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import threading
from recognizer import recognizer
from pathFinder import path_finder

class ImageViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Viewer")

        self.file_path = ""
        self.recognized_label = ""

        # Создание верхней панели с кнопками
        self.button_panel = tk.Frame(master)
        self.button_panel.pack(side="top", fill="x")
        self.button_panel.configure(background="#faedcd")  # Установка цвета фона панели

        # Пользовательский цвет для подсветки кнопок
        self.highlight_color = "#dda15e"  # Здесь вы можете использовать любой цвет в формате HEX или название цвета
        self.colour1 = "#faedcd"
        self.colour2 = "#495057"

        # Image label
        self.image_label = tk.Label(self.button_panel, text="Press 'Recognize'")
        self.image_label.bind()
        self.image_label.pack(fill=tk.BOTH, expand=True)

        # Кнопка "Загрузить фото"
        self.load_button = tk.Button(self.button_panel, text="Load Photo", command=self.uploader, font=("Arial", 12, "bold"))
        self.load_button.pack(side="left", padx=10, pady=5)
        self.load_button.configure(background=self.colour1, foreground=self.colour2, borderwidth=0, padx=15, pady=10)
        self.load_button.bind("<Enter>", lambda event: self.on_enter(event, self.load_button))  # Привязка события наведения мыши
        self.load_button.bind("<Leave>", lambda event: self.on_leave(event, self.load_button))  # Привязка события покидания мыши

        self.button1 = tk.Button(self.button_panel, text="Recognize", command=self.recognizer_m, font=("Arial", 12, "bold"))
        self.button1.pack(side="left", padx=10, pady=5)
        self.button1.configure(background=self.colour1, foreground=self.colour2, borderwidth=0, padx=15, pady=10)
        self.button1.bind("<Enter>", lambda event: self.on_enter(event, self.button1))  # Привязка события наведения мыши
        self.button1.bind("<Leave>", lambda event: self.on_leave(event, self.button1))

        self.button2 = tk.Button(self.button_panel, text="Find path", command=self.path_finder_m, font=("Arial", 12, "bold"))
        self.button2.pack(side="left", padx=10, pady=5)
        self.button2.configure(background=self.colour1, foreground=self.colour2, borderwidth=0, padx=15, pady=10)
        self.button2.bind("<Enter>", lambda event: self.on_enter(event, self.button2))  # Привязка события наведения мыши
        self.button2.bind("<Leave>", lambda event: self.on_leave(event, self.button2))

        self.canvas = tk.Canvas(master, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Enter>", self.enter_image)
        self.canvas.bind("<Leave>", self.leave_image)
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<ButtonRelease-1>", self.stop_move)
        self.canvas.bind("<B1-Motion>", self.move_image)

        self.image = None
        self.image_ref = None
        self.scale = 1.0
        self.cursor_on_image = False
        self.move_start_x = 0
        self.move_start_y = 0
        self.offset_x = 0
        self.offset_y = 0

        self.progressbar_recognize = None
        self.progressbar_find_path = None

    def uploader(self):
        file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.png;*.jpg;*.jpeg")])
        self.file_path = file_path
        if file_path:
            self.image = Image.open(file_path)
            self.display_image()

    def recognizer_m(self):
        self.progressbar_recognize = ttk.Progressbar(self.master, mode="indeterminate")
        self.progressbar_recognize.pack(side="bottom", fill="x")
        self.progressbar_recognize.start()
        threading.Thread(target=self.recognize_task).start()

    def recognize_task(self):
        self.recognized_label = recognizer(self.file_path)
        self.image_label.config(text=self.recognized_label)
        self.progressbar_recognize.stop()
        self.progressbar_recognize.destroy()

    def path_finder_m(self):
        self.progressbar_find_path = ttk.Progressbar(self.master, mode="indeterminate")
        self.progressbar_find_path.pack(side="bottom", fill="x")
        self.progressbar_find_path.start()
        threading.Thread(target=self.path_finder_task).start()

    def path_finder_task(self):
        image = path_finder(self.recognized_label)
        self.image = image
        self.display_image()
        self.progressbar_find_path.stop()
        self.progressbar_find_path.destroy()

    def display_image(self):
        if self.image_ref:
            self.canvas.delete(self.image_ref)
        if self.image:
            window_width = self.canvas.winfo_width()
            window_height = self.canvas.winfo_height()
            image_width, image_height = self.image.size

            new_width = int(image_width * self.scale)
            new_height = int(image_height * self.scale)

            # Вычисление координат верхнего левого угла изображения для центрирования
            x = (window_width - new_width) // 2 + self.offset_x
            y = (window_height - new_height) // 2 + self.offset_y

            resized_image = self.image.resize((new_width, new_height), 3)
            self.image_ref = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(x, y, anchor=tk.NW, image=self.image_ref)

    def zoom(self, event):
        if self.cursor_on_image and self.image:
            if event.delta > 0:
                self.scale *= 1.1
            else:
                self.scale /= 1.1
            self.display_image()

    def enter_image(self, event):
        self.cursor_on_image = True

    def leave_image(self, event):
        self.cursor_on_image = False

    def start_move(self, event):
        self.move_start_x = event.x
        self.move_start_y = event.y

    def stop_move(self, event):
        self.move_start_x = 0
        self.move_start_y = 0

    def move_image(self, event):
        if self.move_start_x and self.move_start_y and self.cursor_on_image and self.image:
            delta_x = event.x - self.move_start_x
            delta_y = event.y - self.move_start_y
            self.offset_x += delta_x
            self.offset_y += delta_y
            self.move_start_x = event.x
            self.move_start_y = event.y
            self.display_image()

    def on_enter(self, event, button):
        button.configure(background=self.highlight_color)  # Изменение цвета кнопки при наведении мыши

    def on_leave(self, event, button):
        button.configure(background=self.colour1)  # Возвращение исходного цвета кнопки после покидания мыши

def main():
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
