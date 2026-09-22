# ==========================================
# IG_TABLE_TENNIS_ANALYZER
# igtta.py
# Ventana principal
# ==========================================

from kivy.app import App
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

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
        
        Window.clearcolor = (0, 0, 0, 1)
        
        # ==========================================
        # VENTANA PRINCIPAL
        # ==========================================

        principal = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )
        
        # ==========================================
        # VARIABLES
        # ==========================================

        self.jugada = ""

        # Indica si ya se ha mostrado el resultado
        # de la última jugada
        self.jugada_finalizada = False

        # ==========================================
        # TÍTULO
        # ==========================================

        self.titulo = Entrada.crear_titulo()

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
        # CONTENEDOR DEL BOTÓN
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
        #
        # El visor puede crecer, pero solamente
        # dentro del espacio que queda disponible.
        #
        # De esta forma:
        #
        # - El título no desaparece.
        # - La salida permanece visible.
        # - El marcador permanece visible.
        # - Los botones inferiores permanecen visibles.
        # - Una jugada larga utiliza ScrollView.
        #
        # ==========================================

        def ajustar_altura_visor(*args):

            # --------------------------------------
            # Alturas FIJAS que debemos conservar
            # --------------------------------------

            altura_titulo = self.titulo.height

            altura_separador = dp(30)

            altura_panel = self.panel.height

            altura_label = dp(22)

            altura_salida = dp(180)

            altura_fila = dp(70)

            altura_botones = (
                self.botones_inferiores.height
            )

            # --------------------------------------
            # ESPACIOS ENTRE LOS ELEMENTOS
            # --------------------------------------
            #
            # principal tiene:
            #
            # padding arriba + abajo = 20
            #
            # y varios spacing de 10.
            #
            # Hay 7 elementos principales:
            #
            # 1 título
            # 2 separador
            # 3 panel
            # 4 label
            # 5 visor
            # 6 salida
            # 7 fila
            # 8 botones inferiores
            #
            # Entre ellos hay 7 espacios.
            #
            # --------------------------------------

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

            # --------------------------------------
            # ESPACIO REAL DISPONIBLE PARA EL VISOR
            # --------------------------------------

            espacio_disponible = (
                principal.height
                - altura_fija
                - dp(80)
            )

            # --------------------------------------
            # ALTURA FINAL DEL VISOR
            # --------------------------------------

            altura_final = min(
                ALTURA_MAXIMA,
                max(
                    0,
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

        self.visor.bind(
            height=ajustar_altura_visor
        )

        self.panel.bind(
            height=ajustar_altura_visor
        )

        self.botones_inferiores.bind(
            height=ajustar_altura_visor
        )

        # ------------------------------------------
        # Primera actualización
        # ------------------------------------------

        Clock.schedule_once(
            ajustar_altura_visor,
            0
        )

        def mostrar_alturas(*args):

            texto_diagnostico = (
                "DIAGNÓSTICO\n\n"
                f"Window.size: {Window.size}\n"
                f"Window.system_size: {Window.system_size}\n"
                f"Window.dpi: {Window.dpi:.1f}\n"
                f"dp(1): {dp(1):.2f}\n\n"
                f"Principal: {principal.height:.1f} dp\n"
                f"Título: {self.titulo.height:.1f} dp\n"
                f"Panel: {self.panel.height:.1f} dp\n"
                f"Label: {self.label_jugada.height:.1f} dp\n"
                f"Scroll: {scroll.height:.1f} dp\n"
                f"Visor: {self.visor.height:.1f} dp\n"
                f"Salida: {self.salida.height:.1f} dp\n"
                f"Fila: {fila.height:.1f} dp\n"
                f"Botones inferiores: "
                f"{self.botones_inferiores.height:.1f} dp"
            )

            diagnostico = Label(
                text=texto_diagnostico,
                color=(1, 1, 1, 1),
                font_size="12sp",
                size_hint=(None, None),
                size=(dp(300), dp(300)),
                halign="left",
                valign="top"
            )

            diagnostico.text_size = diagnostico.size

            from kivy.uix.popup import Popup

            popup_diagnostico = Popup(
                title="Diagnóstico Android",
                content=diagnostico,
                size_hint=(None, None),
                size=(dp(330), dp(360)),
                auto_dismiss=True
            )

            popup_diagnostico.open()

        Clock.schedule_once(
            mostrar_alturas,
            1
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
    # INSERTAR CÓDIGO
    # ==========================================

    def insertar_codigo(
        self,
        codigo
    ):

        # ==========================================
        # SI LA JUGADA ANTERIOR YA TERMINÓ,
        # AL PULSAR EL PRIMER BOTÓN DE LA NUEVA
        # JUGADA SE BORRA AUTOMÁTICAMENTE
        # ==========================================

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

        # ==========================================
        # SI LA PARTIDA ANTERIOR TERMINÓ
        # ==========================================

        if Config.ganador:

            Config.tantoA = 0
            Config.tantoB = 0
            Config.juegoA = 0
            Config.juegoB = 0
            Config.ganador = False

            self.marcador.reiniciar()

        # ==========================================
        # BORRAR ÚLTIMO CÓDIGO
        # ==========================================

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

        # ==========================================
        # BORRAR TODA LA SECUENCIA
        # ==========================================

        elif codigo == "C":

            self.jugada = ""

        # ==========================================
        # AÑADIR CÓDIGO
        # ==========================================

        else:

            self.jugada += codigo

        # ==========================================
        # MOSTRAR JUGADA QUE SE ESTÁ CONSTRUYENDO
        # ==========================================

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

            jugada = (
                self.jugada
                .strip()
                .upper()
            )

            if not jugada:
                return

            # --------------------------------------
            # SEPARADOR ENTRE JUGADAS
            # --------------------------------------

            if self.salida.tiene_texto():

                self.mostrar("")

            # --------------------------------------
            # PROCESAR PUNTO
            # --------------------------------------

            correcta, posicion = (
                self.logica.procesar_punto(
                    jugada
                )
            )

            # --------------------------------------
            # CAMBIAR TÍTULO
            # --------------------------------------

            self.label_jugada.text = (
                "[b]RESULTADO JUGADA:[/b]"
            )

            # ======================================
            # FALTA TERMINAR JUGADA
            # ======================================

            if self.logica.falta_terminar:

                self.salida.mostrar_resultado(
                    falta_terminar=True
                )

            # ======================================
            # RED - SE REPITE SAQUE
            # ======================================

            elif self.logica.repite_saque:

                self.salida.mostrar_resultado(
                    repite_saque=True
                )

            # ======================================
            # VISOR DE JUGADA
            # ======================================

            self.visor.mostrar_resultado(
                jugada,
                correcta,
                posicion,
                self.logica.falta_terminar
            )

            # ======================================
            # MARCADOR
            # ======================================

            self.marcador.actualizar(
                Config.tantoA,
                Config.tantoB,
                Config.juegoA,
                Config.juegoB
            )

            # ======================================
            # LIMPIAR JUGADA
            # ======================================

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

        self.label_jugada.text = (
            "[b]INICIO JUGADA:[/b]"
        )


# ==========================================
# EJECUCIÓN
# ==========================================

if __name__ == "__main__":
    TenisMesaApp().run()
