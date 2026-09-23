# ==========================================
# IG_TABLE_TENNIS_ANALYZER
# widgets/ig_button.py
# Botón personalizado IG
# ==========================================

from kivy.graphics import (
    Color,
    RoundedRectangle,
    Line,
    PushMatrix,
    PopMatrix,
    Translate
)

from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.core.audio import SoundLoader


class IGButton(Button):

    # ==========================================
    # SONIDOS
    # ==========================================

    sonidos_golpe = []
    sonidos_analizar = []
    sonidos_borrar = []
    sonidos_comenzar = []
    sonidos_no = []

    _indice_golpe = 0
    _indice_analizar = 0
    _indice_borrar = 0
    _indice_comenzar = 0
    _indice_no = 0

    # ==========================================
    # ANDROID SOUNDPOOL
    # ==========================================

    _soundpool = None
    _android_sounds = {}
    _android_intentado = False

    # ==========================================
    # CARGAR SONIDOS PARA PC / FALLBACK
    #
    # IMPORTANTE:
    # Estos sonidos NO se reproducen al arrancar.
    # Solo se utilizan cuando se pulsa un botón.
    # ==========================================

    @classmethod
    def _cargar_sonidos(cls):

        if cls.sonidos_golpe:
            return

        try:

            cls.sonidos_golpe = [
                SoundLoader.load(
                    "sounds/golpe_seco.wav"
                ),
                SoundLoader.load(
                    "sounds/golpe_seco.wav"
                ),
                SoundLoader.load(
                    "sounds/golpe_seco.wav"
                ),
            ]

            cls.sonidos_analizar = [
                SoundLoader.load(
                    "sounds/analizar.wav"
                ),
                SoundLoader.load(
                    "sounds/analizar.wav"
                ),
                SoundLoader.load(
                    "sounds/analizar.wav"
                ),
            ]

            cls.sonidos_borrar = [
                SoundLoader.load(
                    "sounds/borrar.wav"
                ),
                SoundLoader.load(
                    "sounds/borrar.wav"
                ),
                SoundLoader.load(
                    "sounds/borrar.wav"
                ),
            ]

            cls.sonidos_comenzar = [
                SoundLoader.load(
                    "sounds/comenzar.wav"
                ),
                SoundLoader.load(
                    "sounds/comenzar.wav"
                ),
                SoundLoader.load(
                    "sounds/comenzar.wav"
                ),
            ]

            cls.sonidos_no = [
                SoundLoader.load(
                    "sounds/no.wav"
                ),
                SoundLoader.load(
                    "sounds/no.wav"
                ),
                SoundLoader.load(
                    "sounds/no.wav"
                ),
            ]

        except Exception:

            cls.sonidos_golpe = []
            cls.sonidos_analizar = []
            cls.sonidos_borrar = []
            cls.sonidos_comenzar = []
            cls.sonidos_no = []

    # ==========================================
    # INICIALIZACIÓN
    # ==========================================

    def __init__(
        self,
        codigo="",
        icon=None,
        **kwargs
    ):

        self.codigo = codigo
        self.icon = icon

        super().__init__(**kwargs)

        # ==================================
        # FUENTE
        # ==================================

        self.font_name = (
            "fonts/NotoSans-SemiBold.ttf"
        )

        # ==================================
        # TEXTO
        # ==================================

        self.halign = "center"
        self.valign = "middle"
        self.line_height = 0.85
        self.bold = True

        if "font_size" not in kwargs:
            self.font_size = "16sp"

        self.color = (
            1,
            1,
            1,
            1
        )

        # ==================================
        # FONDO ORIGINAL DE KIVY
        # ==================================

        self.background_normal = ""
        self.background_down = ""

        self.background_color = (
            0,
            0,
            0,
            0
        )

        self.border = (
            0,
            0,
            0,
            0
        )

        # ==================================
        # COLOR REAL DEL BOTÓN
        # ==================================

        self._color = (
            0.30,
            0.30,
            0.30,
            1
        )

        # ==================================
        # TRANSFORMACIÓN DE ANIMACIÓN
        # ==================================

        with self.canvas.before:

            self.push_matrix = PushMatrix()

            self.translate = Translate(
                x=0,
                y=0
            )

            # ==================================
            # FONDO
            # ==================================

            self.color_fondo = Color(
                rgba=self._color
            )

            self.fondo = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(10)]
            )

            self.pop_matrix = PopMatrix()

        self.bind(
            pos=self._actualizar,
            size=self._actualizar
        )

        # ==================================
        # FLECHA DE RETROCESO
        # ==================================

        if self.codigo == "←":

            with self.canvas.after:

                self.color_flecha = Color(
                    rgba=(0, 0, 0, 1)
                )

                self.flecha = Line(
                    points=[],
                    width=dp(2),
                    cap="square"
                )

            self.bind(
                pos=self._actualizar_flecha,
                size=self._actualizar_flecha
            )

            self._actualizar_flecha()

        # ==================================
        # ICONO
        # ==================================

        if self.icon:

            self.text = ""

            self.imagen = Image(
                source=self.icon,
                size_hint=(None, None)
            )

            self.add_widget(
                self.imagen
            )

            self.bind(
                pos=self._actualizar_icono,
                size=self._actualizar_icono
            )

            self._actualizar_icono()

        self.texture_update()

        # ==================================
        # ANIMACIÓN DE PRESIÓN
        # ==================================

        self.bind(
            on_press=self._animacion_presion
        )

    # ==========================================
    # INICIALIZAR SOUNDPOOL ANDROID
    #
    # IMPORTANTE:
    # NO se ejecuta durante el arranque.
    # Se ejecuta solamente al pulsar un botón.
    # ==========================================

    @classmethod
    def _inicializar_android(cls):

        # Ya se intentó anteriormente
        if cls._android_intentado:
            return

        cls._android_intentado = True

        try:

            from jnius import autoclass

            SoundPoolBuilder = autoclass(
                "android.media.SoundPool$Builder"
            )

            AudioAttributesBuilder = autoclass(
                "android.media.AudioAttributes$Builder"
            )

            AudioAttributes = autoclass(
                "android.media.AudioAttributes"
            )

            audio_attributes = (
                AudioAttributesBuilder()
                .setUsage(
                    AudioAttributes.USAGE_GAME
                )
                .setContentType(
                    AudioAttributes.CONTENT_TYPE_SONIFICATION
                )
                .build()
            )

            cls._soundpool = (
                SoundPoolBuilder()
                .setMaxStreams(8)
                .setAudioAttributes(
                    audio_attributes
                )
                .build()
            )

            # ==================================
            # ACTIVIDAD ANDROID
            # ==================================

            activity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            context = activity.mActivity

            asset_manager = (
                context.getAssets()
            )

            # ==================================
            # SONIDOS
            # ==================================

            nombres = {
                "golpe":
                    "sounds/golpe_seco.wav",

                "analizar":
                    "sounds/analizar.wav",

                "borrar":
                    "sounds/borrar.wav",

                "comenzar":
                    "sounds/comenzar.wav",

                "no":
                    "sounds/no.wav",
            }

            for nombre, archivo in nombres.items():

                try:

                    asset_file = (
                        asset_manager.openFd(
                            archivo
                        )
                    )

                    sound_id = (
                        cls._soundpool.load(
                            asset_file.getFileDescriptor(),
                            asset_file.getStartOffset(),
                            asset_file.getLength(),
                            1
                        )
                    )

                    cls._android_sounds[
                        nombre
                    ] = sound_id

                    asset_file.close()

                except Exception:

                    pass

        except Exception:

            cls._soundpool = None
            cls._android_sounds = {}

    # ==========================================
    # REPRODUCIR SOUNDPOOL ANDROID
    # ==========================================

    @classmethod
    def _reproducir_android(cls, nombre):

        if cls._soundpool is None:
            return False

        sound_id = (
            cls._android_sounds.get(
                nombre
            )
        )

        if not sound_id:
            return False

        try:

            cls._soundpool.play(
                sound_id,
                1.0,
                1.0,
                1,
                0,
                1.0
            )

            return True

        except Exception:

            return False

    # ==========================================
    # REPRODUCIR SONIDO
    # ==========================================

    @classmethod
    def _reproducir_sonido(
        cls,
        sonidos,
        atributo,
        android_nombre=None
    ):

        # ==================================
        # ANDROID
        #
        # SoundPool solo se intenta cuando
        # se pulsa el botón.
        # ==================================

        if android_nombre is not None:

            cls._inicializar_android()

            if cls._reproducir_android(
                android_nombre
            ):

                return

        # ==================================
        # FALLBACK
        # ==================================

        cls._cargar_sonidos()

        if not sonidos:
            return

        indice = getattr(
            cls,
            atributo
        )

        sonido = sonidos[indice]

        indice += 1

        if indice >= len(sonidos):
            indice = 0

        setattr(
            cls,
            atributo,
            indice
        )

        if sonido is not None:

            try:

                sonido.play()

            except Exception:

                pass

    # ==========================================
    # OBTENER Y REPRODUCIR SONIDO
    # ==========================================

    def _reproducir_sonido_boton(self):

        texto = self.text.strip().upper()

        # ==================================
        # ANALIZAR
        # ==================================

        if texto == "ANALIZAR":

            self._reproducir_sonido(
                IGButton.sonidos_analizar,
                "_indice_analizar",
                "analizar"
            )

            return

        # ==================================
        # BORRAR
        # ==================================

        if self.codigo in (
            "C",
            "←",
            "BORRAR",
            "BORRAR_PANTALLA"
        ):

            self._reproducir_sonido(
                IGButton.sonidos_borrar,
                "_indice_borrar",
                "borrar"
            )

            return

        # ==================================
        # BORRAR PANTALLA
        # ==================================

        if "BORRAR PANTALLA" in texto:

            self._reproducir_sonido(
                IGButton.sonidos_borrar,
                "_indice_borrar",
                "borrar"
            )

            return

        # ==================================
        # NUEVA PARTIDA
        # ==================================

        if texto == "NUEVA PARTIDA":

            self._reproducir_sonido(
                IGButton.sonidos_comenzar,
                "_indice_comenzar",
                "comenzar"
            )

            return

        # ==================================
        # SÍ
        # ==================================

        if texto in (
            "SI",
            "SÍ"
        ):

            self._reproducir_sonido(
                IGButton.sonidos_comenzar,
                "_indice_comenzar",
                "comenzar"
            )

            return

        # ==================================
        # NO
        # ==================================

        if texto == "NO":

            self._reproducir_sonido(
                IGButton.sonidos_no,
                "_indice_no",
                "no"
            )

            return

        # ==================================
        # SONIDO NORMAL
        # ==================================

        self._reproducir_sonido(
            IGButton.sonidos_golpe,
            "_indice_golpe",
            "golpe"
        )

    # ==========================================
    # ACTUALIZAR FONDO
    # ==========================================

    def _actualizar(self, *args):

        self.fondo.pos = self.pos
        self.fondo.size = self.size

    # ==========================================
    # ACTUALIZAR FLECHA
    # ==========================================

    def _actualizar_flecha(self, *args):

        if self.codigo != "←":
            return

        x = self.center_x
        y = self.center_y

        largo = (
            min(
                self.width,
                self.height
            ) * 0.25
        )

        punta = dp(8)

        self.flecha.points = [

            x + largo,
            y,
            x - largo,
            y,

            x - largo,
            y,
            x - largo + punta,
            y + punta,

            x - largo,
            y,
            x - largo + punta,
            y - punta,
        ]

    # ==========================================
    # COLOR DEL FONDO
    # ==========================================

    def set_color(self, color):

        self._color = color

        self.color_fondo.rgba = color

    # ==========================================
    # COLOR DEL TEXTO
    # ==========================================

    def set_text_color(self, color):

        self.color = color

    # ==========================================
    # CÓDIGO
    # ==========================================

    def set_codigo(self, codigo):

        self.codigo = codigo

    # ==========================================
    # ACTUALIZAR ICONO
    # ==========================================

    def _actualizar_icono(self, *args):

        if not self.icon:
            return

        lado = (
            min(
                self.width,
                self.height
            ) * 0.55
        )

        self.imagen.size = (
            lado,
            lado
        )

        self.imagen.center = self.center

    # ==========================================
    # ANIMACIÓN DE PRESIÓN + SONIDO
    # ==========================================

    def _animacion_presion(self, *args):

        # ==================================
        # SONIDO INMEDIATO
        # ==================================

        self._reproducir_sonido_boton()

        # ==================================
        # CANCELAR ANIMACIÓN ANTERIOR
        # ==================================

        Animation.cancel_all(
            self.translate
        )

        # ==================================
        # VOLVER A POSICIÓN ORIGINAL
        # ==================================

        self.translate.y = 0

        # ==================================
        # PRESIÓN
        # ==================================

        animacion = Animation(
            y=-dp(5),
            duration=0.05
        )

        # ==================================
        # REGRESO
        # ==================================

        animacion += Animation(
            y=0,
            duration=0.10
        )

        # ==================================
        # EJECUTAR
        # ==================================

        animacion.start(
            self.translate
        )
