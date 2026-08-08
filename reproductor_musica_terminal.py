import pygame
import os
import time
import glob
import platform
import subprocess
import threading
from termcolor import colored

def limpiar_terminal():
    sistema = platform.system().lower() 
    
    if sistema == "windows":
        subprocess.run('cls', shell=True)
    elif sistema == "linux" or sistema == "darwin":
        subprocess.run('clear', shell=True)
    else:
        # Fallback para otros sistemas
        print("\n" * 100)

# Variables globales
canciones = []
indice_actual = 0
reproduciendo = False
pausada = False
bucle_activo = False

# Inicializar pygame
pygame.mixer.init()
pygame.display.init()
pygame.mixer.music.set_endevent(pygame.USEREVENT)
limpiar_terminal()

# ===== FUNCIÓN PARA VERIFICAR EVENTOS EN SEGUNDO PLANO ===== #
def verificar_eventos():
    global indice_actual, reproduciendo, pausada, bucle_activo
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:  # Canción terminó
                if bucle_activo and canciones and reproduciendo:
                    try:
                        # Pasar a la siguiente canción
                        indice_actual = (indice_actual + 1) % len(canciones)
                        #print("\n" + "="*50)
                        #print("   ⏭️  CAMBIANDO A SIGUIENTE CANCIÓN")
                        #print("="*50)
                        pygame.mixer.music.load(canciones[indice_actual])
                        pygame.mixer.music.play()
                        reproduciendo = True
                        pausada = False
                        nombre = os.path.basename(canciones[indice_actual])
                        #print(f"▶️ Reproduciendo: {nombre}")
                    except Exception as e:
                        print(f"❌ Error al cambiar de canción: {e}")
                        reproduciendo = False
        time.sleep(0.1)  # Pequeña pausa para no saturar la CPU

# ===== FUNCIONES DEL REPRODUCTOR ===== #
def reproducir_cancion(indice):
    global indice_actual, reproduciendo, pausada
    
    if not canciones:
        print("❌ No hay canciones para reproducir")
        return
    
    if indice < 0 or indice >= len(canciones):
        print("❌ Índice fuera de rango")
        return
    
    try:
        # Si es la MISMA canción y está en pausa, solo reanudar
        if indice == indice_actual and pausada:
            pygame.mixer.music.unpause()
            pausada = False
            reproduciendo = True
            nombre = os.path.basename(canciones[indice])
            print(f"▶️ Reanudando: {nombre}")
            return
        
        # Si es una canción DIFERENTE o no está en pausa, cargar desde cero
        pygame.mixer.music.load(canciones[indice])
        pygame.mixer.music.play()
        indice_actual = indice
        reproduciendo = True
        pausada = False
        nombre = os.path.basename(canciones[indice])
        print(f"▶️ Reproduciendo: {nombre}")
        
    except Exception as e:
        print(f"❌ Error al reproducir: {e}")

def seleccionar_cancion_especifica():
    if not canciones:
        limpiar_terminal()
        print("❌ No hay canciones cargadas")
        return
    
    mostrar_lista_canciones()
    try:
        num = int(input("\n📌 Número de canción: ")) - 1
        if 0 <= num < len(canciones):
            limpiar_terminal()
            reproducir_cancion(num)
        else:
            limpiar_terminal()
            print("❌ Número inválido")
    except ValueError:
        limpiar_terminal()
        print("❌ Debes ingresar un número")

def mostrar_lista_canciones():
    limpiar_terminal()
    if not canciones:
        print("📭 No hay canciones cargadas")
        return
    
    print("\n🎵 LISTA DE CANCIONES:")
    for i, cancion in enumerate(canciones):
        nombre = os.path.basename(cancion)  # Solo el nombre del archivo
        indicador = " ▶" if i == indice_actual else ""
        print(f"  {i+1}. {nombre}{indicador}")

def obtener_canciones_de_carpeta(ruta):
    """Busca todos los archivos .mp3 en una carpeta"""
    if not os.path.exists(ruta):
        limpiar_terminal()
        print(f"❌ La carpeta '{ruta}' no existe")
        return []
    
    # Buscar archivos mp3
    archivos = glob.glob(os.path.join(ruta, "*.mp3"))
    archivos += glob.glob(os.path.join(ruta, "*.MP3"))
    
    if not archivos:
        print(f"⚠️ No se encontraron archivos MP3 en '{ruta}'")
        return []
    
    print(f"✅ Encontradas {len(archivos)} canciones en '{ruta}'")
    return archivos

def cargar_carpeta():
    global canciones, indice_actual
    limpiar_terminal()
    ruta = input("📁 Ruta de la carpeta: ").strip()
    
    # Si la ruta tiene comillas, las eliminamos
    ruta = ruta.strip('"').strip("'")
    
    # Si no es una ruta absoluta, la unimos al directorio actual
    if not os.path.isabs(ruta):
        ruta = os.path.join(os.getcwd(), ruta)
    
    nuevas_canciones = obtener_canciones_de_carpeta(ruta)
    if nuevas_canciones:
        canciones = nuevas_canciones
        indice_actual = 0
        print(f"✅ Cargadas {len(canciones)} canciones")
        mostrar_lista_canciones()
    else:
        print("❌ No se pudo cargar la carpeta")

