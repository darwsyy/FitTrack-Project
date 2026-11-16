"""FitTrack application shell and primary navigation."""
from kivy.config import Config
from kivy.utils import platform

# Configure a phone-shaped preview before Kivy creates the desktop window.
if platform in ("win", "linux", "macosx"):
    Config.set("graphics", "width", "390")
    Config.set("graphics", "height", "844")
    Config.set("graphics", "resizable", "1")

from kivy.app import App
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from app.widgets.components import PALETTES, FTCard, FTButton, EmptyState


class FitTrackApp(App):
    """Main Kivy application."""

    title = "FitTrack"
    NAV_ITEMS = ("Home", "Cardio", "Workout", "Food", "Sleep")
    NAV_LABELS = {
        "Home": "Home", "Cardio": "Lari", "Workout": "Latihan",
        "Food": "Makan", "Sleep": "Tidur",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_name = "light"
        self.manager = None
        self.nav_buttons = {}
        self.theme_label = None

    @property
    def palette(self):
        return PALETTES[self.theme_name]

    def build(self):
        """Build the app shell."""
        self.manager = ScreenManager(transition=NoTransition())
        for name in self.NAV_ITEMS + ("Profile", "Settings"):
            self.manager.add_widget(self._make_screen(name))

        root = BoxLayout(
            orientation="vertical", spacing=dp(8),
            padding=[dp(12), dp(10), dp(12), dp(8)],
        )
        root.bind(size=self._update_background, pos=self._update_background)
        self.root_layout = root
        self._draw_background(root)

        self.header = self._top_bar()
        root.add_widget(self.header)
        root.add_widget(self.manager)
        self.navigation = self._navigation_bar()
        root.add_widget(self.navigation)
        self.manager.current = "Home"
        self._refresh_navigation()
        return root

    def _draw_background(self, widget):
        widget.canvas.before.clear()
        with widget.canvas.before:
            Color(*self.palette["background"])
            Rectangle(pos=widget.pos, size=widget.size)

    def _update_background(self, widget, *_):
        self._draw_background(widget)

    def _top_bar(self):
        bar = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        title = Label(
            text="FitTrack", bold=True, font_size="22sp",
            color=self.palette["text"], halign="left",
        )
        title.bind(size=lambda obj, size: setattr(obj, "text_size", size))
        profile = FTButton("Profil", self.palette)
        profile.bind(on_release=lambda *_: self.go_to("Profile"))
        bar.add_widget(title)
        bar.add_widget(profile)
        return bar

    def _navigation_bar(self):
        nav = GridLayout(cols=5, spacing=dp(4), size_hint_y=None,
                         height=dp(54))
        self.nav_buttons = {}
        for name in self.NAV_ITEMS:
            button = FTButton(self.NAV_LABELS[name], self.palette,
                              selected=(name == "Home"), font_size="12sp")
            button.bind(on_release=lambda _btn, target=name:
                        self.go_to(target))
            self.nav_buttons[name] = button
            nav.add_widget(button)
        return nav

    def _refresh_navigation(self):
        for name, button in self.nav_buttons.items():
            button.set_selected(self.manager.current == name)

    def go_to(self, screen_name):
        """Navigate without rebuilding the root widget tree."""
        if self.manager and screen_name in self.manager.screen_names:
            self.manager.current = screen_name
            self._refresh_navigation()

    def _make_screen(self, name):
        screen = Screen(name=name)
        page = BoxLayout(orientation="vertical", spacing=dp(12),
                         padding=dp(8))
        page.add_widget(Label(
            text=name, color=self.palette["text"], bold=True,
            font_size="21sp", size_hint_y=None, height=dp(38),
        ))
        if name == "Home":
            self._build_home(page)
        elif name == "Profile":
            self._build_profile(page)
        elif name == "Settings":
            self._build_settings(page)
        else:
            page.add_widget(EmptyState(
                f"Belum ada catatan {name.lower()}",
                "Catatan dan aktivitas yang kamu tambahkan akan muncul di sini.",
                self.palette,
            ))
        screen.add_widget(page)
        return screen

    def _build_home(self, page):
        scroll = ScrollView(do_scroll_x=False)
        content = GridLayout(
            cols=1, spacing=dp(10), padding=[0, 0, 0, dp(12)],
            size_hint_y=None,
        )
        content.bind(minimum_height=content.setter("height"))
        content.add_widget(Label(
            text="Ringkasan aktivitasmu", color=self.palette["muted"],
            font_size="14sp", size_hint_y=None, height=dp(28),
            halign="left",
        ))
        for heading, detail in (
            ("Wellness Score", "Belum ada data yang cukup untuk menghitung skor."),
            ("Aktivitas hari ini", "Belum ada aktivitas yang dicatat."),
            ("Konsistensi mingguan", "Mulai dengan kebiasaan yang realistis."),
            ("Tidur terakhir", "Catatan tidur akan tampil setelah ditambahkan."),
            ("Nutrisi hari ini", "Pencatatan makanan bersifat opsional."),
        ):
            card = FTCard(self.palette, height=dp(92))
            card.add_widget(Label(
                text=heading, color=self.palette["text"], bold=True,
                font_size="15sp", size_hint_y=None, height=dp(24),
                halign="left",
            ))
            card.add_widget(Label(
                text=detail, color=self.palette["muted"],
                font_size="12sp", halign="left",
            ))
            content.add_widget(card)
        scroll.add_widget(content)
        page.add_widget(scroll)

    def _build_profile(self, page):
        card = FTCard(self.palette, height=dp(116))
        card.add_widget(Label(
            text="Profil pengguna", color=self.palette["text"],
            bold=True, font_size="16sp",
        ))
        card.add_widget(Label(
            text="Profil belum diatur. Pengaturan profil akan tersedia pada Phase 2.",
            color=self.palette["muted"], font_size="13sp",
        ))
        page.add_widget(card)
        button = FTButton("Buka Settings", self.palette)
        button.bind(on_release=lambda *_: self.go_to("Settings"))
        page.add_widget(button)

    def _build_settings(self, page):
        card = FTCard(self.palette, height=dp(112))
        card.add_widget(Label(
            text="Tampilan aplikasi", color=self.palette["text"],
            bold=True, font_size="16sp",
        ))
        self.theme_label = Label(
            text=f"Tema aktif: {self.theme_name.title()}",
            color=self.palette["muted"], font_size="13sp",
        )
        card.add_widget(self.theme_label)
        page.add_widget(card)
        toggle = FTButton("Ganti tema terang / gelap", self.palette)
        toggle.bind(on_release=lambda *_: self.toggle_theme())
        page.add_widget(toggle)
        page.add_widget(Label(
            text="Pengaturan akun, privasi, dan data akan ditambahkan pada tahap terkait.",
            color=self.palette["muted"], font_size="12sp",
        ))

    def toggle_theme(self):
        """Apply palette changes in-place and preserve current navigation."""
        old_palette = self.palette
        self.theme_name = "dark" if self.theme_name == "light" else "light"
        new_palette = self.palette
        color_map = {
            tuple(old_palette[key]): new_palette[key]
            for key in old_palette
        }

        def recolor(widget):
            if isinstance(widget, FTCard):
                widget.apply_palette(new_palette)
            if isinstance(widget, FTButton):
                widget.apply_palette(new_palette)
            for attribute in (
                "color", "background_color", "foreground_color",
                "hint_text_color", "cursor_color",
            ):
                if hasattr(widget, attribute):
                    value = getattr(widget, attribute)
                    if isinstance(value, (list, tuple)) and len(value) == 4:
                        replacement = color_map.get(tuple(value))
                        if replacement is not None:
                            setattr(widget, attribute, replacement)
            for child in widget.children:
                recolor(child)

        recolor(self.root_layout)
        self._draw_background(self.root_layout)
        if self.theme_label:
            self.theme_label.text = f"Tema aktif: {self.theme_name.title()}"
        self._refresh_navigation()
