import customtkinter as ctk
from tkinter import PhotoImage
from PIL import Image, ImageTk

# Configuracion:
azulOscuro = "#053B50"
azulRegular = "#176B87"
azulClaro = "#64CCC5"
blanco = "#EEEEEE"
negro = "#010101"
gris = "#343638"
negro2 = "#292727"

proyecto = ctk.CTk()

ancho_ventana = 800; alto_ventana = 600
ancho_pantalla = proyecto.winfo_screenwidth()
alto_pantalla = proyecto.winfo_screenheight()
pos_x = (ancho_pantalla // 2) - (ancho_ventana // 2)
pos_y = (alto_pantalla // 2) - (alto_ventana // 2)

proyecto.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")
proyecto.resizable(False, False)
proyecto.config(bg=negro)

# Titulo:
titulo = ctk.CTkLabel(proyecto, text="RED DE DATOS CORPORATIVA", font=("Arial", 40, "bold"), text_color=blanco, fg_color=negro)
titulo.place(relx=0.5, rely=0.1, anchor='center')

# Imagen principal
imagen = Image.open("imagen_main.png")  # Reemplaza con la ruta a tu imagen
imagen = imagen.resize((300, 200), Image.LANCZOS)  # Ajusta el tamaño según sea necesario
imagen_main = ImageTk.PhotoImage(imagen)
imagen_label = ctk.CTkLabel(proyecto, image=imagen_main, text="")
imagen_label.place(relx=0.5, rely=0.35, anchor='center')

# Label de Integrantes:
frame_integrantes = ctk.CTkFrame(proyecto, width=350, height=170, border_color=azulRegular, border_width=3, fg_color=negro)
frame_integrantes.place(relx=0.28, rely=0.55)

label_integrantes = ctk.CTkLabel(frame_integrantes, text="INTEGRANTES", font=('Arial', 28, "bold"), text_color=blanco)
label_integrantes.place(relx=0.22, y=20)

frame_lista_integrantes = ctk.CTkFrame(frame_integrantes, width=350, height=100, border_color=azulRegular, border_width=3, fg_color=negro)
frame_lista_integrantes.place(y=70)

integrante1 = ctk.CTkLabel(frame_integrantes, text="« Andre Gabriel Valverde Mozo »", font=("Arial", 17, "bold"), text_color=blanco, width=220)
integrante1.place(x=42, y=80)

integrante2 = ctk.CTkLabel(frame_integrantes, text="« Piero Gonzalo Delgado Corrales »", font=("Arial", 17, "bold"), text_color=blanco, width=220)
integrante2.place(x=32, y=105)

integrante3 = ctk.CTkLabel(frame_integrantes, text="« Sebastián Roberto Paredes Puente »", font=("Arial", 17, "bold"), text_color=blanco, width=220)
integrante3.place(x=22, y=130)

# Función para abrir la nueva ventana
def abrir_ventana_grafo_completo():
    nueva_ventana = ctk.CTkToplevel(proyecto)
    nueva_ventana.geometry("1000x800")
    nueva_ventana.resizable(False, False)
    nueva_ventana.grab_set()
    
    # Cargar y mostrar la imagen del grafo completo
    imagen_grafo = Image.open("grafo_principal.png")
    imagen_grafo = imagen_grafo.resize((1000, 800), Image.LANCZOS)
    imagen_grafo_ctk = ctk.CTkImage(light_image=imagen_grafo, size=(1000, 800))
    
    label_imagen_grafo = ctk.CTkLabel(nueva_ventana, image=imagen_grafo_ctk, text="")
    label_imagen_grafo.pack()


# Botones
boton_grafo_completo = ctk.CTkButton(proyecto, text="Grafo Completo", width=200, height=50, font=("Arial", 15, "bold"), command=abrir_ventana_grafo_completo)
boton_grafo_completo.place(relx=0.25, rely=0.9, anchor='center')

boton_grafo_muestral = ctk.CTkButton(proyecto, text="Grafo Muestral", width=200, height=50, font=("Arial", 20, "bold"))
boton_grafo_muestral.place(relx=0.75, rely=0.9, anchor='center')



proyecto.mainloop()