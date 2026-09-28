# ==========================================
# widgets/marcador.py
# Marcador de IG Table Tennis Analyzer
# ==========================================

from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.clock import Clock


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

        # ==========================================
        # CONTROL DEL PARPADEO
        # ==========================================

        self._evento_parpadeo = None

        self._jugador_parpadeando = None

        self._juego_parpadeando = None

        self._numero_visible = True

        # ==========================================
        # VALORES DEL MARCADOR
        # ==========================================

        self._tantoA = 0
        self._tantoB = 0

        self._juegoA = 0
        self._juegoB = 0

        # ==========================================
        # MARCADOR INICIAL
        # ==========================================

        self.actualizar(
            0,
            0,
            0,
            0
        )

    # ==========================================
    # ACTUALIZAR TEXT_SIZE
    # ==========================================

    def _actualizar_text_size(
        self,
        instancia,
        valor
    ):

        self.text_size = valor

    # ==========================================
    # ACTUALIZAR MARCADOR
    # ==========================================

    def actualizar(
        self,
        tantoA,
        tantoB,
        juegoA,
        juegoB
    ):

        self._tantoA = tantoA
        self._tantoB = tantoB

        self._juegoA = juegoA
        self._juegoB = juegoB

        self._numero_visible = True

        self._actualizar_texto()

    # ==========================================
    # HACER PARPADEAR EL TANTO DE A
    # ==========================================

    def parpadear_A(self):

        self._iniciar_parpadeo("A")

    # ==========================================
    # HACER PARPADEAR EL TANTO DE B
    # ==========================================

    def parpadear_B(self):

        self._iniciar_parpadeo("B")

    # ==========================================
    # HACER PARPADEAR EL JUEGO DE A
    # ==========================================

    def parpadear_juego_A(self):

        self._iniciar_parpadeo_juego("A")

    # ==========================================
    # HACER PARPADEAR EL JUEGO DE B
    # ==========================================

    def parpadear_juego_B(self):

        self._iniciar_parpadeo_juego("B")

    # ==========================================
    # INICIAR PARPADEO DEL TANTO
    # ==========================================

    def _iniciar_parpadeo(
        self,
        jugador
    ):

        self._detener_evento_parpadeo()

        self._juego_parpadeando = None

        self._jugador_parpadeando = jugador

        self._numero_visible = True

        self._actualizar_texto()

        self._evento_parpadeo = Clock.schedule_interval(
            self._alternar_parpadeo,
            0.30
        )

    # ==========================================
    # INICIAR PARPADEO DEL JUEGO
    # ==========================================

    def _iniciar_parpadeo_juego(
        self,
        jugador
    ):

        self._detener_evento_parpadeo()

        self._jugador_parpadeando = None

        self._juego_parpadeando = jugador

        self._numero_visible = True

        self._actualizar_texto()

        self._evento_parpadeo = Clock.schedule_interval(
            self._alternar_parpadeo,
            0.30
        )

    # ==========================================
    # ALTERNAR PARPADEO
    # ==========================================

    def _alternar_parpadeo(
        self,
        dt
    ):

        if (
            self._jugador_parpadeando is None
            and self._juego_parpadeando is None
        ):

            return

        self._numero_visible = not self._numero_visible

        self._actualizar_texto()

    # ==========================================
    # ACTUALIZAR TEXTO
    # ==========================================

    def _actualizar_texto(self):

        # ==========================================
        # JUEGOS
        # ==========================================

        if self._juegoA > self._juegoB:

            # --------------------------------------
            # JUEGO A PARPADEANDO
            # --------------------------------------

            if (
                self._juego_parpadeando == "A"
                and not self._numero_visible
                and self._juegoA > 0
            ):

                juegosA = (
                    f"[color=000000][b]"
                    f"{self._juegoA}"
                    f"[/b][/color]"
                )

            else:

                juegosA = (
                    f"[color=ffff00][b]"
                    f"{self._juegoA}"
                    f"[/b][/color]"
                )

            juegosB = str(
                self._juegoB
            )

        elif self._juegoB > self._juegoA:

            # --------------------------------------
            # JUEGO B PARPADEANDO
            # --------------------------------------

            juegosA = str(
                self._juegoA
            )

            if (
                self._juego_parpadeando == "B"
                and not self._numero_visible
                and self._juegoB > 0
            ):

                juegosB = (
                    f"[color=000000][b]"
                    f"{self._juegoB}"
                    f"[/b][/color]"
                )

            else:

                juegosB = (
                    f"[color=ffff00][b]"
                    f"{self._juegoB}"
                    f"[/b][/color]"
                )

        else:

            # --------------------------------------
            # JUEGOS EMPATADOS
            # --------------------------------------

            if (
                self._juego_parpadeando == "A"
                and not self._numero_visible
                and self._juegoA > 0
            ):

                juegosA = (
                    f"[color=000000][b]"
                    f"{self._juegoA}"
                    f"[/b][/color]"
                )

            else:

                juegosA = str(
                    self._juegoA
                )

            if (
                self._juego_parpadeando == "B"
                and not self._numero_visible
                and self._juegoB > 0
            ):

                juegosB = (
                    f"[color=000000][b]"
                    f"{self._juegoB}"
                    f"[/b][/color]"
                )

            else:

                juegosB = str(
                    self._juegoB
                )

        # ==========================================
        # TANTO A
        # ==========================================

        if (
            self._jugador_parpadeando == "A"
            and not self._numero_visible
            and self._tantoA > 0
        ):

            tantoA = "[color=000000]1[/color]"

        else:

            tantoA = str(
                self._tantoA
            )

        # ==========================================
        # TANTO B
        # ==========================================

        if (
            self._jugador_parpadeando == "B"
            and not self._numero_visible
            and self._tantoB > 0
        ):

            tantoB = "[color=000000]1[/color]"

        else:

            tantoB = str(
                self._tantoB
            )

        # ==========================================
        # DISEÑO ORIGINAL
        # ==========================================

        self.text = (
            "[b]MARCADOR[/b]\n\n"
            f"Jugador A : {tantoA}     "
            f"Juegos : {juegosA}\n"
            f"Jugador B : {tantoB}     "
            f"Juegos : {juegosB}"
        )

    # ==========================================
    # DETENER ANIMACIÓN
    # ==========================================

    def detener_animacion(self):

        self._jugador_parpadeando = None

        self._juego_parpadeando = None

        self._numero_visible = True

        self._detener_evento_parpadeo()

        self._actualizar_texto()

    # ==========================================
    # DETENER EVENTO
    # ==========================================

    def _detener_evento_parpadeo(self):

        if self._evento_parpadeo is not None:

            self._evento_parpadeo.cancel()

            self._evento_parpadeo = None

    # ==========================================
    # REINICIAR
    # ==========================================

    def reiniciar(self):

        self.detener_animacion()

        self._tantoA = 0
        self._tantoB = 0

        self._juegoA = 0
        self._juegoB = 0

        self.actualizar(
            0,
            0,
            0,
            0
        )