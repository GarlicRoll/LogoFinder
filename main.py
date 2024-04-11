import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Viewer")


        # Создание верхней панели с кнопками
        self.button_panel = tk.Frame(master)
        self.button_panel.pack(side="top", fill="x")
        self.button_panel.configure(background="#faedcd")  # Установка цвета фона панели

        # Пользовательский цвет для подсветки кнопок
        self.highlight_color = "#dda15e"  # Здесь вы можете использовать любой цвет в формате HEX или название цвета
        self.colour1 = "#faedcd"
        self.colour2 = "#495057"

        # Кнопка "Загрузить фото"
        self.load_button = tk.Button(self.button_panel, text="Загрузить фото", command=self.load_image, font=("Arial", 12, "bold"))
        self.load_button.pack(side="left", padx=10, pady=5)
        self.load_button.configure(background=self.colour1, foreground=self.colour2, borderwidth=2, padx=15, pady=10)
        self.load_button.bind("<Enter>", lambda event: self.on_enter(event, self.load_button))  # Привязка события наведения мыши
        self.load_button.bind("<Leave>", lambda event: self.on_leave(event, self.load_button))  # Привязка события покидания мыши

        
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

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image = Image.open(file_path)
            self.display_image()

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
