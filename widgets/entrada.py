# ==========================================
# widgets/entrada.py
# Entrada de jugadas
# ==========================================

from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp

from widgets.ig_button import IGButton


class Entrada(TextInput):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.hint_text = "Introduce la jugada..."
        self.multiline = False

        self.size_hint = (1, None)
        self.height = dp(55)

        self.font_size = "20sp"

    # ==================================
    # TÍTULO + BOTÓN AYUDA
    # ==================================

    @staticmethod
    def crear_titulo(app):

        # ------------------------------------------
        # CONTENEDOR PRINCIPAL
        # ------------------------------------------

        contenedor = AnchorLayout(
            size_hint=(1, None),
            height=dp(45)
        )

        # ------------------------------------------
        # CAPA DEL TÍTULO
        # ------------------------------------------

        capa_titulo = AnchorLayout(
            size_hint=(1, 1),
            anchor_x="center",
            anchor_y="top",
            padding=(
                0,
                dp(3),
                dp(45),
                0
            )
        )

        titulo = Label(
            text="IG Table Tennis Analyzer",
            font_name="fonts/Hand-Bold.ttf",
            size_hint=(1, None),
            height=dp(30),
            font_size="22sp",
            halign="center",
            valign="middle"
        )

        titulo.bind(
            size=lambda w, s: setattr(
                w,
                "text_size",
                w.size
            )
        )

        capa_titulo.add_widget(
            titulo
        )

        contenedor.add_widget(
            capa_titulo
        )

        # ------------------------------------------
        # CAPA DEL BOTÓN AYUDA
        # ------------------------------------------

        capa_ayuda = AnchorLayout(
            size_hint=(1, 1),
            anchor_x="right",
            anchor_y="top",
            padding=(
                0,
                dp(40),
                dp(2),
                0
            )
        )

        boton_ayuda = IGButton(
            text="?",
            size_hint=(None, None),
            width=dp(40),
            height=dp(40),
            font_size="22sp"
        )

        boton_ayuda.set_color(
            (0.30, 0.30, 0.30, 1)
        )

        boton_ayuda.bind(
            on_press=app.mostrar_ayuda
        )

        capa_ayuda.add_widget(
            boton_ayuda
        )

        contenedor.add_widget(
            capa_ayuda
        )

        return contenedor

    # ==================================
    # BOTONES INFERIORES
    # ==================================

    @staticmethod
    def crear_botones_inferiores(app):

        fila = BoxLayout(
            size_hint=(1, None),
            height=dp(50),
            spacing=dp(8)
        )

        boton_nueva = IGButton(
            text="Nueva partida"
        )

        boton_borrar = IGButton(
            text="Borrar Pantalla"
        )

        boton_nueva.set_color(
            (0.25, 0.25, 0.25, 1)
        )

        boton_borrar.set_color(
            (0.25, 0.25, 0.25, 1)
        )

        boton_nueva.bind(
            on_press=app.nueva_partida
        )

        boton_borrar.bind(
            on_press=app.borrar
        )

        fila.add_widget(
            boton_nueva
        )

        fila.add_widget(
            boton_borrar
        )

        return fila