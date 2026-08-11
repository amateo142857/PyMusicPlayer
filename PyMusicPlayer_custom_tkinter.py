import pygame
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import time
import threading
from PIL import Image, ImageTk
import tkinter as tk

# ===== CONFIGURACIÓN DE TEMA =====
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ===== VARIABLES GLOBALES =====
canciones = []
indice_actual = 0
reproduciendo = False
pausada = False
bucle_activo = False
duracion_total = 0
tiempo_inicio = 0
posicion_arrastre = 0

# Variables de la interfaz
root = None
lista_canciones = None
btn_play = None
barra_progreso = None
label_tiempo_actual = None
label_tiempo_total = None
label_cancion_actual = None
slider_volumen = None
label_volumen_valor = None

# ===== FUNCIONES DE INICIALIZACIÓN =====
def inicializar_pygame():
    pygame.mixer.init()
    pygame.display.init()
    pygame.mixer.music.set_endevent(pygame.USEREVENT)

def iniciar_hilo_eventos():
    def verificar_eventos():
        global bucle_activo, canciones, indice_actual
        while True:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if bucle_activo and canciones:
                        root.after(0, cancion_siguiente)
            time.sleep(0.1)
    
    hilo = threading.Thread(target=verificar_eventos, daemon=True)
    hilo.start()

# ===== FUNCIONES DE CARGA =====
def cargar_carpeta():
    global canciones
    carpeta = filedialog.askdirectory(title="Seleccionar carpeta de música")
    
    if carpeta:
        canciones = []
        for archivo in os.listdir(carpeta):
            if archivo.lower().endswith(('.mp3', '.wav', '.ogg')):
                canciones.append(os.path.join(carpeta, archivo))
        
        if canciones:
            actualizar_lista()
            messagebox.showinfo("Éxito", f"Se cargaron {len(canciones)} canciones")
        else:
            messagebox.showwarning("Sin canciones", "No se encontraron archivos de música en la carpeta")

def cargar_archivos():
    global canciones
    archivos = filedialog.askopenfilenames(
        title="Seleccionar archivos de música",
        filetypes=[("Archivos de audio", "*.mp3 *.wav *.ogg"), ("Todos los archivos", "*.*")]
    )
    if archivos:
        canciones = list(archivos)
        actualizar_lista()
        messagebox.showinfo("Éxito", f"Se cargaron {len(canciones)} canciones")

def actualizar_lista():
    lista_canciones.delete(0, ctk.END)
    for cancion in canciones:
        nombre = os.path.basename(cancion)
        lista_canciones.insert(ctk.END, nombre)

# ===== FUNCIONES DE REPRODUCCIÓN =====
def reproducir_seleccion(event=None):
    if lista_canciones.curselection():
        indice = lista_canciones.curselection()[0]
        reproducir_cancion(indice)

def reproducir_cancion(indice):
    global indice_actual, reproduciendo, pausada, duracion_total, tiempo_inicio
    
    try:
        cancion = canciones[indice]
        pygame.mixer.music.load(cancion)
        pygame.mixer.music.play()
        indice_actual = indice
        reproduciendo = True
        pausada = False
        tiempo_inicio = time.time()
        btn_play.configure(text="⏸️")
        
        duracion_total = pygame.mixer.Sound(cancion).get_length()
        label_tiempo_total.configure(text=formatear_tiempo(duracion_total))
        
        nombre = os.path.basename(cancion)
        label_cancion_actual.configure(text=f"🎵 {nombre}")
        
        lista_canciones.selection_clear(0, ctk.END)
        lista_canciones.selection_set(indice)
        lista_canciones.see(indice)
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo reproducir la canción: {e}")

def play_pause():
    global reproduciendo, pausada, tiempo_inicio
    
    if not canciones:
        messagebox.showwarning("Sin canciones", "Primero carga canciones")
        return
    
    if reproduciendo and not pausada:
        pygame.mixer.music.pause()
        pausada = True
        btn_play.configure(text="▶️")
    elif pausada:
        pygame.mixer.music.unpause()
        pausada = False
        tiempo_inicio = time.time() - (pygame.mixer.music.get_pos() / 1000)
        btn_play.configure(text="⏸️")
    else:
        reproducir_cancion(indice_actual)

