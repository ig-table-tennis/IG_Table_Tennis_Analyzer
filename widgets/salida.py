# ==========================================
# widgets/salida.py
# Historial de salida
# ==========================================

from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.metrics import dp


class Salida(ScrollView):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # ==================================
        # CONFIGURACIÓN
        # ==================================

        self.font_name = (
            "fonts/NotoSans-SemiBold.ttf"
        )

        self.do_scroll_x = False
        self.do_scroll_y = True

        # ==================================
        # CONTENEDOR DEL HISTORIAL
        # ==================================

        self.contenedor = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            spacing=dp(4),
            padding=(dp(8), dp(8))
        )

        self.contenedor.bind(
            minimum_height=self.contenedor.setter(
                "height"
            )
        )

        # ==================================
        # FONDO NEGRO
        # ==================================

        with self.contenedor.canvas.before:

            Color(0, 0, 0, 1)

            self.fondo = Rectangle(
                pos=self.contenedor.pos,
                size=self.contenedor.size
            )

        self.contenedor.bind(
            pos=self._actualizar_fondo,
            size=self._actualizar_fondo
        )

        self.add_widget(
            self.contenedor
        )

        self.size_hint = (1, None)

    # ==================================
    # MOSTRAR TEXTO NORMAL
    # ==================================

    def mostrar(self, texto):

        texto = str(texto)

        etiqueta = Label(
            text=texto,
            markup=True,
            font_name=self.font_name,
            font_size="16sp",
            halign="left",
            valign="top",
            size_hint=(1, None),
            color=(0.0, 1.0, 0.0, 1),
            padding=(dp(0), dp(2))
        )

        etiqueta.bind(
            width=self._actualizar_ancho
        )

        etiqueta.bind(
            texture_size=self._actualizar_alto
        )

        self.contenedor.add_widget(
            etiqueta
        )

        Clock.schedule_once(
            self._ir_abajo,
            0
        )

    # ==================================
    # MOSTRAR BLOQUE ARRIBA
    # ==================================

    def mostrar_bloque_arriba(
        self,
        bloque
    ):

        bloque = str(bloque)

        etiqueta = Label(
            text=bloque,
            markup=True,
            font_name=self.font_name,
            font_size="16sp",
            halign="center",
            valign="top",
            size_hint=(1, None),
            color=(0.0, 1.0, 0.0, 1),
            padding=(dp(0), dp(2))
        )

        etiqueta.bind(
            width=self._actualizar_ancho
        )

        etiqueta.bind(
            texture_size=self._actualizar_alto
        )

        self.contenedor.add_widget(
            etiqueta,
            index=0
        )

        Clock.schedule_once(
            self._ir_arriba,
            0
        )

    # ==================================
    # MOSTRAR BLOQUE DEBAJO
    # ==================================

    def mostrar_bloque_debajo(
        self,
        bloque
    ):

        bloque = str(bloque)

        etiqueta = Label(
            text=bloque,
            markup=True,
            font_name=self.font_name,
            font_size="16sp",
            halign="left",
            valign="top",
            size_hint=(1, None),
            color=(0.0, 1.0, 0.0, 1),
            padding=(dp(0), dp(2))
        )

        etiqueta.bind(
            width=self._actualizar_ancho
        )

        etiqueta.bind(
            texture_size=self._actualizar_alto
        )

        self.contenedor.add_widget(
            etiqueta
        )

        Clock.schedule_once(
            self._ir_abajo,
            0
        )

    # ==================================
    # RESULTADO DE LA JUGADA
    # ==================================

    def mostrar_resultado(
        self,
        ganador=None,
        colision=None,
        posicion=None,
        game_over=False,
        falta_terminar=False,
        repite_saque=False
    ):

        resultado = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            spacing=dp(2),
            padding=(0, dp(2))
        )

        # ==================================
        # FALTA TERMINAR
        # ==================================

        if falta_terminar:

            fila = self._fila_icono_texto(
                "icons/diana.png",
                "[color=ff0000][b]"
                "FALTA TERMINAR JUGADA..."
                "[/b][/color]"
            )

            resultado.add_widget(
                fila
            )

        # ==================================
        # RED - SE REPITE EL SAQUE
        # ==================================

        elif repite_saque:

            fila = self._fila_icono_texto(
                "icons/pala.png",
                "[color=ff0000][b]"
                "RED, SE REPITE EL SAQUE"
                "[/b][/color]"
            )

            resultado.add_widget(
                fila
            )

        # ==================================
        # RESULTADO NORMAL
        # ==================================

        else:

            fila1 = self._fila_icono_texto(
                "icons/pala.png",
                "[b]Punto ganado por jugador:[/b] "
                f"{ganador}"
            )

            fila2 = self._fila_icono_texto(
                "icons/diana.png",
                "[b]Motivo:[/b] "
                f"{colision}"
            )

            resultado.add_widget(
                fila1
            )

            resultado.add_widget(
                fila2
            )

        # ==================================
        # GAME OVER
        # ==================================

        if game_over:

            # ----------------------------------
            # LÍNEA SEPARADORA VERDE
            # ----------------------------------

            linea = Widget(
                size_hint=(1, None),
                height=dp(10)
            )

            with linea.canvas:

                Color(
                    0,
                    1,
                    0,
                    1
                )

                linea.rect = Rectangle(
                    pos=(
                        linea.x,
                        linea.y + dp(4)
                    ),
                    size=(
                        linea.width,
                        dp(1)
                    )
                )

            linea.bind(
                pos=self._actualizar_linea,
                size=self._actualizar_linea
            )

            resultado.add_widget(
                linea
            )

            # ----------------------------------
            # FILA GAME OVER
            # ----------------------------------

            fila_game_over = BoxLayout(
                orientation="horizontal",
                size_hint=(1, None),
                spacing=dp(6),
                padding=(
                    dp(0),
                    dp(2)
                )
            )

            # ----------------------------------
            # TEXTO GAME OVER
            # ----------------------------------

            game = Label(
                text=(
                    "[color=ff0000][b]"
                    "GAME OVER. PARTIDA GANADA "
                    f"POR EL JUGADOR {ganador}"
                    "[/b][/color]"
                ),
                markup=True,
                font_name=self.font_name,
                font_size="16sp",
                halign="left",
                valign="middle",
                size_hint=(1, None),
                color=(1, 1, 1, 1),
                padding=(
                    dp(0),
                    dp(2)
                )
            )

            # ----------------------------------
            # ANCHO DISPONIBLE
            # ----------------------------------

            game.bind(
                width=self._actualizar_ancho
            )

            # ----------------------------------
            # ALTURA SEGÚN EL TEXTO
            # ----------------------------------

            game.bind(
                texture_size=self._actualizar_alto
            )

            # ----------------------------------
            # TROFEO
            # ----------------------------------

            trofeo = Image(
                source="icons/campeon.png",
                size_hint=(None, None),
                size=(
                    dp(28),
                    dp(28)
                ),
                allow_stretch=True,
                keep_ratio=True
            )

            fila_game_over.add_widget(
                game
            )

            fila_game_over.add_widget(
                trofeo
            )

            # ----------------------------------
            # LA FILA SE ADAPTA A GAME
            # ----------------------------------

            def ajustar_fila(*args):

                fila_game_over.height = max(
                    game.height,
                    trofeo.height
                ) + dp(4)

            game.bind(
                height=ajustar_fila
            )

            trofeo.bind(
                height=ajustar_fila
            )

            Clock.schedule_once(
                ajustar_fila,
                0
            )

            resultado.add_widget(
                fila_game_over
            )

        # ==================================
        # ALTURA AUTOMÁTICA DEL RESULTADO
        # ==================================

        def ajustar_resultado(*args):

            resultado.height = (
                resultado.minimum_height
            )

        resultado.bind(
            minimum_height=ajustar_resultado
        )

        Clock.schedule_once(
            ajustar_resultado,
            0
        )

        # ==================================
        # INSERTAR ARRIBA
        # ==================================

        self.contenedor.add_widget(
            resultado,
            index=0
        )

        Clock.schedule_once(
            self._ir_arriba,
            0
        )

    # ==================================
    # FILA ICONO + TEXTO
    # ==================================

    def _fila_icono_texto(
        self,
        ruta_icono,
        texto
    ):

        fila = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            spacing=dp(6),
            padding=(0, dp(2))
        )

        # ----------------------------------
        # ICONO
        # ----------------------------------

        icono = Image(
            source=ruta_icono,
            size_hint=(None, None),
            size=(
                dp(24),
                dp(24)
            ),
            allow_stretch=True,
            keep_ratio=True
        )

        # ----------------------------------
        # TEXTO
        # ----------------------------------

        etiqueta = Label(
            text=texto,
            markup=True,
            font_name=self.font_name,
            font_size="16sp",
            halign="left",
            valign="middle",
            size_hint=(1, None),
            color=(0.0, 1.0, 0.0, 1)
        )

        # ----------------------------------
        # ANCHO DEL TEXTO
        # ----------------------------------

        def actualizar_texto(*args):

            etiqueta.text_size = (
                etiqueta.width,
                None
            )

        etiqueta.bind(
            width=actualizar_texto
        )

        # ----------------------------------
        # ALTURA DEL TEXTO
        # ----------------------------------

        def actualizar_altura(*args):

            etiqueta.height = max(
                dp(28),
                etiqueta.texture_size[1]
            )

            fila.height = max(
                etiqueta.height,
                icono.height
            ) + dp(4)

        etiqueta.bind(
            texture_size=actualizar_altura
        )

        fila.add_widget(
            icono
        )

        fila.add_widget(
            etiqueta
        )

        Clock.schedule_once(
            actualizar_altura,
            0
        )

        return fila

    # ==================================
    # BORRAR
    # ==================================

    def borrar(self):

        self.contenedor.clear_widgets()

    # ==================================
    # ¿TIENE TEXTO?
    # ==================================

    def tiene_texto(self):

        return bool(
            self.contenedor.children
        )

    # ==================================
    # ACTUALIZAR ALTO
    # ==================================

    def _actualizar_alto(
        self,
        instancia,
        valor
    ):

        instancia.height = max(
            dp(1),
            valor[1]
        )

    # ==================================
    # ACTUALIZAR ANCHO
    # ==================================

    def _actualizar_ancho(
        self,
        instancia,
        valor
    ):

        instancia.text_size = (
            valor,
            None
        )

    # ==================================
    # ACTUALIZAR LÍNEA
    # ==================================

    def _actualizar_linea(
        self,
        instancia,
        valor
    ):

        instancia.rect.pos = (
            instancia.x,
            instancia.y + dp(4)
        )

        instancia.rect.size = (
            instancia.width,
            dp(1)
        )

    # ==================================
    # ACTUALIZAR FONDO
    # ==================================

    def _actualizar_fondo(
        self,
        instancia,
        valor
    ):

        self.fondo.pos = instancia.pos
        self.fondo.size = instancia.size

    # ==================================
    # SCROLL ABAJO
    # ==================================

    def _ir_abajo(
        self,
        dt
    ):

        self.scroll_y = 0

    # ==================================
    # SCROLL ARRIBA
    # ==================================

    def _ir_arriba(
        self,
        dt
    ):

        self.scroll_y = 1
