import subprocess
import os
from tkinter import Tk, filedialog, simpledialog, messagebox, BooleanVar, Checkbutton, Button, Toplevel, Label

CALIBRE_PATH = r"C:\Program Files\Calibre2\ebook-convert.exe"

def mostrar_opciones_previas(parent, usar_nombre_autom):
    ventana = Toplevel(parent)
    ventana.title("Opciones de conversión")
    ventana.geometry("300x120")
    ventana.resizable(False, False)

    Label(ventana, text="Configuración antes de la conversión").pack(pady=10)

    check = Checkbutton(ventana, text="Usar nombre original del PDF sin preguntar",
                        variable=usar_nombre_autom)
    check.pack()

    Button(ventana, text="Continuar", command=ventana.destroy).pack(pady=10)

    ventana.grab_set()
    ventana.wait_window()  # Espera que se cierre sin crear un mainloop separado

def convertir_pdf_a_epub(ruta_pdf, carpeta_destino, usar_nombre_autom, ventana_progreso, etiqueta_contador, etiqueta_nombre, index, total):
    nombre_original = os.path.splitext(os.path.basename(ruta_pdf))[0]

    if usar_nombre_autom.get():
        nuevo_nombre = nombre_original
    else:
        nuevo_nombre = simpledialog.askstring(
            "Nombre del EPUB",
            f"Nombre para el EPUB generado:\n(Predeterminado: {nombre_original})",
            initialvalue=nombre_original
        )

        if not nuevo_nombre:
            print(f"⏩ Conversión cancelada para: {ruta_pdf}")
            return

    ruta_epub = os.path.join(carpeta_destino, nuevo_nombre + ".epub")

    # Actualizar ventana de progreso
    etiqueta_contador.config(text=f"Convirtiendo archivo {index + 1} de {total}")
    etiqueta_nombre.config(text=nombre_original + ".pdf")
    ventana_progreso.update_idletasks()

    comando = [
        CALIBRE_PATH,
        ruta_pdf,
        ruta_epub,
        "--enable-heuristics",
        "--preserve-cover-aspect-ratio"
    ]

    try:
        subprocess.run(comando, check=True)
        print(f"✅ Convertido: {ruta_epub}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al convertir {ruta_pdf}")
        print(e)

def seleccionar_y_convertir_multiples():
    root = Tk()
    root.withdraw()

    usar_nombre_autom = BooleanVar(root, value=True)

    archivos_pdf = filedialog.askopenfilenames(
        title="Selecciona varios archivos PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )

    if not archivos_pdf:
        root.destroy()
        return

    carpeta_destino = filedialog.askdirectory(
        title="Selecciona carpeta de destino para los EPUB"
    )

    if not carpeta_destino:
        root.destroy()
        return

    mostrar_opciones_previas(root, usar_nombre_autom)

    # Crear ventana de progreso
    ventana_progreso = Toplevel(root)
    ventana_progreso.title("Progreso de conversión")
    ventana_progreso.geometry("400x120")
    ventana_progreso.resizable(False, False)

    etiqueta_contador = Label(ventana_progreso, text="Iniciando...")
    etiqueta_contador.pack(pady=10)

    etiqueta_nombre = Label(ventana_progreso, text="")
    etiqueta_nombre.pack(pady=5)

    total = len(archivos_pdf)

    for i, archivo in enumerate(archivos_pdf):
        convertir_pdf_a_epub(
            archivo,
            carpeta_destino,
            usar_nombre_autom,
            ventana_progreso,
            etiqueta_contador,
            etiqueta_nombre,
            i,
            total
        )

    ventana_progreso.destroy()
    messagebox.showinfo("Proceso finalizado", "Todos los archivos han sido procesados.")
    root.destroy()

# Ejecutar
if __name__ == "__main__":
    seleccionar_y_convertir_multiples()
