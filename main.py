import traceback

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


try:
    from igtta import TenisMesaApp
    TenisMesaApp().run()

except Exception:
    error = traceback.format_exc()

    class ErrorApp(App):
        def build(self):
            scroll = ScrollView()

            label = Label(
                text=error,
                font_size="12sp",
                size_hint_y=None,
                halign="left",
                valign="top"
            )

            label.bind(texture_size=label.setter("size"))

            scroll.add_widget(label)

            return scroll

    ErrorApp().run()
