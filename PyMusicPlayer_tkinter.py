import pygame
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import time
import threading
from PIL import Image, ImageTk

# ===== VARIABLES GLOBALES =====
canciones = []
indice_actual = 0
reproduciendo = False
pausada = False
bucle_activo = False
duracion_total = 0
tiempo_inicio = 0
posicion_arrastre = 0  # ← INICIALIZADA

# Variables de la interfaz
root = None
lista_canciones = None
btn_play = None
barra_progreso = None
label_tiempo_actual = None
label_tiempo_total = None
label_cancion_actual = None
volumen_var = None
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
    lista_canciones.delete(0, tk.END)
    for cancion in canciones:
        nombre = os.path.basename(cancion)
        lista_canciones.insert(tk.END, nombre)

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
        btn_play.config(text="⏸️")
        
        duracion_total = pygame.mixer.Sound(cancion).get_length()
        label_tiempo_total.config(text=formatear_tiempo(duracion_total))
        
        nombre = os.path.basename(cancion)
        label_cancion_actual.config(text=f"🎵 {nombre}")
        
        lista_canciones.selection_clear(0, tk.END)
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
        btn_play.config(text="▶️")
    elif pausada:
        pygame.mixer.music.unpause()
        pausada = False
        tiempo_inicio = time.time() - (pygame.mixer.music.get_pos() / 1000)
        btn_play.config(text="⏸️")
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
    btn_play.config(text="▶️")
    barra_progreso['value'] = 0
    label_tiempo_actual.config(text="00:00")
    label_cancion_actual.config(text="🎵 Detenido")

def toggle_bucle():
    global bucle_activo
    bucle_activo = not bucle_activo
    estado = "Activado" if bucle_activo else "Desactivado"
    print(f"🔁 Bucle: {estado}")

def cambiar_volumen(valor):
    vol = float(valor)
    pygame.mixer.music.set_volume(vol)
    label_volumen_valor.config(text=f"{int(vol * 100)}%")

# ===== FUNCIONES DE PROGRESO =====
def actualizar_progreso():
    global duracion_total, reproduciendo, pausada, tiempo_inicio
    
    if reproduciendo and not pausada:
        if pygame.mixer.music.get_busy():
            pos = time.time() - tiempo_inicio
            if duracion_total > 0:
                porcentaje = (pos / duracion_total) * 100
                barra_progreso['value'] = min(porcentaje, 100)
                label_tiempo_actual.config(text=formatear_tiempo(pos))
    
    root.after(500, actualizar_progreso)

