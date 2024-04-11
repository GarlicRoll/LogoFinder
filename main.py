import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from ttkbootstrap import Style
import PJ_graph

style = Style(theme="lumen")

class PhotoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Загрузить фото")
        self.geometry("600x600")

        # Создание верхней панели с кнопками
        self.button_panel = tk.Frame(self)
        self.button_panel.pack(side="top", fill="x")
        self.button_panel.configure(background="#9aa199")  # Установка цвета фона панели

        # Пользовательский цвет для подсветки кнопок
        self.highlight_color = "#9aff99"  # Здесь вы можете использовать любой цвет в формате HEX или название цвета
        self.colour1="#ffa199"
        self.colour2="#ffffff"
        # Кнопка "Загрузить фото"
        self.load_button = tk.Button(self.button_panel, text="Загрузить фото", command=self.load_image)
        self.load_button.pack(side="left", padx=10, pady=5)
        self.load_button.configure(background=self.colour1, foreground=self.colour2)
        self.load_button.bind("<Enter>", lambda event: self.on_enter(event, self.load_button))  # Привязка события наведения мыши
        self.load_button.bind("<Leave>", lambda event: self.on_leave(event, self.load_button))  # Привязка события покидания мыши

        # Кнопка "Рассчитать"
        self.calculate_button = tk.Button(self.button_panel, text="Рассчитать", command=self.load_image_from_project)
        self.calculate_button.pack(side="left", padx=10, pady=5)
        self.calculate_button.configure(background=self.colour1, foreground=self.colour2)
        self.calculate_button.bind("<Enter>", lambda event: self.on_enter(event, self.calculate_button))  # Привязка события наведения мыши
        self.calculate_button.bind("<Leave>", lambda event: self.on_leave(event, self.calculate_button))  # Привязка события покидания мыши

        # Создание метки для отображения изображения
        self.image_label = tk.Label(self)
        self.image_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)  # Занимает 80% ширины и высоты окна

        self.fig = PJ_graph.generate_image()

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            image = image.convert("RGB")  
            self.photo = ImageTk.PhotoImage(image=image)  
            self.image_label.config(image=self.photo)

    def load_image_from_project(self):
        PJ_graph.save_image(self.fig)
        
        # Загрузка изображения
        image = Image.open('graph_image.png')
        image = ImageTk.PhotoImage(image=image)
        
        # Отображение изображения в метке
        self.image_label.config(image=image)
        self.image_label.image = image


        PJ_graph.os.remove('graph_image.png')
    
    def on_enter(self, event, button):
        button.configure(background=self.highlight_color, padx=15, pady=10, relief=tk.RAISED)  # Изменение цвета и размера кнопки при наведении

    def on_leave(self, event, button):
        button.configure(background=self.colour1, padx=10, pady=5, relief=tk.FLAT)  # Возвращение исходного цвета и размера кнопки после покидания мыши

if __name__ == "__main__":
    app = PhotoApp()
    app.mainloop()