def main():
    global indice_actual, pausada, reproduciendo, bucle_activo
    
    # ===== INICIAR HILO DE VERIFICACIÓN DE EVENTOS ===== #
    hilo_eventos = threading.Thread(target=verificar_eventos, daemon=True)
    hilo_eventos.start()
    
    try:
        while True:
            # ===== MOSTRAR MENÚ =====
            print("\n" + "="*50)
            print("   🎵 REPRODUCTOR DE MÚSICA ")
            print("="*50)
            print("1. 📂 Cargar carpeta de canciones")
            print("2. 🎯 Elegir canción específica")
            print("3. ▶️  Reproducir/Reanudar")
            print("4. ⏸️  Pausar")
            print("5. ⏭️  Siguiente canción")
            print("6. ⏮️  Canción anterior")
            
            # Mostrar estado del bucle en el menú
            estado_bucle = "✅ ACTIVADO" if bucle_activo else "❌ DESACTIVADO"
            print(f"7. 🔄 Bucle automático [{estado_bucle}]")
            
            print("8. 🔊 Cambiar volumen (0.0 - 1.0)")
            print("9. 📋 Mostrar lista de canciones")
            print("A. ℹ️  Canción actual")
            print("0. 🚪 Salir")
            print("-"*50)
            
            if canciones:
                actual = os.path.basename(canciones[indice_actual])
                # Mostrar estado de reproducción
                if pygame.mixer.music.get_busy():
                    estado_reprod = "▶️ Reproduciendo"
                elif pausada:
                    estado_reprod = "⏸️ Pausado"
                else:
                    estado_reprod = "⏹️ Detenido"
                print(f"🎯 Actual: {actual} - {estado_reprod}")
            else:
                print("🎯 Sin canciones cargadas")
            print("="*50)

            opcion = input("👉 Elige una opción: ").strip()

            if opcion == "1":
                cargar_carpeta()
            elif opcion == "2":
                seleccionar_cancion_especifica()
            elif opcion == "3":
                if not canciones:
                    limpiar_terminal()
                    print("❌ Primero carga una carpeta (opción 1)")
                elif pausada:
                    pygame.mixer.music.unpause()
                    pausada = False
                    reproduciendo = True
                    limpiar_terminal()
                    print("▶️ Reanudado")
                elif pygame.mixer.music.get_busy():
                    limpiar_terminal()
                    print("⚠️ Ya está reproduciendo")
                else:
                    limpiar_terminal()
                    reproducir_cancion(indice_actual)
            elif opcion == "4":
                if pygame.mixer.music.get_busy():
                    limpiar_terminal()
                    pygame.mixer.music.pause()
                    pausada = True
                    reproduciendo = False
                    print("⏸️ Pausado")
                else:
                    limpiar_terminal()
                    print("⚠️ No hay música reproduciéndose")
            elif opcion == "5":
                if canciones:
                    indice_actual = (indice_actual + 1) % len(canciones)
                    limpiar_terminal()
                    reproducir_cancion(indice_actual)
                else:
                    limpiar_terminal()
                    print("❌ No hay canciones cargadas")
            elif opcion == "6":
                if canciones:
                    indice_actual = (indice_actual - 1) % len(canciones)
                    limpiar_terminal()
                    reproducir_cancion(indice_actual)
                else:
                    limpiar_terminal()
                    print("❌ No hay canciones cargadas")
            elif opcion == "7":
                bucle_activo = not bucle_activo
                limpiar_terminal()
                estado = "ACTIVADO ✅" if bucle_activo else "DESACTIVADO ❌"
                print(f"🔄 Bucle automático {estado}")
                time.sleep(1)  # Pausa para ver el mensaje
            elif opcion == "8":
                try:
                    vol = float(input("🔊 Volumen (0.0 a 1.0): "))
                    if 0 <= vol <= 1:
                        pygame.mixer.music.set_volume(vol)
                        limpiar_terminal()
                        print(f"✅ Volumen ajustado a {vol}")
                    else:
                        print("❌ El volumen debe estar entre 0.0 y 1.0")
                except ValueError:
                    print("❌ Ingresa un número válido")
            elif opcion == "9":
                mostrar_lista_canciones()
            elif opcion.lower() == "a":
                if canciones:
                    limpiar_terminal()
                    nombre = os.path.basename(canciones[indice_actual])
                    if pygame.mixer.music.get_busy():
                        estado = "▶️ Reproduciendo"
                    elif pausada:
                        estado = "⏸️ Pausado"
                    else:
                        estado = "⏹️ Detenido"
                    print(f"🎵 {nombre} - {estado}")
                else:
                    limpiar_terminal()
                    print("❌ No hay canciones cargadas")
            elif opcion == "0":
                print(colored("\n\nSaliendo del programa ....","red"))
                pygame.mixer.music.stop()
                break
            else:
                limpiar_terminal()
                print("❌ Opción no válida")
            
            time.sleep(0.1)

    except KeyboardInterrupt:
        print(colored("\n\nSaliendo del programa ....","red"))

if __name__ == '__main__':
    main()