def cancion_siguiente():
    global indice_actual
    if canciones:
        indice_actual = (indice_actual + 1) % len(canciones)
        reproducir_cancion(indice_actual)

def cancion_anterior():
    global indice_actual
    if canciones:
        indice_actual = (indice_actual - 1) % len(canciones)
        reproducir_cancion(indice_actual)

def stop():
    global reproduciendo, pausada
    pygame.mixer.music.stop()
    reproduciendo = False
    pausada = False
    btn_play.configure(text="▶️")
    barra_progreso.set(0)
    label_tiempo_actual.configure(text="00:00")
    label_cancion_actual.configure(text="🎵 Detenido")

def toggle_bucle():
    global bucle_activo
    bucle_activo = not bucle_activo

def cambiar_volumen(valor):
    vol = float(valor)
    pygame.mixer.music.set_volume(vol)
    label_volumen_valor.configure(text=f"{int(vol * 100)}%")

# ===== FUNCIONES DE PROGRESO =====
def actualizar_progreso():
    global duracion_total, reproduciendo, pausada, tiempo_inicio
    
    if reproduciendo and not pausada:
        if pygame.mixer.music.get_busy():
            pos = time.time() - tiempo_inicio
            if duracion_total > 0:
                progreso = pos / duracion_total
                barra_progreso.set(min(progreso, 1.0))
                label_tiempo_actual.configure(text=formatear_tiempo(pos))
    
    root.after(500, actualizar_progreso)