def formatear_tiempo(segundos):
    minutos = int(segundos // 60)
    segs = int(segundos % 60)
    return f"{minutos:02d}:{segs:02d}"

# ===== FUNCIONES PARA LA BARRA DE PROGRESO =====
def on_barra_click(event):
    """Saltar a una posición haciendo clic en la barra"""
    global duracion_total, reproduciendo, pausada, tiempo_inicio
    
    if not canciones or not reproduciendo:
        return
    
    x = event.x
    ancho = barra_progreso.winfo_width()
    
    if ancho > 0 and duracion_total > 0:
        porcentaje = x / ancho
        nueva_posicion = duracion_total * porcentaje
        
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            pygame.mixer.music.play(start=nueva_posicion)
            tiempo_inicio = time.time() - nueva_posicion
            if pausada:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
            
            barra_progreso['value'] = porcentaje * 100
            label_tiempo_actual.config(text=formatear_tiempo(nueva_posicion))

def on_barra_drag(event):
    """Arrastrar en la barra de progreso"""
    global duracion_total, posicion_arrastre
    
    if not canciones or not reproduciendo:
        return
    
    x = event.x
    ancho = barra_progreso.winfo_width()
    
    if ancho > 0 and duracion_total > 0:
        porcentaje = x / ancho
        posicion_arrastre = duracion_total * porcentaje
        
        barra_progreso['value'] = min(porcentaje * 100, 100)
        label_tiempo_actual.config(text=formatear_tiempo(posicion_arrastre))

def on_barra_release(event):
    """Soltar el arrastre en la barra"""
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
        
        porcentaje = (posicion_arrastre / duracion_total) * 100
        barra_progreso['value'] = min(porcentaje, 100)
        label_tiempo_actual.config(text=formatear_tiempo(posicion_arrastre))

# ===== FUNCIÓN DE CIERRE =====
def cerrar():
    pygame.mixer.music.stop()
    pygame.quit()
    root.destroy()

# ===== CONSTRUIR INTERFAZ =====
def crear_interfaz():
    global root, lista_canciones, btn_play, barra_progreso
    global label_tiempo_actual, label_tiempo_total, label_cancion_actual
    global volumen_var, label_volumen_valor
    
    root = tk.Tk()
    root.title("Reproductor de Música")
    root.geometry("800x600")
    root.resizable(True, True)
    
    # ===== Icono =====
    try:
        icono1 = Image.open("img/icono.png")
        icono_ventana = ImageTk.PhotoImage(icono1)
        root.iconphoto(False, icono_ventana)
    except:
        pass
    
    # ===== FRAME SUPERIOR =====
    frame_superior = tk.Frame(root, bg="#2c2c2c", pady=10)
    frame_superior.pack(fill=tk.X)
    
    btn_cargar_carpeta = tk.Button(
        frame_superior, 
        text="📂 Cargar Carpeta", 
        command=cargar_carpeta,
        bg="#404040", fg="white",
        font=("Arial", 10, "bold"),
        padx=15, pady=5
    )
    btn_cargar_carpeta.pack(side=tk.LEFT, padx=5)
    
    btn_cargar_archivos = tk.Button(
        frame_superior,
        text="🎵 Cargar Archivos",
        command=cargar_archivos,
        bg="#404040", fg="white",
        font=("Arial", 10, "bold"),
        padx=15, pady=5
    )
    btn_cargar_archivos.pack(side=tk.LEFT, padx=5)
    
    # ===== FRAME DE BUCLE =====
    frame_bucle = tk.Frame(frame_superior, bg="#2c2c2c")
    frame_bucle.pack(side=tk.RIGHT, padx=10)
    
    bucle_var = tk.BooleanVar(value=False)
    btn_bucle = tk.Checkbutton(
        frame_bucle,
        text="🔁 Bucle",
        variable=bucle_var,
        command=toggle_bucle,
        bg="#2c2c2c", fg="white",
        selectcolor="#404040",
        font=("Arial", 10, "bold")
    )
    btn_bucle.pack(side=tk.RIGHT, padx=5)
    
    # ===== LISTA DE CANCIONES =====
    frame_lista = tk.Frame(root)
    frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    scrollbar = tk.Scrollbar(frame_lista)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    lista_canciones = tk.Listbox(
        frame_lista,
        yscrollcommand=scrollbar.set,
        bg="#1e1e1e",
        fg="white",
        selectbackground="#4040ff",
        selectforeground="white",
        font=("Arial", 10),
        height=15
    )
    lista_canciones.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=lista_canciones.yview)
    
    lista_canciones.bind("<Double-Button-1>", reproducir_seleccion)
    
    # ===== FRAME DE CONTROLES =====
    frame_controles = tk.Frame(root, bg="#2c2c2c", pady=10)
    frame_controles.pack(fill=tk.X, padx=10, pady=5)
    
    frame_botones = tk.Frame(frame_controles, bg="#2c2c2c")
    frame_botones.pack(side=tk.LEFT)
    
    btn_anterior = tk.Button(
        frame_botones,
        text="⏮",
        command=cancion_anterior,
        bg="#404040", fg="white",
        font=("Arial", 14),
        width=3
    )
    btn_anterior.pack(side=tk.LEFT, padx=5)
    
    btn_play = tk.Button(
        frame_botones,
        text="▶️",
        command=play_pause,
        bg="#404040", fg="white",
        font=("Arial", 14),
        width=3
    )
    btn_play.pack(side=tk.LEFT, padx=5)
    
    btn_siguiente = tk.Button(
        frame_botones,
        text="⏭",
        command=cancion_siguiente,
        bg="#404040", fg="white",
        font=("Arial", 14),
        width=3
    )
    btn_siguiente.pack(side=tk.LEFT, padx=5)
    
    btn_stop = tk.Button(
        frame_botones,
        text="⏹",
        command=stop,
        bg="#404040", fg="white",
        font=("Arial", 14),
        width=3
    )
    btn_stop.pack(side=tk.LEFT, padx=5)
    
    # ===== VOLUMEN =====
    frame_volumen = tk.Frame(frame_controles, bg="#2c2c2c")
    frame_volumen.pack(side=tk.RIGHT, padx=10)
    
    label_volumen_texto = tk.Label(
        frame_volumen,
        text="🔊",
        bg="#2c2c2c",
        fg="white",
        font=("Arial", 12)
    )
    label_volumen_texto.pack(side=tk.LEFT, padx=5)
    
    volumen_var = tk.DoubleVar(value=0.7)
    slider_volumen = tk.Scale(
        frame_volumen,
        from_=0.0,
        to=1.0,
        orient=tk.HORIZONTAL,
        resolution=0.05,
        variable=volumen_var,
        command=cambiar_volumen,
        bg="#2c2c2c",
        fg="white",
        troughcolor="#404040",
        length=120
    )
    slider_volumen.pack(side=tk.LEFT, padx=5)
    
    label_volumen_valor = tk.Label(
        frame_volumen,
        text="70%",
        bg="#2c2c2c",
        fg="white",
        font=("Arial", 10)
    )
    label_volumen_valor.pack(side=tk.LEFT, padx=5)
    
    # ===== BARRA DE PROGRESO =====
    frame_progreso = tk.Frame(root, bg="#2c2c2c")
    frame_progreso.pack(fill=tk.X, padx=10, pady=5)
    
    barra_progreso = ttk.Progressbar(
        frame_progreso,
        orient=tk.HORIZONTAL,
        length=400,
        mode='determinate'
    )
    barra_progreso.pack(fill=tk.X, padx=5)
    
    barra_progreso.bind("<Button-1>", on_barra_click)
    barra_progreso.bind("<B1-Motion>", on_barra_drag)
    barra_progreso.bind("<ButtonRelease-1>", on_barra_release)
    
    # ===== TIEMPO =====
    frame_tiempo = tk.Frame(root, bg="#2c2c2c")
    frame_tiempo.pack(fill=tk.X, padx=15)
    
    label_tiempo_actual = tk.Label(
        frame_tiempo,
        text="00:00",
        bg="#2c2c2c",
        fg="white",
        font=("Arial", 9)
    )
    label_tiempo_actual.pack(side=tk.LEFT)
    
    label_tiempo_total = tk.Label(
        frame_tiempo,
        text="00:00",
        bg="#2c2c2c",
        fg="white",
        font=("Arial", 9)
    )
    label_tiempo_total.pack(side=tk.RIGHT)
    
    # ===== INFO =====
    frame_info = tk.Frame(root, bg="#2c2c2c", pady=5)
    frame_info.pack(fill=tk.X, padx=10)
    
    label_cancion_actual = tk.Label(
        frame_info,
        text="🎵 Sin canción seleccionada",
        bg="#2c2c2c",
        fg="#a0a0a0",
        font=("Arial", 10, "italic")
    )
    label_cancion_actual.pack()
    
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