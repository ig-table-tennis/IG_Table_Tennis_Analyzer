🏓 IG Table Tennis Analyzer (IGTTA)

IG Table Tennis Analyzer es una aplicación para el análisis de jugadas de tenis de mesa, desarrollada para registrar y analizar las acciones que ocurren durante un punto mediante un sistema de abreviaturas y zonas de juego.

La aplicación ha sido desarrollada en Python y Kivy y dispone de una versión para Android en formato APK.

---

📱 Aplicación

Nombre: IG Table Tennis Analyzer
Abreviatura: IGTTA
Plataforma: Android
Versión: 1.0.0

La aplicación permite introducir las acciones de una jugada de tenis de mesa y obtener su análisis de forma rápida, facilitando el registro y estudio de los puntos disputados.

---

⚙️ Características

- 🏓 Registro de jugadas de tenis de mesa.
- 📊 Análisis de las acciones realizadas durante cada punto.
- 🎯 Sistema de zonas y colisiones de juego.
- 🏆 Marcador y control de puntuación.
- 🔄 Gestión de nuevas partidas.
- 🗑️ Borrado de la pantalla de análisis.
- 🔊 Efectos de sonido para las diferentes acciones.
- 🎨 Interfaz gráfica personalizada.
- 📱 Aplicación compilada para Android.
- 💾 Base de datos integrada para las acciones y zonas de juego.

---

🛠️ Tecnologías

El proyecto utiliza principalmente:

- Python
- Kivy
- SQLite
- Buildozer
- GitHub Actions

---

📂 Estructura del proyecto

IG_Table_Tennis_Analyzer/
│
├── igtta.py
├── main.py
├── logica.py
├── buildozer.spec
├── colisionables.db
│
├── widgets/
│   ├── entrada.py
│   ├── salida.py
│   ├── marcador.py
│   ├── visor_jugada.py
│   ├── panel_botones.py
│   ├── flow_layout.py
│   └── ig_button.py
│
├── fonts/
│   └── ...
│
├── sounds/
│   └── ...
│
├── *.png
│
└── .github/
    └── workflows/
        └── build-apk.yml

---

📱 Android

La aplicación se compila como APK para dispositivos Android mediante Buildozer y GitHub Actions.

La APK incluye los recursos necesarios para ejecutar la aplicación, incluyendo:

- Código Python.
- Base de datos.
- Fuentes.
- Sonidos.
- Imágenes y recursos gráficos.

---

🧪 Estado del proyecto

Versión 1.0.0 — Finalizada

El desarrollo de la versión actual de IG Table Tennis Analyzer ha finalizado y la aplicación ha sido compilada y probada en Android.

---

👨‍💻 Autor

Iván Gutiérrez

Proyecto desarrollado para el análisis y registro de jugadas de tenis de mesa.

---

© Copyright

Copyright (c) 2026 Iván Gutiérrez.

Todos los derechos reservados.

El código fuente original de IG Table Tennis Analyzer (IGTTA), así como los materiales originales creados por el autor, no pueden ser copiados, modificados, redistribuidos ni utilizados con fines comerciales sin autorización previa y por escrito del autor.

El repositorio público permite consultar el proyecto, pero dicha publicación no concede una licencia para reutilizar, modificar o redistribuir el código.

Los componentes de terceros incluidos o utilizados por el proyecto permanecen sujetos a sus respectivas licencias y derechos de autor.

Para más información, consulta el archivo ""LICENSE"" (LICENSE).

---

🏓 IG Table Tennis Analyzer

IGTTA — Table Tennis Analysis

© 2026 Iván Gutiérrez. All rights reserved.