def formatear_tiempo(segundos):
    minutos = int(segundos // 60)
    segs = int(segundos % 60)
    return f"{minutos:02d}:{segs:02d}"

# ===== FUNCIONES PARA LA BARRA DE PROGRESO =====
def on_barra_click(event):
    global duracion_total, reproduciendo, pausada, tiempo_inicio
    
    if not canciones or not reproduciendo:
        return
    
    x = event.x
    ancho = barra_progreso.winfo_width()
    
    if ancho > 0 and duracion_total > 0:
        progreso = x / ancho
        nueva_posicion = duracion_total * progreso
        
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            pygame.mixer.music.play(start=nueva_posicion)
            tiempo_inicio = time.time() - nueva_posicion
            if pausada:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
            
            barra_progreso.set(min(progreso, 1.0))
            label_tiempo_actual.configure(text=formatear_tiempo(nueva_posicion))

def on_barra_drag(event):
    global duracion_total, posicion_arrastre
    
    if not canciones or not reproduciendo:
        return
    
    x = event.x
    ancho = barra_progreso.winfo_width()
    
    if ancho > 0 and duracion_total > 0:
        progreso = x / ancho
        posicion_arrastre = duracion_total * progreso
        
        barra_progreso.set(min(progreso, 1.0))
        label_tiempo_actual.configure(text=formatear_tiempo(posicion_arrastre))

def on_barra_release(event):
    global posicion_arrastre, duracion_total, pausada, tiempo_inicio
    
    if not canciones or not reproduciendo:
        return
    
    if pygame.mixer.music.get_busy() and posicion_arrastre > 0:
        pygame.mixer.music.pause()
        pygame.mixer.music.play(start=posicion_arrastre)
        tiempo_inicio = time.time() - posicion_arrastre
        if pausada:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        
        progreso = posicion_arrastre / duracion_total
        barra_progreso.set(min(progreso, 1.0))
        label_tiempo_actual.configure(text=formatear_tiempo(posicion_arrastre))

# ===== FUNCIÓN DE CIERRE =====
def cerrar():
    pygame.mixer.music.stop()
    pygame.quit()
    root.destroy()

# ===== CONSTRUIR INTERFAZ CON CUSTOMTKINTER =====
def crear_interfaz():
    global root, lista_canciones, btn_play, barra_progreso
    global label_tiempo_actual, label_tiempo_total, label_cancion_actual
    global slider_volumen, label_volumen_valor
    
    root = ctk.CTk()
    root.title("Reproductor de Música")
    root.geometry("900x700")
    
    #Establecer tamaño mínimo para que siempre se vean los controles
    root.minsize(700, 500)  # Ancho mínimo 700, Alto mínimo 500
    
    root.resizable(True, True)
    
    # Configurar colores
    color_fondo = "#1a1a2e"
    color_frame = "#16213e"
    color_boton = "#0f3460"
    color_hover = "#1a4f8a"
    
    # ===== FRAME PRINCIPAL =====
    frame_principal = ctk.CTkFrame(root, fg_color=color_fondo)
    frame_principal.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)
    
    # ===== FRAME SUPERIOR (Título) =====
    frame_titulo = ctk.CTkFrame(frame_principal, fg_color=color_frame, corner_radius=15)
    frame_titulo.pack(fill=ctk.X, padx=10, pady=(0, 15))
    
    titulo_label = ctk.CTkLabel(
        frame_titulo,
        text="🎶 Reproductor de Música",
        font=ctk.CTkFont(size=24, weight="bold"),
        text_color="#e94560"
    )
    titulo_label.pack(pady=15)

    # ===== ICONO DE LA VENTANA ===== #
    try:
        icono1 = Image.open("img/icono.png")
        icono_ventana = ImageTk.PhotoImage(icono1)
        root.iconphoto(False, icono_ventana)
    except:
        pass  

    # ===== FRAME DE BOTONES SUPERIORES =====
    frame_superior = ctk.CTkFrame(frame_principal, fg_color=color_frame, corner_radius=15)
    frame_superior.pack(fill=ctk.X, padx=10, pady=(0, 15))
    
    # Botón cargar carpeta
    btn_cargar_carpeta = ctk.CTkButton(
        frame_superior,
        text="📂 Cargar Carpeta",
        command=cargar_carpeta,
        fg_color=color_boton,
        hover_color=color_hover,
        font=ctk.CTkFont(size=14, weight="bold"),
        corner_radius=10,
        height=40,
        width=150
    )
    btn_cargar_carpeta.pack(side=ctk.LEFT, padx=10, pady=10)
    
    # Botón cargar archivos
    btn_cargar_archivos = ctk.CTkButton(
        frame_superior,
        text="🎵 Cargar Archivos",
        command=cargar_archivos,
        fg_color=color_boton,
        hover_color=color_hover,
        font=ctk.CTkFont(size=14, weight="bold"),
        corner_radius=10,
        height=40,
        width=150
    )
    btn_cargar_archivos.pack(side=ctk.LEFT, padx=10, pady=10)
    
    # Switch de bucle
    frame_bucle = ctk.CTkFrame(frame_superior, fg_color="transparent")
    frame_bucle.pack(side=ctk.RIGHT, padx=20, pady=10)
    
    bucle_switch = ctk.CTkSwitch(
        frame_bucle,
        text="🔁 Bucle",
        command=toggle_bucle,
        font=ctk.CTkFont(size=14, weight="bold"),
        progress_color="#e94560",
        fg_color="#404040",
        onvalue=True,
        offvalue=False
    )
    bucle_switch.pack()
    
    # ===== FRAME DE LISTA =====
    frame_lista = ctk.CTkFrame(frame_principal, fg_color=color_frame, corner_radius=15)
    
    frame_lista.pack(fill=ctk.BOTH, expand=True, padx=10, pady=(0, 15))
    
    # Label para la lista
    label_lista = ctk.CTkLabel(
        frame_lista,
        text="📋 Lista de Reproducción",
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color="#e94560"
    )
    label_lista.pack(pady=(10, 5))
    
    # Listbox personalizada con altura limitada
    lista_canciones = tk.Listbox(
        frame_lista,
        bg="#1a1a2e",
        fg="white",
        selectbackground="#e94560",
        selectforeground="white",
        font=("Segoe UI", 11),
        height=12,  
        relief="flat",
        highlightthickness=1,
        highlightcolor="#e94560"
    )
    lista_canciones.pack(fill=ctk.BOTH, expand=True, padx=10, pady=(0, 10))
    
    lista_canciones.bind("<Double-Button-1>", reproducir_seleccion)
    
    # ===== FRAME DE CANCIÓN ACTUAL =====
    frame_info = ctk.CTkFrame(frame_principal, fg_color=color_frame, corner_radius=15)
    frame_info.pack(fill=ctk.X, padx=10, pady=(0, 15))
    
    label_cancion_actual = ctk.CTkLabel(
        frame_info,
        text="🎵 Sin canción seleccionada",
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color="#a0a0a0"
    )
    label_cancion_actual.pack(pady=15)
    
    # ===== FRAME DE PROGRESO Y TIEMPOS =====
    frame_progreso = ctk.CTkFrame(frame_principal, fg_color=color_frame, corner_radius=15)
    frame_progreso.pack(fill=ctk.X, padx=10, pady=(0, 15))
    
    # Barra de progreso
    barra_progreso = ctk.CTkProgressBar(
        frame_progreso,
        orientation="horizontal",
        progress_color="#e94560",
        fg_color="#404040",
        height=8,
        corner_radius=4
    )
    barra_progreso.pack(fill=ctk.X, padx=15, pady=(15, 5))
    barra_progreso.set(0.0)
    
    # Frame de tiempos
    frame_tiempos = ctk.CTkFrame(frame_progreso, fg_color="transparent")
    frame_tiempos.pack(fill=ctk.X, padx=15, pady=(0, 10))
    
    label_tiempo_actual = ctk.CTkLabel(
        frame_tiempos,
        text="00:00",
        font=ctk.CTkFont(size=12),
        text_color="#a0a0a0"
    )
    label_tiempo_actual.pack(side=ctk.LEFT)
    
    label_tiempo_total = ctk.CTkLabel(
        frame_tiempos,
        text="00:00",
        font=ctk.CTkFont(size=12),
        text_color="#a0a0a0"
    )
    label_tiempo_total.pack(side=ctk.RIGHT)
    
    # Eventos para la barra de progreso
    barra_progreso.bind("<Button-1>", on_barra_click)
    #barra_progreso.bind("<B1-Motion>", on_barra_drag)
    #barra_progreso.bind("<ButtonRelease-1>", on_barra_release)
    
    # ===== FRAME DE CONTROLES =====
    frame_controles = ctk.CTkFrame(frame_principal, fg_color=color_frame, corner_radius=15)
    frame_controles.pack(fill=ctk.X, padx=10, pady=(0, 15))
    
    # Botones de control
    frame_botones = ctk.CTkFrame(frame_controles, fg_color="transparent")
    frame_botones.pack(side=ctk.LEFT, padx=20, pady=10)
    
    def crear_boton(texto, comando, size=16):
        return ctk.CTkButton(
            frame_botones,
            text=texto,
            command=comando,
            fg_color=color_boton,
            hover_color=color_hover,
            font=ctk.CTkFont(size=size, weight="bold"),
            corner_radius=10,
            height=45,
            width=55
        )
    
    btn_anterior = crear_boton("⏮", cancion_anterior)
    btn_anterior.pack(side=ctk.LEFT, padx=5)
    
    btn_play = crear_boton("▶️", play_pause)
    btn_play.pack(side=ctk.LEFT, padx=5)
    
    btn_siguiente = crear_boton("⏭", cancion_siguiente)
    btn_siguiente.pack(side=ctk.LEFT, padx=5)
    
    btn_stop = crear_boton("⏹", stop)
    btn_stop.pack(side=ctk.LEFT, padx=5)
    
    # ===== VOLUMEN =====
    frame_volumen = ctk.CTkFrame(frame_controles, fg_color="transparent")
    frame_volumen.pack(side=ctk.RIGHT, padx=20, pady=10)
    
    label_volumen_icon = ctk.CTkLabel(
        frame_volumen,
        text="🔊",
        font=ctk.CTkFont(size=18)
    )
    label_volumen_icon.pack(side=ctk.LEFT, padx=5)
    
    slider_volumen = ctk.CTkSlider(
        frame_volumen,
        from_=0,
        to=1,
        orientation="horizontal",
        command=cambiar_volumen,
        progress_color="#e94560",
        fg_color="#404040",
        width=120,
        height=6
    )
    slider_volumen.pack(side=ctk.LEFT, padx=10)
    slider_volumen.set(0.7)
    
    label_volumen_valor = ctk.CTkLabel(
        frame_volumen,
        text="70%",
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color="#e94560"
    )
    label_volumen_valor.pack(side=ctk.LEFT, padx=5)
    
    # ===== INICIALIZAR =====
    inicializar_pygame()
    iniciar_hilo_eventos()
    actualizar_progreso()
    
    root.protocol("WM_DELETE_WINDOW", cerrar)
    
    return root

# ===== EJECUTAR =====
if __name__ == "__main__":
    root = crear_interfaz()
    root.mainloop()