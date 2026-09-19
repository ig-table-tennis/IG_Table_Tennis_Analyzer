# ==========================================
# widgets/visor_jugada.py
# ==========================================

from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.clock import Clock


class VisorJugada(Label):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # ==========================================
        # CONFIGURACIÓN DEL LABEL
        # ==========================================

        self.markup = True

        self.font_name = "fonts/NotoSans-SemiBold.ttf"
        self.font_size = "18sp"

        self.size_hint = (1, None)
        self.size_hint_y = None

        # Altura de una sola línea.
        self.height = dp(30)

        self.halign = "left"
        self.valign = "top"

        # IMPORTANTE:
        # No dejamos espacio interior.
        self.padding = (0, 0)

        self.color = (0, 0, 0, 1)

        # El ancho se controla desde el ScrollView.
        # La altura queda determinada por el texto.
        self.text_size = (self.width, None)

        # ScrollView que contiene este visor.
        self.scroll = None

        # ==========================================
        # BINDINGS
        # ==========================================

        self.bind(
            width=self._actualizar_ancho,
            texture_size=self._actualizar_altura
        )

    # ==========================================
    # CONECTAR CON EL SCROLLVIEW
    # ==========================================

    def conectar_scroll(self, scroll):

        self.scroll = scroll

    # ==========================================
    # ACTUALIZAR ANCHO
    # ==========================================

    def _actualizar_ancho(self, *args):

        self.text_size = (
            self.width,
            None
        )

    # ==========================================
    # ACTUALIZAR ALTURA
    # ==========================================

    def _actualizar_altura(self, *args):

        # ==========================================
        # LA ALTURA ES EXACTAMENTE LA DEL TEXTO
        # ==========================================

        self.height = max(
            dp(30),
            self.texture_size[1]
        )

        # ==========================================
        # IMPORTANTE
        # ==========================================
        #
        # NO HACEMOS SCROLL AQUÍ.
        #
        # Mientras la jugada ocupe una sola línea,
        # debe permanecer en la primera línea,
        # inmediatamente debajo de:
        #
        # INICIO JUGADA:
        #
        # El ScrollView solamente debe desplazarse
        # cuando el contenido realmente sobrepasa
        # la altura visible.
        #
        # ==========================================

    # ==========================================
    # IR AL FINAL DEL SCROLL
    # ==========================================

    def _ir_al_final(self, *args):

        if self.scroll is None:
            return

        # ==========================================
        # SOLO DESPLAZAR SI HAY DESBORDAMIENTO
        # ==========================================

        if self.height > self.scroll.height:

            self.scroll.scroll_y = 0

    # ==========================================
    # LIMPIAR
    # ==========================================

    def limpiar(self):

        self.text = ""

        self.height = dp(30)

        # Al limpiar no necesitamos desplazar
        # el ScrollView.
        if self.scroll is not None:

            Clock.schedule_once(
                self._comprobar_scroll,
                0
            )

    # ==========================================
    # COMPROBAR SI HAY QUE HACER SCROLL
    # ==========================================

    def _comprobar_scroll(self, *args):

        if self.scroll is None:
            return

        # ==========================================
        # SI EL CONTENIDO CABE, QUEDA ARRIBA
        # ==========================================

        if self.height <= self.scroll.height:

            self.scroll.scroll_y = 1

        # ==========================================
        # SI EL CONTENIDO SOBREPASA EL VISOR,
        # MOSTRAMOS LA PARTE FINAL
        # ==========================================

        else:

            self.scroll.scroll_y = 0

    # ==========================================
    # MOSTRAR JUGADA
    # ==========================================

    def mostrar(
        self,
        cadena,
        posicion_resaltada=None
    ):

        colores = {
            "JA": "ffff00",
            "JB": "ffff00",
            "MA": "0066cc",
            "MB": "0066cc",
            "R": "009900",
            "TM": "ff0000",
            "BP": "ff0000",
            "V": "ff0000",
            "L": "ff0000",
            "S": "ff0000",
        }

        partes = []

        i = 0

        while i < len(cadena):

            # ==================================
            # CÓDIGOS DE DOS CARACTERES
            # ==================================

            if cadena[i:i + 2] in (
                "JA",
                "JB",
                "MA",
                "MB",
                "TM",
                "BP"
            ):

                codigo = cadena[i:i + 2]
                inicio = i

                i += 2

            # ==================================
            # CÓDIGOS DE UN CARÁCTER
            # ==================================

            else:

                codigo = cadena[i]
                inicio = i

                i += 1

            # ==================================
            # RESALTAR POSICIÓN
            # ==================================

            if (
                posicion_resaltada is not None
                and inicio == posicion_resaltada
            ):

                partes.append(
                    f"[color=ff0000]{codigo}[/color]"
                )

            # ==================================
            # COLOR NORMAL
            # ==================================

            else:

                color = colores.get(
                    codigo,
                    "ffffff"
                )

                partes.append(
                    f"[color={color}]{codigo}[/color]"
                )

        # ==========================================
        # MOSTRAR TEXTO
        # ==========================================

        self.text = "".join(partes)

        # ==========================================
        # NO HACER SCROLL TODAVÍA
        # ==========================================
        #
        # Si la jugada acaba de comenzar, permanece
        # en la primera línea.
        #
        # Si el texto aumenta y posteriormente
        # sobrepasa el área visible, entonces
        # comprobamos el scroll.
        #
        # ==========================================

        Clock.schedule_once(
            self._comprobar_scroll,
            0
        )

    # ==========================================
    # MOSTRAR RESULTADO
    # ==========================================

    def mostrar_resultado(
        self,
        cadena,
        correcta,
        posicion_error=None,
        falta_terminar=False
    ):

        partes = []

        i = 0

        while i < len(cadena):

            # ==================================
            # CÓDIGOS DE DOS CARACTERES
            # ==================================

            if cadena[i:i + 2] in (
                "JA",
                "JB",
                "MA",
                "MB",
                "TM",
                "BP"
            ):

                codigo = cadena[i:i + 2]
                inicio = i

                i += 2

            # ==================================
            # CÓDIGOS DE UN CARÁCTER
            # ==================================

            else:

                codigo = cadena[i]
                inicio = i

                i += 1

            # ==================================
            # FALTA TERMINAR
            # ==================================

            if falta_terminar:

                partes.append(
                    f"[color=ffffff]{codigo}[/color]"
                )

            # ==================================
            # ERROR DE SECUENCIA
            # ==================================

            elif not correcta:

                partes.append(
                    f"[color=ffffff]{codigo}[/color]"
                )

            # ==================================
            # ERROR / GOLPE RESALTADO
            # ==================================

            elif (
                posicion_error is not None
                and inicio == posicion_error
            ):

                partes.append(
                    f"[color=ff0000][b]{codigo}[/b][/color]"
                )

            # ==================================
            # NORMAL
            # ==================================

            else:

                partes.append(
                    f"[color=ffffff]{codigo}[/color]"
                )

        # ==========================================
        # CONSTRUIR TEXTO
        # ==========================================

        texto = "".join(partes)

        # ==========================================
        # FALTA TERMINAR
        # ==========================================

        if falta_terminar:

            texto += (
                "[color=ff0000][b]?[/b][/color]"
            )

        # ==========================================
        # MOSTRAR RESULTADO
        # ==========================================

        self.text = texto

        # ==========================================
        # MOSTRAR LA PARTE FINAL SOLAMENTE SI
        # EL CONTENIDO SUPERA EL ÁREA VISIBLE
        # ==========================================

        Clock.schedule_once(
            self._comprobar_scroll,
            0
        )
