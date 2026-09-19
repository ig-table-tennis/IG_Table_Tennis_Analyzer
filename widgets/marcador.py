# ==========================================
# widgets/marcador.py
# Marcador de IG Table Tennis Analyzer
# ==========================================

from kivy.uix.label import Label
from kivy.metrics import dp


class Marcador(Label):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        
        self.font_name = "fonts/NotoSans-SemiBold.ttf"

        self.markup = True

        self.size_hint = (1, None)

        self.height = dp(90)

        self.halign = "right"

        self.valign = "middle"

        self.bind(
            size=self._actualizar_text_size
        )

        self.actualizar(0, 0, 0, 0)

    # ==================================

    def _actualizar_text_size(self, instancia, valor):

        self.text_size = valor

    # ==================================

    def actualizar(
        self,
        tantoA,
        tantoB,
        juegoA,
        juegoB
    ):

        # Determinar quién va por delante en                   juegos
        if juegoA > juegoB:
            juegosA = (
                f"[color=ffff00][b]{juegoA}[/b][/color]"
            )
            juegosB = str(juegoB)

        elif juegoB > juegoA:
            juegosA = str(juegoA)
            juegosB = (
                f"[color=ffff00][b]{juegoB}[/b][/color]"
            )

        else:
            juegosA = str(juegoA)
            juegosB = str(juegoB)

        self.text = (
            "[b]MARCADOR[/b]\n\n"
            f"Jugador A : {tantoA}     "
            f"Juegos : {juegosA}\n"
            f"Jugador B : {tantoB}     "
            f"Juegos : {juegosB}"
        )

    # ==================================

    def reiniciar(self):

        self.actualizar(0, 0, 0, 0)
