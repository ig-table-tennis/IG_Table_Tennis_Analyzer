# ==========================================
# widgets/entrada.py
# Entrada de jugadas
# ==========================================

from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
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

    @staticmethod
    def crear_titulo():

        titulo = Label(
            text="IG Table Tennis Analyzer",
            font_name="fonts/Hand-Bold.ttf",
            size_hint=(1, None),
            height=dp(45),
            font_size="22sp",
            halign="center",
            valign="bottom",
            padding_y=dp(0)
        )

        titulo.bind(
            size=lambda w, s: setattr(
                w,
                "text_size",
                w.size
            )
        )

        return titulo

    # ==================================

    @staticmethod
    def crear_botones_inferiores(app):

        fila = BoxLayout(
            size_hint=(1, None),
            height=dp(60),
            spacing=dp(8)
        )

        # ==================================
        # FONDO DE LA FILA INFERIOR
        # ==================================

        with fila.canvas.before:

            from kivy.graphics import Color, Rectangle

            Color(
                0.15,
                0.15,
                0.15,
                1
            )

            fondo = Rectangle(
                pos=fila.pos,
                size=fila.size
            )

            fila.bind(
                pos=lambda w, v: setattr(
                    fondo,
                    "pos",
                    w.pos
                ),
                size=lambda w, v: setattr(
                    fondo,
                    "size",
                    w.size
                )
            )

        # ==================================
        # BOTONES
        # ==================================

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
