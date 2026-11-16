"""FitTrack application shell, navigation, and onboarding/profile UI."""
from pathlib import Path
from datetime import datetime
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
from kivy.uix.spinner import Spinner

from app.database.connection import Database
from app.database.repositories.profile_repository import ProfileRepository
from app.services.data_manager import DataManager
from app.widgets.components import PALETTES, FTCard, FTButton, EmptyState, FTInput
from app.features.onboarding.validation import ProfileValidationError


class FitTrackApp(App):
    """Main Kivy application."""

    title = "FitTrack"
    NAV_ITEMS = ("Home", "Cardio", "Workout", "Food", "Sleep")
    NAV_LABELS = {
        "Home": "Home", "Cardio": "Lari", "Workout": "Latihan",
        "Food": "Makan", "Sleep": "Tidur",
    }
    EXPERIENCE_OPTIONS = {
        "Tidak ditentukan": "unspecified",
        "Pemula": "beginner",
        "Menengah": "intermediate",
        "Lanjutan": "advanced",
    }
    TRAINING_OPTIONS = {
        "Gym": "gym", "Home workout": "home", "Keduanya": "both",
    }

    def __init__(self, database_path=None, **kwargs):
        super().__init__(**kwargs)
        self.database_path = Path(database_path) if database_path else None
        self.theme_name = "light"
        self.manager = None
        self.nav_buttons = {}
        self.theme_label = None
        self.profile_forms = {}
        self.database = None
        self.profile_repository = None
        self.data_manager = None
        self.delete_confirmation_pending = False

    @property
    def palette(self):
        return PALETTES[self.theme_name]

    def build(self):
        """Initialize local storage and build the app shell."""
        db_path = self.database_path or (
            Path(self.user_data_dir) / "fittrack.sqlite3"
        )
        self.database = Database(db_path)
        self.profile_repository = ProfileRepository(self.database)
        self.data_manager = DataManager(self.database)

        self.manager = ScreenManager(transition=NoTransition())
        screen_names = ("Onboarding",) + self.NAV_ITEMS + ("Profile", "Settings")
        for name in screen_names:
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

        self._load_profile_form()
        if self.profile_repository.get_profile() is None:
            self.manager.current = "Onboarding"
        else:
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
        settings = FTButton("Setelan", self.palette)
        settings.bind(on_release=lambda *_: self.go_to("Settings"))
        self.settings_button = settings
        bar.add_widget(title)
        bar.add_widget(settings)
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
        elif name == "Onboarding":
            self._build_profile_form(page, "Onboarding")
        elif name == "Profile":
            self._build_profile_form(page, "Profile")
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

    def _build_profile_form(self, page, form_name):
        scroll = ScrollView(do_scroll_x=False)
        content = BoxLayout(
            orientation="vertical", spacing=dp(8),
            padding=[dp(4), dp(4), dp(4), dp(18)],
            size_hint_y=None,
        )
        content.bind(minimum_height=content.setter("height"))

        description = (
            "Isi nama tampilan untuk mulai. Data tinggi dan berat badan "
            "boleh dikosongkan dan tidak digunakan untuk menilai tubuh."
            if form_name == "Onboarding"
            else "Ubah profil kapan saja. Pengukuran tubuh tetap opsional."
        )
        content.add_widget(Label(
            text=description, color=self.palette["muted"],
            font_size="12sp", size_hint_y=None, height=dp(52),
            halign="left", valign="middle",
        ))

        fields = {}
        fields["display_name"] = self._add_form_field(
            content, "Nama tampilan *", "Nama"
        )
        fields["height_cm"] = self._add_form_field(
            content, "Tinggi badan (cm) — opsional", "Contoh: 165",
            input_filter="float"
        )
        fields["weight_kg"] = self._add_form_field(
            content, "Berat badan (kg) — opsional", "Contoh: 55",
            input_filter="float"
        )

        content.add_widget(self._form_label("Pengalaman olahraga"))
        experience = Spinner(
            text="Tidak ditentukan", values=list(self.EXPERIENCE_OPTIONS),
            size_hint_y=None, height=dp(46),
            background_normal="", background_color=self.palette["surface"],
            color=self.palette["text"], font_size="13sp",
        )
        content.add_widget(experience)
        fields["experience_level"] = experience

        content.add_widget(self._form_label("Preferensi latihan"))
        training = Spinner(
            text="Keduanya", values=list(self.TRAINING_OPTIONS),
            size_hint_y=None, height=dp(46),
            background_normal="", background_color=self.palette["surface"],
            color=self.palette["text"], font_size="13sp",
        )
        content.add_widget(training)
        fields["preferred_training_mode"] = training

        message = Label(
            text="", color=self.palette["muted"], font_size="12sp",
            size_hint_y=None, height=dp(42), halign="left",
        )
        content.add_widget(message)
        fields["message"] = message

        save_button = FTButton(
            "Simpan dan lanjutkan" if form_name == "Onboarding"
            else "Simpan perubahan", self.palette,
        )
        save_button.bind(on_release=lambda *_: self._save_profile_form(form_name))
        content.add_widget(save_button)

        if form_name == "Onboarding":
            skip_button = FTButton("Lewati pengaturan profil", self.palette)
            skip_button.bind(on_release=lambda *_: self.go_to("Home"))
            content.add_widget(skip_button)
        else:
            export_button = FTButton("Ekspor data saya (JSON)", self.palette)
            export_button.bind(on_release=lambda *_: self.export_user_data())
            content.add_widget(export_button)
            delete_button = FTButton("Hapus semua data", self.palette)
            delete_button.bind(on_release=lambda *_: self.request_delete_data())
            content.add_widget(delete_button)
            fields["delete_button"] = delete_button

        self.profile_forms[form_name] = fields
        scroll.add_widget(content)
        page.add_widget(scroll)

    def _form_label(self, text):
        return Label(
            text=text, color=self.palette["text"], font_size="13sp",
            size_hint_y=None, height=dp(24), halign="left",
        )

    def _add_form_field(self, content, label_text, hint_text,
                        input_filter=None):
        content.add_widget(self._form_label(label_text))
        field = FTInput(
            self.palette, hint_text=hint_text, input_filter=input_filter,
            font_size="14sp",
        )
        content.add_widget(field)
        return field

    def _save_profile_form(self, form_name):
        fields = self.profile_forms[form_name]
        values = {
            "display_name": fields["display_name"].text,
            "height_cm": fields["height_cm"].text,
            "weight_kg": fields["weight_kg"].text,
            "experience_level": self.EXPERIENCE_OPTIONS.get(
                fields["experience_level"].text, "unspecified"
            ),
            "preferred_training_mode": self.TRAINING_OPTIONS.get(
                fields["preferred_training_mode"].text, "both"
            ),
        }
        try:
            self.profile_repository.save_profile(values)
        except ProfileValidationError as error:
            fields["message"].text = str(error)
            fields["message"].color = (0.8, 0.2, 0.2, 1)
            return
        fields["message"].text = "Profil berhasil disimpan."
        fields["message"].color = self.palette["accent"]
        self._load_profile_form()
        if form_name == "Onboarding":
            self.go_to("Home")

    def _load_profile_form(self):
        profile = self.profile_repository.get_profile()
        fields = self.profile_forms.get("Profile")
        if not fields or not profile:
            return
        fields["display_name"].text = profile["display_name"]
        fields["height_cm"].text = (
            str(profile["height_cm"]) if profile["height_cm"] is not None else ""
        )
        fields["weight_kg"].text = (
            str(profile["weight_kg"]) if profile["weight_kg"] is not None else ""
        )
        experience_labels = {
            value: label for label, value in self.EXPERIENCE_OPTIONS.items()
        }
        training_labels = {
            value: label for label, value in self.TRAINING_OPTIONS.items()
        }
        fields["experience_level"].text = experience_labels[
            profile["experience_level"]
        ]
        fields["preferred_training_mode"].text = training_labels[
            profile["preferred_training_mode"]
        ]

    def export_user_data(self):
        """Export the local database to a JSON file in app-private storage."""
        export_dir = Path(self.user_data_dir) / "exports"
        filename = (
            "fittrack-export-" + datetime.now().strftime("%Y%m%d-%H%M%S")
            + ".json"
        )
        destination = self.data_manager.export_json(export_dir / filename)
        fields = self.profile_forms.get("Profile")
        if fields:
            fields["message"].text = f"Ekspor tersimpan: {destination}"
        return destination

    def request_delete_data(self):
        """Require a second tap before deleting all local user records."""
        fields = self.profile_forms.get("Profile")
        if not self.delete_confirmation_pending:
            self.delete_confirmation_pending = True
            if fields:
                fields["delete_button"].text = "Konfirmasi hapus semua data"
                fields["message"].text = (
                    "Tekan sekali lagi untuk menghapus seluruh data lokal."
                )
            return False

        self.data_manager.delete_all_data()
        self.delete_confirmation_pending = False
        if fields:
            fields["delete_button"].text = "Hapus semua data"
            fields["message"].text = "Semua data lokal telah dihapus."
        self.go_to("Onboarding")
        return True

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
            if isinstance(widget, FTInput):
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
