import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil


def operacionFotos(origen, destino, label_resultado, ventana, operacion):
    try:
        if not os.path.exists(destino):
            mensaje = f"Creando directorio de destino: {destino}"
            label_resultado.config(text=mensaje)
            ventana.update()
            os.makedirs(destino)

        archivos_por_mover = []

        for root, dirs, files in os.walk(origen):
            for filename in files:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.mp4', '.avi', '.mkv', '.flv', '.mov')):
                    origen_completo = os.path.join(root, filename)

                    # Obtener el nombre del directorio y construir la ruta de destino
                    directorio = os.path.relpath(root, origen)
                    destino_directorio = os.path.join(destino, directorio)

                    # Añadir la información del archivo para mover/copiar
                    destino_completo = os.path.join(destino_directorio, filename)
                    archivos_por_mover.append((origen_completo, destino_completo))

        for origen_completo, destino_completo in archivos_por_mover:
            try:
                if operacion == "mover":
                    mensaje = f"Moviendo: {origen_completo} ---> {destino_completo}"
                    label_resultado.config(text=mensaje)
                    ventana.update()
                elif operacion == "copiar":
                    mensaje = f"Copiando: {origen_completo} ---> {destino_completo}"
                    label_resultado.config(text=mensaje)
                    ventana.update()
                # Crear subcarpeta si no existe
                directorio = os.path.dirname(destino_completo)
                if not os.path.exists(directorio):
                    os.makedirs(directorio)

                if operacion == 'copiar':
                    shutil.copy2(origen_completo, destino_completo)
                elif operacion == 'mover':
                    shutil.move(origen_completo, destino_completo)
            except Exception as e:
                mensaje_error = f"Error al {operacion}: {filename}: {e}"
                label_resultado.config(text=mensaje_error)

            # Agregar una pausa pequeña para permitir la actualización de la interfaz gráfica
            ventana.after(100)

    except Exception as e:
        mensaje_general = f"Error general en el bucle principal: {e}"
        label_resultado.config(text=mensaje_general)



def seleccionar_ruta_origen():
    ruta_origen = filedialog.askdirectory()
    entry_origen.delete(0, tk.END)
    entry_origen.insert(0, ruta_origen)


def seleccionar_ruta_destino():
    ruta_destino = filedialog.askdirectory()
    entry_destino.delete(0, tk.END)
    entry_destino.insert(0, ruta_destino)


def copiar_fotos():
    ruta_origen = entry_origen.get()
    ruta_destino = entry_destino.get()

    label_resultado.config(text="")  # Limpiar el texto antes de cada operación

    try:
        operacionFotos(ruta_origen, ruta_destino, label_resultado, ventana, 'copiar')
        messagebox.showinfo("Éxito", "Copia exitosa")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")


def mover_fotos():
    ruta_origen = entry_origen.get()
    ruta_destino = entry_destino.get()

    label_resultado.config(text="")  # Limpiar el texto antes de cada operación

    try:
        operacionFotos(ruta_origen, ruta_destino, label_resultado, ventana, 'mover')
        messagebox.showinfo("Éxito", "Movimiento exitoso")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("FotoCopy by Ivan Pedron")
ruta_icono = "logo.png"  # Reemplaza con la ruta de tu propio archivo .png
img = tk.PhotoImage(file=ruta_icono)
ventana.iconphoto(True, img)

# Configurar el tamaño de la ventana
ventana.geometry("500x300")
ventana.minsize(500, 300)
ventana.maxsize(500, 300)

# Widgets
label_origen = tk.Label(ventana, text="Ruta de origen:")
label_origen.pack(pady=5)

entry_origen = tk.Entry(ventana, width=40)
entry_origen.pack(pady=5)

button_origen = tk.Button(ventana, text="Seleccionar", command=seleccionar_ruta_origen)
button_origen.pack(pady=5)

label_destino = tk.Label(ventana, text="Ruta de destino:")
label_destino.pack(pady=5)

entry_destino = tk.Entry(ventana, width=40)
entry_destino.pack(pady=5)

button_destino = tk.Button(ventana, text="Seleccionar", command=seleccionar_ruta_destino)
button_destino.pack(pady=5)

# Contenedor Frame para los botones de operaciones
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=5)

button_copiar = tk.Button(frame_botones, text="Copiar Fotos", command=copiar_fotos)
button_copiar.pack(side=tk.LEFT, padx=5)

button_mover = tk.Button(frame_botones, text="Mover Fotos", command=mover_fotos)
button_mover.pack(side=tk.LEFT, padx=5)

# Label para mostrar mensajes
label_resultado = tk.Label(ventana, text="", font=("Arial", 10), wraplength=450)
label_resultado.pack(pady=10)

# Iniciar el bucle de eventos
ventana.mainloop()
