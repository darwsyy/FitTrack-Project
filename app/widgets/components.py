"""Reusable presentation components for FitTrack."""
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

PALETTES = {
    "light": {
        "background": (0.96, 0.97, 0.98, 1),
        "surface": (1, 1, 1, 1),
        "text": (0.10, 0.14, 0.19, 1),
        "muted": (0.40, 0.45, 0.51, 1),
        "accent": (0.12, 0.48, 0.39, 1),
        "accent_text": (1, 1, 1, 1),
        "border": (0.88, 0.90, 0.92, 1),
    },
    "dark": {
        "background": (0.07, 0.09, 0.12, 1),
        "surface": (0.12, 0.15, 0.19, 1),
        "text": (0.93, 0.95, 0.97, 1),
        "muted": (0.65, 0.69, 0.74, 1),
        "accent": (0.20, 0.66, 0.55, 1),
        "accent_text": (0.04, 0.08, 0.07, 1),
        "border": (0.22, 0.26, 0.31, 1),
    },
}


class FTCard(BoxLayout):
    """Rounded surface with a theme-aware background."""

    def __init__(self, palette, **kwargs):
        super().__init__(orientation="vertical", padding=dp(14),
                         spacing=dp(8), size_hint_y=None, **kwargs)
        self.palette = palette
        self.bind(pos=self._redraw, size=self._redraw)
        self._redraw()

    def _redraw(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.palette["surface"])
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])

    def apply_palette(self, palette):
        self.palette = palette
        self._redraw()


class FTButton(Button):
    """Consistent, theme-aware button."""

    def __init__(self, text, palette, selected=False, **kwargs):
        super().__init__(text=text, **kwargs)
        self.palette = palette
        self.selected = selected
        self.size_hint_y = None
        self.height = dp(46)
        self.font_size = "13sp"
        self.background_normal = ""
        self.background_down = ""
        self.apply_palette(palette)

    def apply_palette(self, palette):
        self.palette = palette
        self.background_color = (
            palette["accent"] if self.selected else palette["surface"]
        )
        self.color = (
            palette["accent_text"] if self.selected else palette["text"]
        )
        self.bold = self.selected

    def set_selected(self, selected):
        self.selected = selected
        self.apply_palette(self.palette)


class EmptyState(BoxLayout):
    """Informative placeholder for a page without user records."""

    def __init__(self, title, message, palette, **kwargs):
        super().__init__(orientation="vertical", spacing=dp(8),
                         padding=dp(18), **kwargs)
        self.add_widget(Label(text=title, color=palette["text"],
                              bold=True, font_size="17sp",
                              size_hint_y=None, height=dp(28)))
        self.add_widget(Label(text=message, color=palette["muted"],
                              font_size="13sp", halign="center",
                              valign="middle"))


class LoadingState(Label):
    """Small reusable loading indicator for future async operations."""

    def __init__(self, palette, **kwargs):
        super().__init__(text="Memuat data...", color=palette["muted"],
                         font_size="13sp", **kwargs)


class FTInput(TextInput):
    """Reusable text input with FitTrack palette defaults."""

    def __init__(self, palette, hint_text="", **kwargs):
        super().__init__(hint_text=hint_text, multiline=False, **kwargs)
        self.size_hint_y = None
        self.height = dp(46)
        self.padding = [dp(12), dp(12)]
        self.apply_palette(palette)

    def apply_palette(self, palette):
        self.background_normal = ""
        self.background_active = ""
        self.background_color = palette["surface"]
        self.foreground_color = palette["text"]
        self.hint_text_color = palette["muted"]
        self.cursor_color = palette["accent"]


class FTChartContainer(FTCard):
    """Reserved chart surface; real charts wait for domain data."""

    def __init__(self, title, palette, **kwargs):
        super().__init__(palette, height=dp(150), **kwargs)
        self.add_widget(Label(text=title, color=palette["text"],
                              bold=True, font_size="15sp"))
        self.add_widget(Label(
            text="Grafik akan ditampilkan setelah data tersedia.",
            color=palette["muted"], font_size="12sp",
        ))
