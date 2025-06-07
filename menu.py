import customtkinter as ctk
from tkinter import messagebox
import os

class MenuApp:
    def __init__(self):
        ctk.set_appearance_mode("light")
        self.root = ctk.CTk()
        self.root.title("PanKira AI")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        self.main_frame = ctk.CTkFrame(self.root, fg_color="skyblue", border_width=0, corner_radius=0)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
        self.mostrar_menu_principal()

    def abrir_prediccion(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        loading_label = ctk.CTkLabel(self.main_frame, text="Cargando...", font=("Arial", 18))
        loading_label.place(relx=0.5, rely=0.4, anchor="center")
        progress = ctk.CTkProgressBar(self.main_frame, mode="indeterminate", width=200)
        progress.place(relx=0.5, rely=0.5, anchor="center")
        self.main_frame.after(0, progress.start)

        import importlib.util
        import threading

        def cargar_main():
            spec = importlib.util.spec_from_file_location("main", os.path.join(os.path.dirname(__file__), "main.py"))
            main_mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(main_mod)
            if hasattr(main_mod, "MainApp"):
                self.main_frame.after(0, lambda: _finish_loading(main_mod.MainApp))
            elif hasattr(main_mod, "main"):
                self.main_frame.after(0, lambda: _finish_loading(main_mod.main))
            else:
                self.main_frame.after(0, lambda: _finish_loading(None))

        def _finish_loading(main_func):
            progress.stop()
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            if main_func:
                # Si es clase, instanciarla y pasar el frame y el callback para "Atrás"
                if isinstance(main_func, type):
                    main_func(self.main_frame, on_back=self.mostrar_menu_principal)
                else:
                    main_func(self.main_frame)
            else:
                ctk.CTkLabel(
                    self.main_frame, text="main.py no tiene función main(frame) ni clase MainApp",
                    text_color="red"
                ).place(relx=0.5, rely=0.5, anchor="center")

        threading.Thread(target=cargar_main).start()

    def interpretar(self):
        messagebox.showinfo("Interpretar", "Funcionalidad en desarrollo")

    def cerrar(self):
        self.root.destroy()

    def mostrar_menu_principal(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        title_label = ctk.CTkLabel(self.main_frame, text="PanKira AI", font=("Arial", 32), fg_color="transparent")
        title_label.place(relx=0.5, rely=0.18, anchor="center")
        btn_predecir = ctk.CTkButton(self.main_frame, text="Predecir", corner_radius=5, command=self.abrir_prediccion)
        btn_predecir.place(relx=0.5, rely=0.38, anchor="center")
        btn_interpretar = ctk.CTkButton(self.main_frame, text="Interpretar", corner_radius=5, command=self.interpretar)
        btn_interpretar.place(relx=0.5, rely=0.50, anchor="center")
        btn_cerrar = ctk.CTkButton(self.main_frame, text="Cerrar", corner_radius=5, command=self.cerrar)
        btn_cerrar.place(relx=0.5, rely=0.62, anchor="center")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MenuApp()
    app.run()
