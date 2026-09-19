# ==========================================
# widgets/panel_botones.py
# Panel de botones
# ==========================================

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.metrics import dp

from widgets.ig_button import IGButton


class PanelBotones(BoxLayout):

    def __init__(self, callback, **kwargs):

        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.size_hint = (1, None)
        self.height = dp(145)
        self.spacing = dp(5)

        self.callback = callback

        self.crear_fila(
            (
                ("Jugador\nA", "JA"),
                ("Jugador\nB", "JB"),
                ("Mesa\nA", "MA"),
                ("Mesa\nB", "MB"),
            )
        )

        self.crear_fila(
            (
                ("Red", "R"),
                ("Tapa\nMesa", "TM"),
                ("Base\nPata", "BP"),
                ("ATRÁS", "←"),
            )
        )

        self.crear_fila(
            (
                ("Valla", "V"),
                ("Lateral", "L"),
                ("Suelo", "S"),
                ("C", "C"),
            )
        )

    # ==================================

    def crear_fila(self, datos):

        fila = BoxLayout(
            size_hint=(1, None),
            height=dp(45),
            spacing=dp(5)
        )

        datos = list(datos)

        while len(datos) < 4:
            datos.append(None)

        for info in datos:

            if info is None:

                fila.add_widget(
                    Widget(
                        size_hint_x=1
                    )
                )

                continue

            texto, codigo = info

            if codigo == "←":

                boton = IGButton(
                    text="",
                    codigo=codigo,
                    size_hint_x=1
                )

            else:

                boton = IGButton(
                    text=texto,
                    codigo=codigo,
                    size_hint_x=1
                )

            if codigo == "←":

                boton.set_color(
                    (1, 1, 1, 1)
                )

                boton.set_text_color(
                    (0, 0, 0, 1)
                )

            elif codigo == "C":

                boton.set_color(
                    (1, 1, 1, 1)
                )

                boton.set_text_color(
                    (0, 0, 0, 1)
                )
                
                boton.font_size = "18sp"

            elif codigo in ("JA", "JB"):

                boton.set_color(
                    (1, 1, 0, 1)
                )

                boton.set_text_color(
                    (0, 0, 0, 1)
                )

            elif codigo in ("MA", "MB"):

                boton.set_color(
                    (0, 0.4, 1, 1)
                )

                boton.set_text_color(
                    (1, 1, 1, 1)
                )

            elif codigo == "R":

                boton.set_color(
                    (0, 0.8, 0, 1)
                )

                boton.set_text_color(
                    (1, 1, 1, 1)
                )

            else:

                boton.set_color(
                    (1, 0, 0, 1)
                )

                boton.set_text_color(
                    (1, 1, 1, 1)
                )

            boton.bind(
                on_press=self.pulsado
            )

            fila.add_widget(
                boton
            )

        self.add_widget(
            fila
        )

    # ==================================

    def pulsado(self, boton):

        self.callback(
            boton.codigo
        )
