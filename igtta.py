# ==========================================
# IG_TABLE_TENNIS_ANALYZER
# igtta.py
# Ventana principal
# ==========================================

from kivy.app import App
from kivy.metrics import dp
from kivy.clock import Clock

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from widgets.panel_botones import PanelBotones
from widgets.marcador import Marcador
from widgets.salida import Salida
from widgets.visor_jugada import VisorJugada
from widgets.entrada import Entrada
from widgets.ig_button import IGButton

from logica import Logica, Config


class TenisMesaApp(App):

    def build(self):

        principal = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        self.jugada = ""
        self.jugada_finalizada = False

        # ==========================================
        # TÍTULO + BOTÓN AYUDA
        # ==========================================

        self.titulo = Entrada.crear_titulo(self)

        principal.add_widget(
            self.titulo
        )

        principal.add_widget(
            Widget(
                size_hint=(1, None),
                height=dp(30)
            )
        )

        # ==========================================
        # PANEL DE BOTONES
        # ==========================================

        self.panel = PanelBotones(
            callback=self.insertar_codigo
        )

        principal.add_widget(
            self.panel
        )

        # ==========================================
        # TEXTO INICIO JUGADA
        # ==========================================

        self.label_jugada = Label(
            text="[b]INICIO JUGADA:[/b]",
            markup=True,
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=dp(22),
            halign="left",
            valign="middle"
        )

        self.label_jugada.bind(
            size=lambda w, s: setattr(
                w,
                "text_size",
                w.size
            )
        )

        principal.add_widget(
            self.label_jugada
        )

        # ==========================================
        # VISOR GRÁFICO DE LA JUGADA
        # ==========================================

        ALTURA_MAXIMA = dp(250)
        ALTURA_MINIMA = dp(60)

        scroll = ScrollView(
            size_hint=(1, None),
            height=ALTURA_MINIMA,
            do_scroll_x=False,
            do_scroll_y=True
        )

        self.visor = VisorJugada(
            size_hint=(1, None)
        )

        # ------------------------------------------
        # FONDO DEL VISOR
        # ------------------------------------------

        with self.visor.canvas.before:

            from kivy.graphics import Color, Rectangle

            Color(
                0.7,
                0.7,
                0.7,
                1
            )

            self.visor._bg = Rectangle()

            self.visor.bind(
                pos=lambda w, v: setattr(
                    self.visor._bg,
                    "pos",
                    w.pos
                ),
                size=lambda w, v: setattr(
                    self.visor._bg,
                    "size",
                    w.size
                )
            )

        scroll.add_widget(
            self.visor
        )

        self.visor.conectar_scroll(
            scroll
        )

        principal.add_widget(
            scroll
        )

        # ==========================================
        # HISTORIAL / SALIDA
        # ==========================================

        self.salida = Salida(
            size_hint=(1, None),
            height=dp(180)
        )

        principal.add_widget(
            self.salida
        )

        # ==========================================
        # COMPROBAR + MARCADOR
        # ==========================================

        fila = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(70),
            spacing=dp(10)
        )

        # ------------------------------------------
        # BOTÓN ANALIZAR
        # ------------------------------------------

        self.boton_comprobar = IGButton(
            text="ANALIZAR",
            size_hint=(None, None),
            width=dp(100),
            height=dp(50),
            font_size="12sp"
        )

        self.boton_comprobar.set_color(
            (0.0, 0.65, 0.0, 1)
        )

        self.boton_comprobar.bind(
            on_press=self.comprobar
        )

        # ------------------------------------------
        # CONTENEDOR DEL BOTÓN ANALIZAR
        # ------------------------------------------

        contenedor = AnchorLayout(
            anchor_x="left",
            anchor_y="center",
            size_hint=(None, 1),
            width=dp(120),
            padding=(
                0,
                dp(10),
                0,
                0
            )
        )

        contenedor.add_widget(
            self.boton_comprobar
        )

        fila.add_widget(
            contenedor
        )

        # ------------------------------------------
        # MARCADOR
        # ------------------------------------------

        self.marcador = Marcador()

        fila.add_widget(
            self.marcador
        )

        principal.add_widget(
            fila
        )

        # ==========================================
        # BOTONES INFERIORES
        # ==========================================

        self.botones_inferiores = (
            Entrada.crear_botones_inferiores(
                self
            )
        )

        principal.add_widget(
            self.botones_inferiores
        )

        # ==========================================
        # AJUSTE DINÁMICO DEL VISOR
        # ==========================================

        def ajustar_altura_visor(*args):

            altura_titulo = self.titulo.height

            altura_separador = dp(30)

            altura_panel = self.panel.height

            altura_label = dp(22)

            altura_salida = dp(180)

            altura_fila = dp(70)

            altura_botones = (
                self.botones_inferiores.height
            )

            altura_espacios = (
                dp(20) +
                dp(70)
            )

            altura_fija = (
                altura_titulo
                + altura_separador
                + altura_panel
                + altura_label
                + altura_salida
                + altura_fila
                + altura_botones
                + altura_espacios
            )

            espacio_disponible = (
                principal.height
                - altura_fija
            )

            altura_final = min(
                ALTURA_MAXIMA,
                max(
                    ALTURA_MINIMA,
                    espacio_disponible
                )
            )

            scroll.height = altura_final

        # ==========================================
        # ACTUALIZAR CUANDO CAMBIA LA ALTURA
        # ==========================================

        principal.bind(
            height=ajustar_altura_visor
        )

        self.panel.bind(
            height=ajustar_altura_visor
        )

        self.botones_inferiores.bind(
            height=ajustar_altura_visor
        )

        Clock.schedule_once(
            ajustar_altura_visor,
            0
        )

        # ==========================================
        # LÓGICA
        # ==========================================

        self.logica = Logica(
            self.mostrar,
            self.salida.mostrar_resultado,
            self.salida.mostrar_bloque_arriba
        )

        # ==========================================
        # COMPROBAR BASE DE DATOS
        # ==========================================

        if not self.logica.bd_disponible:

            self.salida.mostrar(
                "[color=ff0000][b]"
                "ERROR CRÍTICO"
                "[/b][/color]\n\n"
                "No se ha encontrado la base de datos "
                "'colisionables.db'.\n\n"
                "La aplicación no puede continuar."
            )

            self.bloquear_interfaz()

        return principal

        # ==========================================
    # MOSTRAR AYUDA
    # ==========================================

    def mostrar_ayuda(
        self,
        instance
    ):

        # ==========================================
        # CONTENEDOR PRINCIPAL
        # ==========================================

        contenido = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        # ==========================================
        # POPUP
        # ==========================================

        popup = Popup(
            title="Ayuda",
            content=contenido,
            size_hint=(None, None),
            size=(
                dp(350),
                dp(600)
            ),
            auto_dismiss=True
        )

        # ==========================================
        # TEXTOS DE LA AYUDA
        # ==========================================

        textos = {

            "¿QUÉ ES IGTTA?": (
                "[b]¿QUÉ ES IGTTA?[/b]\n\n"

                "[b]IG Table Tennis Analyzer (IGTTA)[/b] "
                "es una herramienta diseñada para analizar "
                "jugadas de tenis de mesa y simular una partida "
                "entre dos jugadores: A y B.\n\n"

                "El programa permite registrar, paso a paso, "
                "los contactos que se producen durante cada "
                "jugada y analizar la secuencia para determinar "
                "qué ocurre en el punto.\n\n"

                "Además, IGTTA lleva automáticamente el "
                "marcador de tantos y juegos hasta determinar "
                "el ganador de la partida."
            ),

            "¿CÓMO SE SIMULA UNA PARTIDA?": (
                "[b]¿CÓMO SE SIMULA UNA PARTIDA?[/b]\n\n"

                "Una partida real de tenis de mesa se juega "
                "normalmente al mejor de 5 juegos, y cada juego "
                "es a 11 tantos.\n\n"

                "Para que la simulación con IGTTA sea más rápida "
                "y no resulte larga o pesada, el programa utiliza "
                "una modalidad de partida reducida:\n\n"

                "• Cada juego es a 3 tantos.\n"
                "• La partida es al mejor de 5 juegos.\n"
                "• Gana la partida el jugador que consigue "
                "3 juegos primero.\n\n"

                "De esta forma, una partida puede terminar en un "
                "máximo de 5 juegos, haciendo la simulación mucho "
                "más ágil."
            ),

            "¿CÓMO SE INICIA UNA JUGADA?": (
                "[b]¿CÓMO SE INICIA UNA JUGADA?[/b]\n\n"

                "Cada punto comienza con un saque realizado "
                "por uno de los dos jugadores.\n\n"

                "El saque debe introducirse siguiendo esta "
                "secuencia:\n\n"

                "[b]Jugador A:[/b]\n"
                "JA → MA → MB\n\n"

                "[b]Jugador B:[/b]\n"
                "JB → MB → MA\n\n"

                "Es decir:\n\n"

                "1. Golpeo del jugador que realiza el saque.\n"
                "2. Primer bote en la mesa cercana al jugador "
                "que saca.\n"
                "3. Segundo bote en la mesa del jugador "
                "contrario.\n\n"

                "Una vez completado el saque, la pelota continúa "
                "en juego."
            ),

            "¿CÓMO CONTINÚA LA JUGADA?": (
                "[b]¿CÓMO CONTINÚA LA JUGADA?[/b]\n\n"

                "Después del saque, se introducen las colisiones "
                "que se produzcan durante el punto, siempre en "
                "el mismo orden en que ocurren.\n\n"

                "Puede producirse cualquier combinación de "
                "situaciones contempladas por IGTTA, como:\n\n"

                "• Golpeo de un jugador.\n"
                "• Bote en la mesa.\n"
                "• Contacto con la red.\n"
                "• Contacto con una valla.\n"
                "• Contacto con un lateral.\n"
                "• Contacto con el suelo.\n"
                "• Contacto con la tapa de la mesa.\n"
                "• Contacto con la base de una pata.\n"
                "• O cualquier otra situación contemplada "
                "por el programa.\n\n"

                "Después del saque no existe una secuencia "
                "predeterminada: la secuencia dependerá de lo "
                "que ocurra durante la jugada."
            ),

            "¿CÓMO TERMINA UNA JUGADA?": (
                "[b]¿CÓMO TERMINA UNA JUGADA?[/b]\n\n"

                "IGTTA analiza la secuencia introducida y "
                "determina cómo termina el punto.\n\n"

                "El resultado se muestra en pantalla junto "
                "con la explicación correspondiente.\n\n"

                "No es necesario conocer de memoria todas las "
                "reglas del tenis de mesa para utilizar el "
                "programa. Tener conocimientos básicos del juego "
                "facilita la comprensión de las situaciones, "
                "pero IGTTA está diseñado para que el resultado "
                "sea didáctico y fácil de seguir.\n\n"

                "El programa se encarga de analizar la secuencia "
                "y explicar qué ha ocurrido."
            ),

            "BOTONES DE JUEGO": (
                "[b]BOTONES DE JUEGO[/b]\n\n"

                "[b]Jugador A / Jugador B[/b]\n"
                "Identifican a los dos jugadores que participan "
                "en la jugada. A corresponde al jugador A y B "
                "corresponde al jugador B.\n\n"

                "[b]Mesa A / Mesa B[/b]\n"
                "Identifican el lado de la mesa correspondiente "
                "a cada jugador.\n\n"

                "[b]Red[/b]\n"
                "Indica un contacto de la pelota con la red.\n\n"

                "[b]Tapa Mesa[/b]\n"
                "Indica un contacto de la pelota con la tabla "
                "situada en la parte inferior de la mesa que une "
                "las patas y proporciona una mayor sujeción y "
                "estabilidad.\n\n"

                "[b]Base Pata[/b]\n"
                "Indica un contacto de la pelota con las patas "
                "de la mesa, que son las que sostienen la mesa "
                "sobre el suelo.\n\n"

                "[b]Valla[/b]\n"
                "Indica un contacto de la pelota con una valla.\n\n"

                "[b]Lateral[/b]\n"
                "Indica un contacto de la pelota con un lateral.\n\n"

                "[b]Suelo[/b]\n"
                "Indica un contacto de la pelota con el suelo."
            ),

            "OTROS BOTONES": (
                "[b]OTROS BOTONES[/b]\n\n"

                "[b]ATRÁS ←[/b]\n"
                "Elimina la última acción introducida "
                "en la jugada.\n\n"

                "[b]C[/b]\n"
                "Borra la jugada que se está introduciendo "
                "para comenzar de nuevo.\n\n"

                "[b]ANALIZAR[/b]\n"
                "Analiza la secuencia introducida y muestra "
                "el resultado.\n\n"

                "[b]Nueva partida[/b]\n"
                "Comienza una nueva partida y reinicia "
                "el marcador.\n\n"

                "[b]Borrar Pantalla[/b]\n"
                "Borra la información mostrada en pantalla."
            ),

            "IMPORTANTE": (
                "[b]IMPORTANTE[/b]\n\n"

                "Introduce siempre las acciones en el mismo "
                "orden en que se producen durante la jugada.\n\n"

                "Una vez introducida la secuencia, pulsa "
                "[b]ANALIZAR[/b] para que IGTTA compruebe "
                "la jugada y muestre el resultado."
            )
        }

        # ==========================================
        # MOSTRAR MENÚ PRINCIPAL
        # ==========================================

        def mostrar_menu():

            contenido.clear_widgets()

            titulo = Label(
                text="[b]ÍNDICE DE AYUDA[/b]",
                markup=True,
                size_hint=(1, None),
                height=dp(40),
                font_size="18sp"
            )

            contenido.add_widget(
                titulo
            )

            scroll = ScrollView(
                size_hint=(1, 1),
                do_scroll_x=False,
                do_scroll_y=True
            )

            lista = BoxLayout(
                orientation="vertical",
                spacing=dp(8),
                size_hint_y=None,
                padding=dp(5)
            )

            lista.bind(
                minimum_height=lista.setter(
                    "height"
                )
            )

            for titulo_seccion in textos:

                boton = IGButton(
                    text=titulo_seccion,
                    size_hint=(1, None),
                    height=dp(48),
                    font_size="13sp"
                )

                boton.set_color(
                    (0.25, 0.25, 0.25, 1)
                )

                boton.set_text_color(
                    (1, 1, 1, 1)
                )

                boton.bind(
                    on_press=lambda btn,
                    seccion=titulo_seccion:
                    mostrar_seccion(seccion)
                )

                lista.add_widget(
                    boton
                )

            scroll.add_widget(
                lista
            )

            contenido.add_widget(
                scroll
            )

        # ==========================================
        # MOSTRAR UNA SECCIÓN
        # ==========================================

        def mostrar_seccion(
            seccion
        ):

            contenido.clear_widgets()

            # ------------------------------
            # BOTÓN VOLVER
            # ------------------------------

            fila_superior = BoxLayout(
                orientation="horizontal",
                size_hint=(1, None),
                height=dp(45)
            )

            boton_volver = IGButton(
                text="← VOLVER",
                size_hint=(None, 1),
                width=dp(100),
                font_size="13sp"
            )

            boton_volver.set_color(
                (0.25, 0.25, 0.25, 1)
            )

            boton_volver.set_text_color(
                (1, 1, 1, 1)
            )

            boton_volver.bind(
                on_press=lambda *_:
                mostrar_menu()
            )

            fila_superior.add_widget(
                boton_volver
            )

            fila_superior.add_widget(
                Widget()
            )

            contenido.add_widget(
                fila_superior
            )

            # ------------------------------
            # TEXTO
            # ------------------------------

            texto = Label(
                text=textos[seccion],
                markup=True,
                halign="left",
                valign="top",
                size_hint_y=None,
                font_size="14sp"
            )

            def ajustar_texto(
                widget,
                width
            ):

                widget.text_size = (
                    width,
                    None
                )

            texto.bind(
                width=ajustar_texto
            )

            texto.bind(
                texture_size=lambda w, s:
                setattr(
                    w,
                    "height",
                    s[1]
                )
            )

            scroll = ScrollView(
                size_hint=(1, 1),
                do_scroll_x=False,
                do_scroll_y=True
            )

            scroll.add_widget(
                texto
            )

            contenido.add_widget(
                scroll
            )

        # ==========================================
        # ABRIR EN EL MENÚ PRINCIPAL
        # ==========================================

        mostrar_menu()

        popup.open()

    # ==========================================
    # INSERTAR CÓDIGO
    # ==========================================

    def insertar_codigo(
        self,
        codigo
    ):

        if self.jugada_finalizada:

            self.salida.borrar()
            self.visor.limpiar()

            self.logica.falta_terminar = False
            self.logica.repite_saque = False
            self.logica.posicion_resaltada = None

            self.jugada_finalizada = False
            self.jugada = ""

            self.label_jugada.text = (
                "[b]INICIO JUGADA:[/b]"
            )

        if Config.ganador:

            Config.tantoA = 0
            Config.tantoB = 0
            Config.juegoA = 0
            Config.juegoB = 0
            Config.ganador = False

            self.marcador.reiniciar()

        if codigo == "←":

            if self.jugada:

                if self.jugada[-2:] in (
                    "JA",
                    "JB",
                    "MA",
                    "MB",
                    "TM",
                    "BP"
                ):

                    self.jugada = (
                        self.jugada[:-2]
                    )

                else:

                    self.jugada = (
                        self.jugada[:-1]
                    )

        elif codigo == "C":

            self.jugada = ""

        else:

            self.jugada += codigo

        self.visor.mostrar(
            self.jugada
        )

    # ==========================================
    # MOSTRAR
    # ==========================================

    def mostrar(
        self,
        texto
    ):

        self.salida.mostrar(
            texto
        )

    # ==========================================
    # BLOQUEAR INTERFAZ
    # ==========================================

    def bloquear_interfaz(self):

        self.panel.disabled = True
        self.panel.opacity = 0.35

        self.boton_comprobar.disabled = True
        self.boton_comprobar.opacity = 0.35

        self.botones_inferiores.disabled = True
        self.botones_inferiores.opacity = 0.35

        self.visor.opacity = 0.35

        self.marcador.opacity = 0.35

    # ==========================================
    # COMPROBAR
    # ==========================================

    def comprobar(
        self,
        instance
    ):

        try:

            self.marcador.detener_animacion()

            jugada = (
                self.jugada
                .strip()
                .upper()
            )

            if not jugada:
                return

            if self.salida.tiene_texto():

                self.mostrar("")

            tantoA_antes = Config.tantoA
            tantoB_antes = Config.tantoB
            juegoA_antes = Config.juegoA
            juegoB_antes = Config.juegoB

            correcta, posicion = (
                self.logica.procesar_punto(
                    jugada
                )
            )

            self.label_jugada.text = (
                "[b]RESULTADO JUGADA:[/b]"
            )

            if self.logica.falta_terminar:

                self.salida.mostrar_resultado(
                    falta_terminar=True
                )

            elif self.logica.repite_saque:

                self.salida.mostrar_resultado(
                    repite_saque=True
                )

            self.visor.mostrar_resultado(
                jugada,
                correcta,
                posicion,
                self.logica.falta_terminar
            )

            self.marcador.actualizar(
                Config.tantoA,
                Config.tantoB,
                Config.juegoA,
                Config.juegoB
            )

            if (
                Config.tantoA > tantoA_antes
                and Config.tantoA > 0
            ):

                Clock.schedule_once(
                    lambda dt:
                    self.marcador.parpadear_A(),
                    0
                )

            elif (
                Config.tantoB > tantoB_antes
                and Config.tantoB > 0
            ):

                Clock.schedule_once(
                    lambda dt:
                    self.marcador.parpadear_B(),
                    0
                )

            elif Config.juegoA > juegoA_antes:

                Clock.schedule_once(
                    lambda dt:
                    self.marcador.parpadear_juego_A(),
                    0
                )

            elif Config.juegoB > juegoB_antes:

                Clock.schedule_once(
                    lambda dt:
                    self.marcador.parpadear_juego_B(),
                    0
                )

            self.jugada = ""
            self.jugada_finalizada = True

        except Exception:

            import traceback

            self.mostrar("")

            self.mostrar(
                "[color=ff0000][b]"
                "ERROR"
                "[/b][/color]"
            )

            self.mostrar(
                traceback.format_exc()
            )

    # ==========================================
    # BORRAR
    # ==========================================

    def borrar(
        self,
        instance
    ):

        self.salida.borrar()
        self.visor.limpiar()

        self.logica.falta_terminar = False
        self.logica.repite_saque = False
        self.logica.posicion_resaltada = None

        self.jugada = ""
        self.jugada_finalizada = False

        self.label_jugada.text = (
            "[b]INICIO JUGADA:[/b]"
        )

    # ==========================================
    # NUEVA PARTIDA
    # ==========================================

    def nueva_partida(
        self,
        instance
    ):

        contenido = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(10)
        )

        mensaje = Label(
            text="¿Comenzar una nueva partida?"
        )

        contenido.add_widget(
            mensaje
        )

        botones = BoxLayout(
            size_hint=(1, None),
            height=dp(45),
            spacing=dp(10)
        )

        popup = Popup(
            title="Confirmación",
            content=contenido,
            size_hint=(None, None),
            size=(
                dp(320),
                dp(180)
            ),
            auto_dismiss=False
        )

        boton_si = IGButton(
            text="Sí"
        )

        boton_si.set_color(
            (0.0, 0.65, 0.0, 1)
        )

        boton_no = IGButton(
            text="No"
        )

        boton_no.set_color(
            (0.8, 0.0, 0.0, 1)
        )

        # ------------------------------------------
        # CONFIRMAR NUEVA PARTIDA
        # ------------------------------------------

        def confirmar(_):

            popup.dismiss()

            self.salida.borrar()
            self.visor.limpiar()

            self.jugada = ""
            self.jugada_finalizada = False

            self.label_jugada.text = (
                "[b]INICIO JUGADA:[/b]"
            )

            Config.tantoA = 0
            Config.tantoB = 0
            Config.juegoA = 0
            Config.juegoB = 0
            Config.ganador = False

            self.logica.falta_terminar = False
            self.logica.repite_saque = False
            self.logica.posicion_resaltada = None

            self.marcador.reiniciar()

        boton_si.bind(
            on_press=confirmar
        )

        boton_no.bind(
            on_press=lambda *_:
            popup.dismiss()
        )

        botones.add_widget(
            boton_si
        )

        botones.add_widget(
            boton_no
        )

        contenido.add_widget(
            botones
        )

        popup.open()

    # ==========================================
    # BORRAR ÚLTIMO
    # ==========================================

    def borrar_ultimo(self):

        if (
            len(self.jugada) >= 2
            and self.jugada[-2:] in (
                "JA",
                "JB",
                "MA",
                "MB",
                "TM",
                "BP"
            )
        ):

            self.jugada = (
                self.jugada[:-2]
            )

        else:

            self.jugada = (
                self.jugada[:-1]
            )

        self.visor.mostrar(
            self.jugada
        )

    # ==========================================
    # LIMPIAR JUGADA
    # ==========================================

    def limpiar_jugada(self):

        self.jugada = ""

        self.visor.limpiar()

        self.logica.falta_terminar = False
        self.logica.repite_saque = False
        self.logica.posicion_resaltada = None

        self.label_jugada.text = (
            "[b]INICIO JUGADA:[/b]"
        )


# ==========================================
# EJECUCIÓN
# ==========================================

if __name__ == "__main__":
    TenisMesaApp().run()