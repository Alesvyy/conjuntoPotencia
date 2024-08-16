import tkinter as tk
from tkinter import messagebox, scrolledtext
from itertools import chain, combinations
import math
import os

def powerset(iterable):
    "Genera el conjunto potencia de un iterable."
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

class VisualApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conjunto Potencia Visual")
        self.set_icon()
        self.center_window(850, 700)
        self.root.state('zoomed')  # Maximiza la ventana al iniciar
        
        # Fuentes utilizadas en la aplicación
        main_font = ("Montserrat", 10, "normal")
        label_font = ("Montserrat", 14, "bold")  # Fuente más grande para la etiqueta principal

        # Etiqueta principal con tamaño de fuente aumentado
        tk.Label(root, text="Introduce los elementos del conjunto (separados por comas):", font=label_font).pack(pady=20)

        # Ajuste del tamaño de la entrada (más corta y más alta)
        self.entry = tk.Entry(root, font=("Montserrat", 12, "normal"), width=25)
        self.entry.pack(pady=10)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Mostrar Conjunto Potencia", command=self.show_powerset, bg="#00479B", fg="white", relief="flat", width="22", font=main_font).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Pasos", command=self.show_steps, bg="#2D91CF", fg="white", relief="flat", width="6", font=main_font).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="X", command=self.clear_canvas, bg="#800A0A", fg="white", relief="flat", width="2", font=main_font).pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(root, bg='white')
        self.canvas.pack(pady=10, fill=tk.BOTH, expand=True)
        
    def set_icon(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, '..' ,'iconos', 'conjunto.ico')
        icon_path = os.path.abspath(icon_path)
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el ícono: {e}")
        else:
            messagebox.showerror("Error", f"El ícono no existe en la ruta: {icon_path}")


    def generate_colors(self, num_colors):
        # Colores pastel para los círculos
        base_colors = ['#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9', '#BAE1FF', '#D5B0B0', '#B0D4FF', '#B9FBC0', '#E0BBE4', '#F9F3F3']
        return [base_colors[i % len(base_colors)] for i in range(num_colors)]

    def calculate_font_size(self, text, radius):
        """Calcula el tamaño de la fuente en función del tamaño del círculo y el texto."""
        # Obtener un tamaño base de fuente proporcional al radio
        base_font_size = int(radius * 0.4)

        # Crear una etiqueta temporal para medir el tamaño del texto con la fuente base
        temp_label = tk.Label(self.canvas, text=text, font=("Arial", base_font_size))
        temp_label.update_idletasks()  # Asegura que el tamaño se calcule correctamente
        text_width = temp_label.winfo_reqwidth()
        text_height = temp_label.winfo_reqheight()
        temp_label.destroy()  # Eliminar la etiqueta temporal
        
        # Ajustar el tamaño de la fuente si el texto no cabe en el círculo
        while (text_width > radius * 2 or text_height > radius * 2) and base_font_size > 5:
            base_font_size -= 1
            temp_label = tk.Label(self.canvas, text=text, font=("Arial", base_font_size))
            temp_label.update_idletasks()
            text_width = temp_label.winfo_reqwidth()
            text_height = temp_label.winfo_reqheight()
            temp_label.destroy()

        return base_font_size

    def show_powerset(self):
        self.canvas.delete("all")
        elements = [e.strip() for e in self.entry.get().split(',') if e.strip()]
        if not elements:
            messagebox.showerror("Error", "Introduce al menos un elemento.")
            return

        # Esperar a que el canvas se haya renderizado para obtener las dimensiones correctas
        self.root.update_idletasks()

        subsets = list(powerset(elements))
        num_subsets = len(subsets)

        # Ajustar el radio y la distancia de los círculos en función del tamaño del canvas
        radius = max(20, min(self.canvas.winfo_width(), self.canvas.winfo_height()) / (2.5 * num_subsets))
        distance = min(self.canvas.winfo_width(), self.canvas.winfo_height()) / 2.6  # Distancia desde el centro
        colors = self.generate_colors(num_subsets)
        angle_step = 2 * math.pi / num_subsets
        center_x, center_y = self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2

        for i, subset in enumerate(subsets):
            angle = i * angle_step
            x = center_x + distance * math.cos(angle)
            y = center_y + distance * math.sin(angle)
            x, y = min(max(radius, x), self.canvas.winfo_width() - radius), min(max(radius, y), self.canvas.winfo_height() - radius)
            subset_text = ', '.join(subset) if subset else '∅'
            font_size = self.calculate_font_size(subset_text, radius)
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=colors[i], outline=colors[i])  # Misma coloración para relleno y borde
            self.canvas.create_text(x, y, text=subset_text, font=("Arial", font_size), fill='black')


    def show_steps(self):
        elements = [e.strip() for e in self.entry.get().split(',') if e.strip()]
        if not elements:
            messagebox.showerror("Error", "Introduce al menos un elemento.")
            return

        steps_window = tk.Toplevel(self.root)
        steps_window.title("Pasos para Calcular el Conjunto Potencia")
        self.center_window(700, 400, steps_window)

        self.set_icon_for_window(steps_window)

        steps_text = scrolledtext.ScrolledText(steps_window, font=("Montserrat", 10, "normal"))
        steps_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        steps_text.insert(tk.END, "Pasos para calcular el conjunto potencia:\n\n")
        steps_text.insert(tk.END, "1. **Identificar los elementos del conjunto:**\n")
        steps_text.insert(tk.END, f"   - Elementos: {', '.join(elements)}\n\n")
        steps_text.insert(tk.END, "2. **Generar todos los subconjuntos posibles:**\n")
        steps_text.insert(tk.END, "   - El conjunto potencia incluye todos los subconjuntos, incluyendo el subconjunto vacío.\n")
        steps_text.insert(tk.END, "   - Ejemplo: Si el conjunto es {A, B}, el conjunto potencia es {∅, {A}, {B}, {A, B}}.\n\n")
        steps_text.insert(tk.END, "3. **Dibujar los subconjuntos en la interfaz:**\n")
        steps_text.insert(tk.END, "   - Cada subconjunto se representa con un círculo en la interfaz gráfica.\n")
        steps_text.insert(tk.END, "   - Los subconjuntos se distribuyen en una disposición circular para mejor visualización.\n\n")
        steps_text.insert(tk.END, "4. **Resultado final:**\n")
        steps_text.insert(tk.END, f"   - El conjunto potencia de los elementos {', '.join(elements)} se visualiza en la interfaz.\n\n")
        
        subsets = list(powerset(elements))
        formatted_subsets = ['{Ø}' if not subset else '{' + ', '.join(subset) + '}' for subset in subsets]
        formatted_subsets_str = '{' + ', '.join(formatted_subsets) + '}'
        steps_text.insert(tk.END, f"Resultado:\n")
        steps_text.insert(tk.END, f"{formatted_subsets_str}\n")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.entry.delete(0, tk.END)

    def center_window(self, width, height, window=None):
        if window is None:
            window = self.root
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 5
        window.geometry(f'{width}x{height}+{x}+{y}')
        window.update_idletasks()  # Asegura que el cálculo se actualice

        
    def set_icon_for_window(self, window):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, '..' ,'iconos', 'conjunto.ico')
        icon_path = os.path.abspath(icon_path)
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el ícono: {e}")
        else:
            messagebox.showerror("Error", f"El ícono no existe en la ruta: {icon_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = VisualApp(root)
    root.mainloop()
