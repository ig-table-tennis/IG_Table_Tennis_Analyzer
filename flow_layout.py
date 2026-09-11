from kivy.uix.layout import Layout
from kivy.metrics import dp


class FlowLayout(Layout):

    def __init__(self, spacing=5, **kwargs):
        super().__init__(**kwargs)

        self.spacing = spacing

        self.bind(
            children=self._reorganizar,
            size=self._reorganizar
        )

    def do_layout(self):
        self._reorganizar()

    def _reorganizar(self, *args):

        x = 0
        y = 0

        fila_alto = 0

        for widget in self.children[::-1]:

            w = widget.width
            h = widget.height

            if x + w > self.width and x > 0:
                x = 0
                y += fila_alto + self.spacing
                fila_alto = 0

            widget.pos = (self.x + x, self.y + y)

            x += w + self.spacing
            fila_alto = max(fila_alto, h)

        alto = max(dp(40), y + fila_alto)

        if self.height != alto:
            self.height = alto