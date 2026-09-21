[app]

# ==========================================================
# DATOS DE LA APLICACIÓN
# ==========================================================

title = IG Table Tennis Analyzer
package.name = igtabletennisanalyzer
package.domain = com.igtabletennis

source.dir = .
source.main = main.py

version = 1.0.0


# ==========================================================
# ARCHIVOS QUE SE INCLUIRÁN EN EL APK
# ==========================================================

source.include_exts = py,png,jpg,jpeg,kv,atlas,wav,ttf,db


# ==========================================================
# CARPETAS QUE NO SE DEBEN INCLUIR
# ==========================================================

source.exclude_dirs = __pycache__,.kivy,bin,COPIA IG_Table_Tennis_Analyzer,Antiguo IG_Table_Tennis_Analyzer


# ==========================================================
# DEPENDENCIAS
# ==========================================================

requirements = python3,kivy


# ==========================================================
# ORIENTACIÓN
# ==========================================================

orientation = landscape


# ==========================================================
# ANDROID
# ==========================================================

fullscreen = 0

android.api = 35
android.minapi = 21
android.ndk = 27c
android.archs = arm64-v8a


# ==========================================================
# ICONO
# ==========================================================

icon.filename = icons/pala.png

# ==========================================================
# CONFIGURACIÓN DE BUILD
# ==========================================================

[buildozer]

log_level = 2
warn_on_root = 1
