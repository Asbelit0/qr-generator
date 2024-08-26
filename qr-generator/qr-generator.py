import tkinter as tk
from tkinter import messagebox
from qrcode import QRCode
import urllib.parse
import os

class QRGenerator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Generador de QR")
        self.window.geometry("400x600")
        self.window.configure(bg="black")

        # Entradas de texto
        self.text_label = tk.Label(self.window, text="A continuación ingrese si desea covertir a QR un texto, url o email:")
        self.text_label.pack(pady=20)

        self.text_label = tk.Label(self.window, text="Ingrese un texto:", font=("Arial", 11, "bold", "italic"),
                        bg="pink", borderwidth=2, relief="ridge")
        self.text_label.pack(pady=25)
        self.text_entry = tk.Entry(self.window, font=("Arial",10, "italic"), width=30, borderwidth=5, relief="ridge")
        self.text_entry.pack()

        self.url_label = tk.Label(self.window, text="Ingrese una URL:", font=("Arial", 11, "bold", "italic"),  
                        bg="pink", borderwidth=2, relief="ridge")
        self.url_label.pack(pady=30)
        self.url_entry = tk.Entry(self.window, font=("Arial",10, "italic"), width=30, borderwidth=5, relief="ridge")
        self.url_entry.pack()

        self.email_label = tk.Label(self.window, text="Ingrese un email:", font=("Arial", 11, "bold", "italic"), 
                        bg="pink", borderwidth=2, relief="ridge")
        self.email_label.pack(pady=30)
        self.email_entry = tk.Entry(self.window, font=("Arial",10, "italic"), width=30, borderwidth=5, relief="ridge")
        self.email_entry.pack()

        # Campo para ingresar el nombre del archivo
        self.nombre_label = tk.Label(self.window, text="Ingrese un nombre para su QR:", font=("Arial", 11,
                            "bold", "italic"), bg="pink", borderwidth=2, relief="ridge")
        self.nombre_label.pack(pady=30)
        self.nombre_entry = tk.Entry(self.window, font=("Arial",10, "italic"), width=30, borderwidth=5, relief="ridge")
        self.nombre_entry.pack()

        # Button para generar el Qr
        self.generate_btn = tk.Button(self.window, text="Generar QR", font=("Arial", 10, "bold",),
        command=self.generate_qr, bg="red", fg="white", bd=6, relief="groove")
        self.generate_btn.pack(pady=30)

        # Muestra la ventana
        self.window.mainloop()

    def _validate_url(self, url):
        try:
            result = urllib.parse.urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def _validate_email(self, email):
        try:
            result = email.split('@')
            return len(result) == 2 and result[1].endswith('.com')
        except ValueError:
            return False

    def generate_qr(self):
        nombre = self.nombre_entry.get()
        if not nombre:
            messagebox.showerror("Error", "Por favor, ingrese un nombre para el archivo.")
            return

        data = ""
        if self.text_entry.get():
            data = self.text_entry.get()
        elif self.url_entry.get():
            url = self.url_entry.get()
            if self._validate_url(url):
                data = url
            else:
                messagebox.showerror("Error", "URL Inválida")
                return
        elif self.email_entry.get():
            email = self.email_entry.get()
            if self._validate_email(email):
                data = f"Email:{email}"
            else:
                messagebox.showerror("Error", "Email Inválido")
                return

        if not data:
            messagebox.showerror("Error", "Por favor ingrese un texto, URL o e-mail.")
            return

        qr = QRCode(
            version=1,
            error_correction=1,
            box_size=10,
            border=4
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        nombre_archivo = f"{nombre}.png"

        if os.path.exists(nombre_archivo):
            respuesta = messagebox.askyesno("Archivo existente",
            f"El archivo {nombre_archivo} ya existe. ¿Desea reemplazarlo?")
            if not respuesta:
                return
        img.save(nombre_archivo)

        messagebox.showinfo("Listo", f"QR generado correctamente. Se ha guardado en {nombre_archivo}")

if __name__ == "__main__":
    QRGenerator()