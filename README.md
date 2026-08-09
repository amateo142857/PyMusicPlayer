# 🎵 PyMusicPlayer

**Reproductor de música en Python con dos interfaces: Terminal y Tkinter**

---

## 📋 Descripción

PyMusicPlayer es un reproductor de música desarrollado en Python que ofrece **dos versiones** en un solo proyecto:

- **Versión Terminal (CLI)**: Interfaz por consola para usuarios que prefieren la línea de comandos
- **Versión Tkinter (GUI)**: Interfaz gráfica moderna con controles visuales

Ambas versiones comparten el mismo motor de reproducción basado en **Pygame** y ofrecen funcionalidades completas.

---

## 🎯 Características

### Funcionalidades Comunes
- 🎵 Reproducción de archivos MP3, WAV y OGG
- 📂 Carga de carpetas completas o archivos individuales
- 🔁 Reproducción en bucle automático
- ⏸️ Pausa/Reanudación
- ⏭️ Navegación entre canciones (Siguiente/Anterior)
- 🛑 Detener reproducción
- 🔊 Control de volumen (0% - 100%)

### Versión Tkinter (GUI)
- 🖥️ Interfaz gráfica moderna y oscura
- 📋 Lista de canciones con doble clic para reproducir
- 📊 Barra de progreso interactiva (clic y arrastre)
- ⏱️ Visualización del tiempo actual y total
- 🎯 Indicador visual de la canción actual
- 🖼️ Icono personalizado

### Versión Terminal (CLI)
- 🎯 Menú interactivo por consola
- 🎵 Lista numerada de canciones
- 🔄 Indicadores visuales de estado
- 🎨 Colores para mejor experiencia (termcolor)

---

## 📦 Requisitos

### Dependencias principales
```bash
pip install pygame termcolor pillow
```

### Dependencias por versión

**Versión Terminal:**
- `pygame`
- `termcolor`

**Versión Tkinter:**
- `pygame`
- `pillow` (PIL)

---

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/amateo142857/PyMusicPlayer.git
cd PyMusicPlayer

# Instalar dependencias
pip install -r requirements.txt
```

---

## 💻 Uso

### Versión Tkinter (GUI)
```bash
python PyMusicPlayer_tkinter.py
```

**Controles:**
- 📂 **Cargar Carpeta**: Selecciona una carpeta con música
- 🎵 **Cargar Archivos**: Selecciona archivos individuales
- ▶️ **Play/Pause**: Reproducir o pausar
- ⏭️ **Siguiente/Anterior**: Navegar canciones
- ⏹️ **Stop**: Detener reproducción
- 🔁 **Bucle**: Activar/Desactivar reproducción en bucle
- 🔊 **Volumen**: Control deslizante
- 📊 **Barra de Progreso**: Haz clic o arrastra para saltar en la canción

### Versión Terminal (CLI)
```bash
python PyMusicPlayer_terminal.py
```

**Controles:**
```
1. 📂 Cargar carpeta de canciones
2. 🎯 Elegir canción específica
3. ▶️  Reproducir/Reanudar
4. ⏸️  Pausar
5. ⏭️  Siguiente canción
6. ⏮️  Canción anterior
7. 🔄 Bucle automático [✅ ACTIVADO]
8. 🔊 Cambiar volumen (0.0 - 1.0)
9. 📋 Mostrar lista de canciones
A. ℹ️  Canción actual
0. 🚪 Salir
```

---

## 📁 Estructura del Proyecto

```
PyMusicPlayer/
├── PyMusicPlayer_tkinter.py   # Versión con interfaz gráfica
├── PyMusicPlayer_terminal.py  # Versión para terminal
├── requirements.txt           # Dependencias
├── README.md                  # Documentación
├── LICENSE                    # Licencia MIT
└── img/
    └── icono.png             # Icono de la aplicación (opcional)
```

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
|------------|-----|
| **Python 3** | Lenguaje base |
| **Pygame** | Motor de audio y eventos |
| **Tkinter** | Interfaz gráfica (GUI) |
| **PIL/Pillow** | Manejo de imágenes (icono) |
| **Termcolor** | Colores en terminal |
| **Threading** | Eventos en segundo plano |

---


## ⚙️ Configuración

### Icono Personalizado
Para agregar un icono a la versión Tkinter:
1. Crea una carpeta `img/` en el directorio raíz
2. Agrega un archivo `icono.png`
3. El programa lo cargará automáticamente

### Formatos Soportados
- ✅ MP3 (MPEG-1 Layer 3)
- ✅ WAV (Waveform Audio)
- ✅ OGG (Ogg Vorbis)

---

## 🐛 Manejo de Errores

- ✅ Archivos corruptos o no soportados
- ✅ Carpetas sin archivos de audio
- ✅ Errores de reproducción
- ✅ Interrupción por teclado (Ctrl+C)
- ✅ Cierre correcto de recursos

---

## 📝 Notas de Desarrollo

### Versión Terminal
- Utiliza hilos para verificar eventos en segundo plano
- Reproducción en bucle mediante eventos de pygame
- Compatible con Windows, Linux y macOS

### Versión Tkinter
- Diseño oscuro moderno
- Barra de progreso con interacción (clic y arrastre)
- Actualización en tiempo real del estado
- Manejo de eventos con `root.after()`

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea tu rama de características (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**Tu Nombre**
- GitHub: [@amateo142857](https://github.com/amateo142857)

---

## 🙏 Agradecimientos

- [Pygame](https://www.pygame.org/) - Motor de audio
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI toolkit
- Comunidad Python por su excelente documentación

---

## ⭐ ¡Dale una estrella!

Si este proyecto te fue útil, considera darle una ⭐ en GitHub.

---

## 📞 Soporte

Si encuentras algún problema, por favor abre un [Issue](https://github.com/amateo142857/PyMusicPlayer/issues).

---

**¡Disfruta tu música! 🎵**