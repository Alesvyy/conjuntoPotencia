# Inspirado de https://www.disfrutalasmatematicas.com/conjuntos/conjunto-potencia-creador.html
# Creado por: Alejandro Soto y Jeffry Valverde

import tkinter as tk
from tkinter import messagebox, scrolledtext
from itertools import chain, combinations
import math
import os

def powerset(iterable):
    "Genera el conjunto potencia de un iterable."
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

class VisualApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conjunto Potencia Visual")
        
        # Tipografia
        Font_tuple = ("Montserrat", 10, "normal") 

        # Configurar el icono de la ventana
        self.set_icon()
        
        # Centrar venta en la pantalla
        self.center_window(self.root, 850, 850)

        # Etiqueta de entrada
        self.label = tk.Label(root, text="Introduce los elementos del conjunto (separados por comas):")
        self.label.pack(pady=20)
        self.label['font'] = Font_tuple

        # Entrada de texto
        self.entry = tk.Entry(root, width=35)
        self.entry.pack(pady=10)
        self.entry['font'] = Font_tuple

        # Crear un marco para contener los botones
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        # Botón para mostrar el conjunto potencia
        show_button = tk.Button(button_frame, text="Mostrar Conjunto Potencia", command=self.show_powerset, bg="#00479B", fg="white", relief="flat", width="22")
        show_button.pack(side=tk.LEFT, padx=5)
        show_button['font'] = Font_tuple

        # Botón para mostrar los pasos
        steps_button = tk.Button(button_frame, text="Pasos", command=self.show_steps, bg="#2D91CF", fg="white", relief="flat", width="6")
        steps_button.pack(side=tk.LEFT, padx=5)
        steps_button['font'] = Font_tuple
        
        clean_button = tk.Button(button_frame, text="X", command=self.clear_canvas, bg="#800A0A", fg="white", relief="flat", width="2")
        clean_button.pack(side=tk.LEFT, padx=5)
        clean_button['font'] = Font_tuple

        # Lienzo para dibujar los círculos
        self.canvas = tk.Canvas(root, width=800, height=650, bg='white')
        self.canvas.pack(pady=10)
        
    def set_icon(self):
        # Ruta del icono
        icon_path = os.path.join('iconos', 'conjunto.ico')

        # Establecer el icono de la ventana
        try:
            self.root.iconbitmap(icon_path)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el icono: {e}")

    def show_powerset(self):
        # Limpiar lienzo
        self.canvas.delete("all")

        # Obtener los elementos
        input_text = self.entry.get()
        elements = [e.strip() for e in input_text.split(',')]
        if not elements or all(e == '' for e in elements):
            messagebox.showerror("Error", "Introduce al menos un elemento.")
            return

        # Calcular conjunto potencia
        subsets = list(powerset(elements))
        
        # Determinar el número total de subconjuntos
        num_subsets = len(subsets)
        
        # Tamaño y ubicación de los círculos
        radius = 30
        center_x, center_y = 400, 325
        distance = 270

        # Calcular ángulo para distribución circular
        angle_step = 2 * math.pi / num_subsets
        
        for i, subset in enumerate(subsets):
            angle = i * angle_step
            x = center_x + distance * math.cos(angle)
            y = center_y + distance * math.sin(angle)

            # Dibujar círculo
            self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill='lightblue', outline='black')
            self.canvas.create_text(x, y, text=', '.join(subset) if subset else '∅', font=("Arial", 12))

    def show_steps(self):
        input_text = self.entry.get()
        elements = [e.strip() for e in input_text.split(',')]
        if not elements or all(e == '' for e in elements):
            messagebox.showerror("Error", "Introduce al menos un elemento.")
            return

        # Crear ventana de pasos
        steps_window = tk.Toplevel(self.root)
        steps_window.title("Pasos para Calcular el Conjunto Potencia")
        self.center_window(steps_window, 700, 400)

        # Configurar el icono de la ventana de pasos
        self.set_icon_for_window(steps_window)

        # Crear área de texto para mostrar los pasos
        steps_text = scrolledtext.ScrolledText(steps_window, width=150, height=30)
        steps_text.pack(pady=10)

        # Agregar pasos explicativos
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
        # Formatear los subconjuntos para que se muestren sin comillas ni comas innecesarias
        # Formatear los subconjuntos para que se muestren en el formato deseado
        formatted_subsets = ['{∅}' if not subset else '{' + ', '.join(subset) + '}' for subset in subsets]
        formatted_subsets_str = '{' + ', '.join(formatted_subsets) + '}'
        steps_text.insert(tk.END, f"Resultado:\n")
        steps_text.insert(tk.END, f"{formatted_subsets_str}\n")
        
        # Tipografia
        Font_tuple = ("Montserrat", 10, "normal") 
        steps_text['font'] = Font_tuple

    def clear_canvas(self):
        self.canvas.delete("all")
        self.entry.delete(0, tk.END)  
        
    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
        
    def set_icon_for_window(self, window):
        # Ruta del icono
        icon_path = os.path.join('iconos', 'conjunto.ico')

        # Establecer el icono de la ventana
        try:
            window.iconbitmap(icon_path)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el icono: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VisualApp(root)
    root.mainloop()