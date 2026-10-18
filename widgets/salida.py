# ==========================================
# widgets/salida.py
# Historial de salida
# ==========================================

from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from kivy.graphics import Color, Rectangle, Line, RoundedRectangle, Mesh
from kivy.clock import Clock
from kivy.metrics import dp


class Salida(ScrollView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.font_name = "fonts/NotoSans-SemiBold.ttf"
        self._game_over_overlay = None
        self._game_over_event = None
        self.do_scroll_x = False
        self.do_scroll_y = True

        self.contenedor = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            spacing=dp(4),
            padding=(dp(8), dp(8))
        )
        self.contenedor.bind(
            minimum_height=self.contenedor.setter("height")
        )

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

        self.add_widget(self.contenedor)
        self.size_hint = (1, None)

    # ==================================
    # MOSTRAR TEXTO NORMAL
    # ==================================

    def mostrar(self, texto):
        etiqueta = Label(
            text=str(texto),
            markup=True,
            font_name=self.font_name,
            font_size="16sp",
            halign="left",
            valign="top",
            size_hint=(1, None),
            color=(0.0, 1.0, 0.0, 1),
            padding=(dp(0), dp(2))
        )
        etiqueta.bind(width=self._actualizar_ancho)
        etiqueta.bind(texture_size=self._actualizar_alto)
        self.contenedor.add_widget(etiqueta)
        Clock.schedule_once(self._ir_abajo, 0)

    # ==================================
    # MOSTRAR BLOQUE ARRIBA
    # ==================================

    def mostrar_bloque_arriba(self, bloque):
        etiqueta = Label(
            text=str(bloque),
            markup=True,
            font_name=self.font_name,
            font_size="16sp",
            halign="center",
            valign="top",
            size_hint=(1, None),
            color=(0.0, 1.0, 0.0, 1),
            padding=(dp(0), dp(2))
        )
        etiqueta.bind(width=self._actualizar_ancho)
        etiqueta.bind(texture_size=self._actualizar_alto)
        self.contenedor.add_widget(etiqueta, index=0)
        Clock.schedule_once(self._ir_arriba, 0)

    # ==================================
    # MOSTRAR BLOQUE DEBAJO
    # ==================================

    def mostrar_bloque_debajo(self, bloque):
        etiqueta = Label(
            text=str(bloque),
            markup=True,
            font_name=self.font_name,
            font_size="16sp",
            halign="left",
            valign="top",
            size_hint=(1, None),
            color=(0.0, 1.0, 0.0, 1),
            padding=(dp(0), dp(2))
        )
        etiqueta.bind(width=self._actualizar_ancho)
        etiqueta.bind(texture_size=self._actualizar_alto)
        self.contenedor.add_widget(etiqueta)
        Clock.schedule_once(self._ir_abajo, 0)

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
            # Retoque mínimo adicional: subir solo el bloque de resultado un poco más.
            # El resto de la interfaz y la separación inferior no cambian.
            padding=(0, dp(-7), 0, dp(2))
        )

        if falta_terminar:
            resultado.add_widget(
                self._fila_icono_texto(
                    "icons/diana.png",
                    "[color=ff0000][b]"
                    "FALTA TERMINAR JUGADA..."
                    "[/b][/color]"
                )
            )

        elif repite_saque:
            resultado.add_widget(
                self._fila_icono_texto(
                    "icons/pala.png",
                    "[color=ff0000][b]"
                    "RED, SE REPITE EL SAQUE"
                    "[/b][/color]"
                )
            )

        else:
            fila1 = self._fila_icono_texto(
                "icons/pala.png",
                "[b]Punto ganado por jugador:[/b] "
                f"{ganador}"
            )
            fila2 = self._fila_motivo(
                "icons/diana.png",
                colision
            )
            resultado.add_widget(fila1)
            resultado.add_widget(fila2)

        # ==================================
        # GAME OVER: mensaje centrado superpuesto
        # ==================================

        if game_over:
            self.mostrar_game_over(ganador)

        def ajustar_resultado(*args):
            resultado.height = resultado.minimum_height

        resultado.bind(minimum_height=ajustar_resultado)
        Clock.schedule_once(ajustar_resultado, 0)

        self.contenedor.add_widget(resultado, index=0)
        Clock.schedule_once(self._ir_arriba, 0)

    # ==================================
    # FILA ICONO + TEXTO
    # ==================================

    def _fila_icono_texto(self, ruta_icono, texto):
        fila = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            spacing=dp(6),
            padding=(0, dp(2))
        )

        icono = Image(
            source=ruta_icono,
            size_hint=(None, None),
            size=(dp(24), dp(24)),
            allow_stretch=True,
            keep_ratio=True
        )

        etiqueta = Label(
            text=texto,
            markup=True,
            font_name=self.font_name,
            font_size="16sp",
            halign="left",
            valign="top",
            size_hint=(1, None),
            color=(0.0, 1.0, 0.0, 1),
            padding=(0, 0)
        )

        def actualizar_texto(*args):
            etiqueta.text_size = (max(0, etiqueta.width), None)

        def actualizar_altura(*args):
            etiqueta.height = max(dp(28), etiqueta.texture_size[1])
            fila.height = max(icono.height, etiqueta.height) + dp(4)

        etiqueta.bind(width=actualizar_texto)
        etiqueta.bind(texture_size=actualizar_altura)

        fila.add_widget(icono)
        fila.add_widget(etiqueta)

        Clock.schedule_once(actualizar_texto, 0)
        Clock.schedule_once(actualizar_altura, 0)
        return fila

    # ==========================================
    # FILA MOTIVO
    # Diana, "Motivo:" y explicación alineados arriba.
    # La explicación empieza en la misma línea que "Motivo:";
    # sus líneas siguientes quedan alineadas con su propio inicio.
    # ==========================================

    def _fila_motivo(self, ruta_icono, motivo):
        fila = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            spacing=dp(6),
            padding=(0, dp(2))
        )

        contenedor_icono = AnchorLayout(
            anchor_x="center",
            anchor_y="top",
            size_hint=(None, None),
            size=(dp(24), dp(24))
        )
        icono = Image(
            source=ruta_icono,
            size_hint=(None, None),
            size=(dp(24), dp(24)),
            allow_stretch=True,
            keep_ratio=True
        )
        contenedor_icono.add_widget(icono)

        zona_texto = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            spacing=dp(4),
            padding=(0, 0)
        )

        etiqueta_motivo = Label(
            text="[b]Motivo:[/b]",
            markup=True,
            font_name=self.font_name,
            font_size="16sp",
            size_hint=(None, None),
            color=(0, 1, 0, 1),
            halign="left",
            valign="top",
            padding=(0, 0)
        )
        etiqueta_motivo.texture_update()
        ancho_motivo = etiqueta_motivo.texture_size[0]
        alto_motivo = max(dp(24), etiqueta_motivo.texture_size[1])

        anclaje_motivo = AnchorLayout(
            anchor_x="left",
            anchor_y="top",
            size_hint=(None, None),
            width=ancho_motivo,
            height=alto_motivo
        )
        etiqueta_motivo.size = (ancho_motivo, alto_motivo)
        anclaje_motivo.add_widget(etiqueta_motivo)

        etiqueta_explicacion = Label(
            text=str(motivo or ""),
            markup=True,
            font_name=self.font_name,
            font_size="16sp",
            size_hint=(1, None),
            color=(0, 1, 0, 1),
            halign="left",
            valign="top",
            # Ajuste fino: subir solo el texto de la explicación un milímetro más.
            # No modifica la posición de la diana, de "Motivo:" ni del resto.
            padding=(0, dp(-2))
        )

        anclaje_explicacion = AnchorLayout(
            anchor_x="left",
            anchor_y="top",
            size_hint=(1, None)
        )
        anclaje_explicacion.add_widget(etiqueta_explicacion)

        zona_texto.add_widget(anclaje_motivo)
        zona_texto.add_widget(anclaje_explicacion)
        fila.add_widget(contenedor_icono)
        fila.add_widget(zona_texto)

        def actualizar(*args):
            # El ancho disponible para la explicación excluye "Motivo:".
            ancho = max(
                dp(1),
                zona_texto.width - anclaje_motivo.width - zona_texto.spacing
            )
            etiqueta_explicacion.text_size = (ancho, None)
            etiqueta_explicacion.width = ancho
            etiqueta_explicacion.texture_update()

            # Añadir un pequeño margen inferior para evitar cortar la última línea.
            alto_explicacion = max(
                dp(24),
                etiqueta_explicacion.texture_size[1]
            ) + dp(6)
            etiqueta_explicacion.height = alto_explicacion

            alto_fila = max(alto_motivo, alto_explicacion)
            zona_texto.height = alto_fila
            anclaje_motivo.height = alto_fila
            anclaje_explicacion.height = alto_fila
            contenedor_icono.height = alto_fila
            fila.height = alto_fila + dp(6)

        zona_texto.bind(width=actualizar)
        fila.bind(width=actualizar)
        Clock.schedule_once(actualizar, 0)

        return fila

    # ==================================
    # AVISO GAME OVER CENTRADO Y PARPADEANTE
    # ==================================

    def mostrar_game_over(self, ganador):
        self.ocultar_game_over()

        overlay = FloatLayout(size_hint=(1, 1))

        # Tarjeta centrada con banda roja rellena y estrellas amarillas.
        cuadro = FloatLayout(
            size_hint=(0.94, None),
            height=dp(112),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        texto = Label(
            text=(
                "[color=ff2020][b]GAME OVER. PARTIDA GANADA\n"
                f"POR EL JUGADOR {ganador}[/b][/color]"
            ),
            markup=True,
            font_name=self.font_name,
            font_size="16sp",
            halign="center",
            valign="middle",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.48, "center_y": 0.5},
            color=(1, 1, 1, 1)
        )
        texto.bind(size=lambda w, v: setattr(w, "text_size", w.size))

        # El trofeo queda junto a la segunda línea y ligeramente por debajo.
        # Su posición horizontal se ajusta un poco a la derecha respecto al diseño.
        trofeo = Image(
            source="icons/campeon.png",
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            pos_hint={"center_x": 0.86, "center_y": 0.38},
            allow_stretch=True,
            keep_ratio=True
        )

        cuadro.add_widget(texto)
        cuadro.add_widget(trofeo)

        # Dibujo en canvas: banda roja, interior blanco y estrellas sólidas.
        self._dibujar_estrellas_game_over(cuadro)

        overlay.add_widget(cuadro)
        Window.add_widget(overlay)

        self._game_over_overlay = overlay
        self._game_over_visible = True
        self._game_over_event = Clock.schedule_interval(
            self._alternar_game_over, 1.2
        )

    def _dibujar_estrellas_game_over(self, cuadro):
        """Dibuja estrellas amarillas rellenas dentro de una banda roja."""
        from math import cos, sin, pi

        def agregar_estrella(vertices, indices, cx, cy, radio):
            # Un vértice central y diez vértices alternando puntas y entrantes.
            base = len(vertices) // 4
            vertices.extend((cx, cy, 0, 0))
            puntos = []
            for i in range(10):
                angulo = -pi / 2 + i * pi / 5
                r = radio if i % 2 == 0 else radio * 0.46
                puntos.append((cx + cos(angulo) * r,
                               cy + sin(angulo) * r))
                vertices.extend((puntos[-1][0], puntos[-1][1], 0, 0))
            for i in range(10):
                indices.extend((base, base + 1 + i, base + 1 + ((i + 1) % 10)))

        def actualizar(*args):
            cuadro.canvas.before.clear()

            x, y = cuadro.pos
            ancho, alto = cuadro.size
            if ancho <= 0 or alto <= 0:
                return

            borde = dp(10)
            radio_esquina = dp(12)
            radio_estrella = dp(4.1)

            with cuadro.canvas.before:
                # La base roja rellena también las cuatro esquinas.
                Color(0.95, 0.0, 0.0, 1)
                RoundedRectangle(
                    pos=(x, y),
                    size=(ancho, alto),
                    radius=[radio_esquina]
                )

                # El rectángulo blanco interior deja visible la banda roja.
                Color(1, 1, 1, 1)
                RoundedRectangle(
                    pos=(x + borde, y + borde),
                    size=(max(dp(1), ancho - 2 * borde),
                          max(dp(1), alto - 2 * borde)),
                    radius=[dp(4)]
                )

                # Estrellas sólidas en las bandas superior e inferior.
                Color(1.0, 0.82, 0.0, 1.0)
                vertices = []
                indices = []
                n_horizontal = max(8, min(30, int(ancho / dp(13))))
                x_inicio = x + borde / 2 + radio_estrella
                x_fin = x + ancho - borde / 2 - radio_estrella
                for i in range(n_horizontal):
                    fraccion = i / max(1, n_horizontal - 1)
                    cx = x_inicio + (x_fin - x_inicio) * fraccion
                    agregar_estrella(
                        vertices, indices, cx, y + borde / 2, radio_estrella
                    )
                    agregar_estrella(
                        vertices, indices, cx, y + alto - borde / 2, radio_estrella
                    )

                # Estrellas en los laterales, sin invadir las esquinas curvas.
                n_vertical = max(2, int((alto - dp(32)) / dp(18)))
                y_inicio = y + dp(16)
                y_fin = y + alto - dp(16)
                for i in range(n_vertical):
                    fraccion = (i + 0.5) / n_vertical
                    cy = y_inicio + (y_fin - y_inicio) * fraccion
                    agregar_estrella(
                        vertices, indices, x + borde / 2, cy, radio_estrella
                    )
                    agregar_estrella(
                        vertices, indices, x + ancho - borde / 2, cy, radio_estrella
                    )

                if vertices and indices:
                    Mesh(vertices=vertices, indices=indices, mode="triangles")

        cuadro.bind(pos=actualizar, size=actualizar)
        Clock.schedule_once(actualizar, 0)

    def _alternar_game_over(self, dt):
        if self._game_over_overlay is None:
            return False
        self._game_over_visible = not self._game_over_visible
        self._game_over_overlay.opacity = (
            1 if self._game_over_visible else 0
        )

    def ocultar_game_over(self):
        if self._game_over_event is not None:
            self._game_over_event.cancel()
            self._game_over_event = None
        if self._game_over_overlay is not None:
            if self._game_over_overlay.parent is not None:
                self._game_over_overlay.parent.remove_widget(
                    self._game_over_overlay
                )
            self._game_over_overlay = None

    # ==================================
    # BORRAR
    # ==================================

    def borrar(self):
        self.ocultar_game_over()
        self.contenedor.clear_widgets()

    # ==================================
    # ¿TIENE TEXTO?
    # ==================================

    def tiene_texto(self):
        return bool(self.contenedor.children)

    # ==================================
    # ACTUALIZAR ALTO
    # ==================================

    def _actualizar_alto(self, instancia, valor):
        instancia.height = max(dp(1), valor[1])

    # ==================================
    # ACTUALIZAR ANCHO
    # ==================================

    def _actualizar_ancho(self, instancia, valor):
        instancia.text_size = (valor, None)

    # ==================================
    # ACTUALIZAR LÍNEA
    # ==================================

    def _actualizar_linea(self, instancia, valor):
        instancia.rect.pos = (
            instancia.x,
            instancia.y + dp(4)
        )
        instancia.rect.size = (instancia.width, dp(1))

    # ==================================
    # ACTUALIZAR FONDO
    # ==================================

    def _actualizar_fondo(self, instancia, valor):
        self.fondo.pos = instancia.pos
        self.fondo.size = instancia.size

    # ==================================
    # SCROLL ABAJO
    # ==================================

    def _ir_abajo(self, dt):
        self.scroll_y = 0

    # ==================================
    # SCROLL ARRIBA
    # ==================================

    def _ir_arriba(self, dt):
        self.scroll_y = 1
