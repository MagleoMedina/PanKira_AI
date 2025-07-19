# ... (código existente al principio del archivo menu.py)
import customtkinter as ctk
from tkinter import messagebox
import os
import importlib.util
import threading

class MenuApp:
    # ... (tu método __init__ y abrir_prediccion se mantienen igual)
    def __init__(self):
        # Establece el modo de apariencia a "Dark" para un look más moderno y profesional
        ctk.set_appearance_mode("Dark")
        # Establece el color primario para los widgets, que afectará botones, comboboxes, etc.
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("PanKira AI")
        self.root.geometry("600x500") # Un poco más grande para mejor espacio
        self.root.minsize(600, 600) # Establece un tamaño mínimo para la ventana
        
        # main_frame con un color de fondo más neutral o transparente
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent") # Usa transparente para que el fondo de la ventana sea el principal
        self.main_frame.pack(fill="both", expand=True) # Usa pack para llenar toda la ventana

        self.mostrar_menu_principal()

    def abrir_prediccion(self):
        """Carga el módulo de predicción y muestra la interfaz."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Mejorar la etiqueta de carga y la barra de progreso
        loading_label = ctk.CTkLabel(
            self.main_frame, 
            text="Cargando Módulo de Predicción...", 
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            text_color="gray70" # Un color más suave
        )
        loading_label.place(relx=0.5, rely=0.4, anchor="center")
        
        progress = ctk.CTkProgressBar(
            self.main_frame, 
            mode="indeterminate", 
            width=250, 
            height=10, 
            corner_radius=5
        )
        progress.place(relx=0.5, rely=0.5, anchor="center")
        self.main_frame.after(0, progress.start)

        def cargar_main():
            """Carga el módulo main.py y muestra la interfaz de predicción."""
            try:
                spec = importlib.util.spec_from_file_location("main", os.path.join(os.path.dirname(__file__), "main.py"))
                main_mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(main_mod)
                if hasattr(main_mod, "MainApp"):
                    self.main_frame.after(0, lambda: _finish_loading(main_mod.MainApp))
                elif hasattr(main_mod, "main"):
                    self.main_frame.after(0, lambda: _finish_loading(main_mod.main))
                else:
                    self.main_frame.after(0, lambda: _finish_loading(None, "Error: main.py no tiene 'main' o 'MainApp'."))
            except Exception as e:
                self.main_frame.after(0, lambda: _finish_loading(None, f"Error al cargar main.py: {e}"))

        def _finish_loading(main_func, error_message=None):
            """Finaliza la carga del módulo y muestra el contenido."""
            progress.stop()
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            
            if error_message:
                ctk.CTkLabel(
                    self.main_frame, 
                    text=error_message,
                    font=ctk.CTkFont(family="Arial", size=16),
                    text_color="red"
                ).place(relx=0.5, rely=0.5, anchor="center")
                # Añadir un botón para volver al menú principal en caso de error
                ctk.CTkButton(
                    self.main_frame, 
                    text="Volver al Menú", 
                    command=self.mostrar_menu_principal,
                    fg_color="gray50", # Un color de botón más neutro para errores
                    hover_color="gray60"
                ).place(relx=0.5, rely=0.6, anchor="center")
            elif main_func:
                if isinstance(main_func, type):
                    main_func(self.main_frame, on_back=self.mostrar_menu_principal)
                else:
                    main_func(self.main_frame)
            else:
                ctk.CTkLabel(
                    self.main_frame, text="Error desconocido al cargar módulo.",
                    text_color="red"
                ).place(relx=0.5, rely=0.5, anchor="center")

        threading.Thread(target=cargar_main).start()

    # --- MÉTODO MODIFICADO ---
    def analizar_ofertas(self):
        """Carga el módulo de recomendación de ofertas y muestra su interfaz."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        loading_label = ctk.CTkLabel(
            self.main_frame, text="Cargando Módulo de Ofertas...",
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"), text_color="gray70"
        )
        loading_label.place(relx=0.5, rely=0.4, anchor="center")
        
        progress = ctk.CTkProgressBar(self.main_frame, mode="indeterminate", width=250)
        progress.place(relx=0.5, rely=0.5, anchor="center")
        progress.start()

        def cargar_modulo_ofertas():
            try:
                spec = importlib.util.spec_from_file_location("interpretar_ofertas", os.path.join(os.path.dirname(__file__), "interpretar_ofertas.py"))
                ofertas_mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(ofertas_mod)
                
                if hasattr(ofertas_mod, "OfertasApp"):
                    self.main_frame.after(0, lambda: _finish_loading(ofertas_mod.OfertasApp))
                else:
                    self.main_frame.after(0, lambda: _finish_loading(None, "Error: 'interpretar_ofertas.py' no contiene la clase 'OfertasApp'."))
            except Exception as e:
                self.main_frame.after(0, lambda: _finish_loading(None, f"Error al cargar 'interpretar_ofertas.py': {e}"))

        def _finish_loading(app_class, error_message=None):
            progress.stop()
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            
            if error_message:
                ctk.CTkLabel(self.main_frame, text=error_message, text_color="red").place(relx=0.5, rely=0.5, anchor="center")
                ctk.CTkButton(self.main_frame, text="Volver", command=self.mostrar_menu_principal).place(relx=0.5, rely=0.6, anchor="center")
            elif app_class:
                app_class(self.main_frame, on_back=self.mostrar_menu_principal)

        threading.Thread(target=cargar_modulo_ofertas).start()
    
    def cerrar(self):
        """Cierra la aplicación."""
        self.root.destroy()
    
    # --- MÉTODO MODIFICADO ---
    def mostrar_menu_principal(self):
        """Muestra el menú principal de la aplicación."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        menu_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        menu_container.pack(expand=True)

        title_label = ctk.CTkLabel(
            menu_container, text="PanKira AI", 
            font=ctk.CTkFont(family="Arial", size=48, weight="bold"),
            text_color="gray80"
        )
        title_label.pack(pady=40)

        button_font = ctk.CTkFont(family="Arial", size=18)
        button_width = 200
        button_height = 45
        button_pady = 15

        btn_predecir = ctk.CTkButton(
            menu_container, text="Predecir Demanda", font=button_font, 
            width=button_width, height=button_height, corner_radius=8,
            command=self.abrir_prediccion
        )
        btn_predecir.pack(pady=button_pady)

        # Botón actualizado para llamar a la nueva función
        btn_interpretar = ctk.CTkButton(
            menu_container, text="Analizar Ofertas", font=button_font, 
            width=button_width, height=button_height, corner_radius=8,
            command=self.analizar_ofertas # Se cambió el comando
        )
        btn_interpretar.pack(pady=button_pady)

        btn_cerrar = ctk.CTkButton(
            menu_container, text="Salir", font=button_font,
            width=button_width, height=button_height, corner_radius=8,
            fg_color="red", hover_color="darkred",
            command=self.cerrar
        )
        btn_cerrar.pack(pady=button_pady)

    def run(self):
        """Inicia la aplicación."""
        self.root.mainloop()

if __name__ == "__main__":
    app = MenuApp()
    app.run()