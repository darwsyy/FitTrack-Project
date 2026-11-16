"""Persistence and business rules for workout sessions."""
from datetime import datetime, timezone
from uuid import uuid4


class WorkoutValidationError(ValueError):
    """Raised when workout data is invalid."""


EXERCISE_SEEDS = (
    ("Push-up", "chest", "bodyweight", "home", "Jaga tubuh tetap lurus dan turunkan badan dengan kontrol."),
    ("Incline Push-up", "chest", "bench", "home", "Gunakan permukaan stabil dan jaga tubuh tetap lurus."),
    ("Knee Push-up", "chest", "bodyweight", "home", "Pertahankan posisi tubuh stabil selama gerakan."),
    ("Squat", "legs", "bodyweight", "both", "Turun sesuai rentang gerak yang nyaman dan jaga keseimbangan."),
    ("Lunge", "legs", "bodyweight", "both", "Langkahkan kaki dengan stabil dan kontrol gerakan."),
    ("Plank", "core", "bodyweight", "home", "Pertahankan posisi netral dan hentikan jika terasa nyeri."),
    ("Chest Press", "chest", "machine", "gym", "Atur beban yang dapat dikendalikan dengan teknik baik."),
    ("Chest Fly", "chest", "machine", "gym", "Gunakan rentang gerak nyaman tanpa memaksa bahu."),
    ("Shoulder Press", "shoulders", "dumbbell", "gym", "Jaga posisi punggung stabil dan gerakkan dengan kontrol."),
    ("Lat Pulldown", "back", "machine", "gym", "Tarik pegangan ke arah dada tanpa mengayun."),
    ("Seated Row", "back", "machine", "gym", "Tarik ke arah badan sambil menjaga posisi punggung."),
    ("Leg Curl", "legs", "machine", "gym", "Gerakkan beban dengan perlahan dan terkontrol."),
    ("Glute Bridge", "glutes", "bodyweight", "home", "Angkat pinggul dengan kontrol tanpa melengkungkan punggung berlebihan."),
    ("Dead Bug", "core", "bodyweight", "home", "Gerakkan sisi berlawanan secara perlahan dengan punggung stabil."),
)

TEMPLATE_SEEDS = (
    ("PPL - Push", "Fokus gerakan dorong; pilihan template, bukan kewajiban.", "gym", ("Push-up", "Chest Press", "Shoulder Press", "Chest Fly")),
    ("PPL - Pull", "Fokus gerakan tarik; sesuaikan dengan alat yang tersedia.", "gym", ("Lat Pulldown", "Seated Row")),
    ("PPL - Legs", "Fokus latihan kaki dengan gerakan yang tersedia.", "gym", ("Squat", "Lunge", "Leg Curl", "Glute Bridge")),
    ("Upper Body", "Template tubuh bagian atas.", "gym", ("Push-up", "Seated Row", "Shoulder Press", "Lat Pulldown")),
    ("Lower Body", "Template tubuh bagian bawah.", "gym", ("Squat", "Lunge", "Glute Bridge", "Leg Curl")),
    ("Full Body", "Template latihan seluruh tubuh.", "gym", ("Squat", "Push-up", "Seated Row", "Plank")),
    ("Home Full Body", "Pilihan latihan berat badan di rumah.", "home", ("Squat", "Push-up", "Glute Bridge", "Plank")),
    ("Home Lower Body", "Pilihan latihan kaki di rumah.", "home", ("Squat", "Lunge", "Glute Bridge")),
)


def _now():
    return datetime.now(timezone.utc).isoformat()


class WorkoutRepository:
    """Stores catalogue, templates, sessions, exercises, and completed sets."""

    def __init__(self, database):
        self.database = database
        self.seed_catalogue()

    def seed_catalogue(self):
        now = _now()
        with self.database.connect() as connection:
            for name, category, equipment, mode, instructions in EXERCISE_SEEDS:
                connection.execute(
                    """INSERT OR IGNORE INTO exercises
                       (id, name, category, equipment, training_mode, instructions)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (str(uuid4()), name, category, equipment, mode, instructions),
                )
            exercise_ids = {
                row["name"]: row["id"]
                for row in connection.execute("SELECT id, name FROM exercises")
            }
            for name, description, mode, exercise_names in TEMPLATE_SEEDS:
                template_id = connection.execute(
                    "SELECT id FROM workout_templates WHERE name = ?", (name,)
                ).fetchone()
                if template_id:
                    continue
                template_id = str(uuid4())
                connection.execute(
                    """INSERT INTO workout_templates
                       (id, name, description, training_mode, is_custom, created_at)
                       VALUES (?, ?, ?, ?, 0, ?)""",
                    (template_id, name, description, mode, now),
                )
                for index, exercise_name in enumerate(exercise_names):
                    connection.execute(
                        """INSERT INTO template_exercises
                           (id, template_id, exercise_id, sort_order)
                           VALUES (?, ?, ?, ?)""",
                        (str(uuid4()), template_id, exercise_ids[exercise_name], index),
                    )

    def list_exercises(self, training_mode=None):
        query = "SELECT * FROM exercises WHERE is_active = 1"
        params = ()
        if training_mode in ("gym", "home"):
            query += " AND training_mode IN (?, 'both')"
            params = (training_mode,)
        query += " ORDER BY category, name"
        with self.database.connect() as connection:
            return [dict(row) for row in connection.execute(query, params)]

    def list_templates(self, training_mode=None):
        with self.database.connect() as connection:
            user = connection.execute(
                "SELECT id FROM users ORDER BY created_at LIMIT 1"
            ).fetchone()
            if user:
                clauses = ["(is_custom = 0 OR user_id = ?)"]
                params = [user["id"]]
            else:
                clauses = ["is_custom = 0"]
                params = []
            if training_mode in ("gym", "home"):
                clauses.append("training_mode IN (?, 'both')")
                params.append(training_mode)
            query = (
                "SELECT * FROM workout_templates WHERE "
                + " AND ".join(clauses) + " ORDER BY is_custom, name"
            )
            return [dict(row) for row in connection.execute(query, params)]

    def create_custom_template(self, name, training_mode, exercise_ids, description=""):
        name = str(name).strip()
        if not name:
            raise WorkoutValidationError("Nama routine wajib diisi.")
        if training_mode not in ("gym", "home"):
            raise WorkoutValidationError("Mode latihan tidak valid.")
        if not exercise_ids:
            raise WorkoutValidationError("Pilih minimal satu exercise.")
        user_id = self._user_id()
        template_id = str(uuid4())
        with self.database.connect() as connection:
            for exercise_id in exercise_ids:
                row = connection.execute(
                    """SELECT id, training_mode FROM exercises
                       WHERE id = ? AND is_active = 1""",
                    (exercise_id,),
                ).fetchone()
                if not row:
                    raise WorkoutValidationError("Exercise tidak ditemukan.")
                if row["training_mode"] not in (training_mode, "both"):
                    raise WorkoutValidationError(
                        "Exercise tidak sesuai dengan mode routine."
                    )
            connection.execute(
                """INSERT INTO workout_templates
                   (id, name, user_id, description, training_mode,
                    is_custom, created_at)
                   VALUES (?, ?, ?, ?, ?, 1, ?)""",
                (template_id, name, user_id, str(description).strip(),
                 training_mode, _now()),
            )
            for index, exercise_id in enumerate(exercise_ids):
                connection.execute(
                    """INSERT INTO template_exercises
                       (id, template_id, exercise_id, sort_order)
                       VALUES (?, ?, ?, ?)""",
                    (str(uuid4()), template_id, exercise_id, index),
                )
        return template_id

    def _user_id(self):
        with self.database.connect() as connection:
            row = connection.execute(
                "SELECT id FROM users ORDER BY created_at LIMIT 1"
            ).fetchone()
        if not row:
            raise WorkoutValidationError("Selesaikan onboarding sebelum memulai workout.")
        return row["id"]

    def get_active_session(self):
        """Return the user's unfinished session, if one exists."""
        try:
            user_id = self._user_id()
        except WorkoutValidationError:
            return None
        with self.database.connect() as connection:
            row = connection.execute(
                """SELECT id FROM workout_sessions
                   WHERE user_id = ? AND status = 'in_progress'
                   ORDER BY started_at DESC LIMIT 1""",
                (user_id,),
            ).fetchone()
        return self.get_session(row["id"]) if row else None

    def start_session(self, name="Workout", training_mode="gym", template_id=None):
        name = str(name).strip() or "Workout"
        if training_mode not in ("gym", "home"):
            raise WorkoutValidationError("Mode latihan harus gym atau home.")
        user_id = self._user_id()
        session_id = str(uuid4())
        now = _now()
        with self.database.connect() as connection:
            active = connection.execute(
                """SELECT id FROM workout_sessions
                   WHERE user_id = ? AND status = 'in_progress' LIMIT 1""",
                (user_id,),
            ).fetchone()
            if active:
                raise WorkoutValidationError(
                    "Selesaikan atau lanjutkan sesi aktif sebelum memulai sesi baru."
                )
            if template_id:
                template = connection.execute(
                    """SELECT * FROM workout_templates
                       WHERE id = ? AND (is_custom = 0 OR user_id = ?)""",
                    (template_id, user_id),
                ).fetchone()
                if not template:
                    raise WorkoutValidationError("Template tidak ditemukan.")
                name = template["name"]
                training_mode = (
                    "home" if template["training_mode"] == "home" else training_mode
                )
            connection.execute(
                """INSERT INTO workout_sessions
                   (id, user_id, template_id, name, training_mode, started_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (session_id, user_id, template_id, name, training_mode, now),
            )
            if template_id:
                rows = connection.execute(
                    """SELECT exercise_id FROM template_exercises
                       WHERE template_id = ? ORDER BY sort_order""",
                    (template_id,),
                ).fetchall()
                for index, row in enumerate(rows):
                    self._insert_session_exercise(
                        connection, session_id, row["exercise_id"], index
                    )
        return self.get_session(session_id)

    @staticmethod
    def _insert_session_exercise(connection, session_id, exercise_id, sort_order):
        exercise = connection.execute(
            "SELECT id FROM exercises WHERE id = ? AND is_active = 1",
            (exercise_id,),
        ).fetchone()
        if not exercise:
            raise WorkoutValidationError("Exercise tidak ditemukan.")
        existing = connection.execute(
            """SELECT id FROM workout_session_exercises
               WHERE session_id = ? AND exercise_id = ?""",
            (session_id, exercise_id),
        ).fetchone()
        if existing:
            return existing["id"]
        exercise_session_id = str(uuid4())
        connection.execute(
            """INSERT INTO workout_session_exercises
               (id, session_id, exercise_id, sort_order)
               VALUES (?, ?, ?, ?)""",
            (exercise_session_id, session_id, exercise_id, sort_order),
        )
        return exercise_session_id

    def add_exercise(self, session_id, exercise_id):
        with self.database.connect() as connection:
            session = connection.execute(
                """SELECT status, training_mode FROM workout_sessions
                   WHERE id = ?""",
                (session_id,),
            ).fetchone()
            if not session or session["status"] != "in_progress":
                raise WorkoutValidationError("Sesi tidak aktif.")
            exercise = connection.execute(
                """SELECT training_mode FROM exercises
                   WHERE id = ? AND is_active = 1""",
                (exercise_id,),
            ).fetchone()
            if not exercise:
                raise WorkoutValidationError("Exercise tidak ditemukan.")
            if exercise["training_mode"] not in (
                session["training_mode"], "both"
            ):
                raise WorkoutValidationError(
                    "Exercise tidak sesuai dengan mode sesi."
                )
            order = connection.execute(
                """SELECT COALESCE(MAX(sort_order), -1) + 1 AS next_order
                   FROM workout_session_exercises WHERE session_id = ?""",
                (session_id,),
            ).fetchone()["next_order"]
            return self._insert_session_exercise(
                connection, session_id, exercise_id, order
            )

    def add_set(self, session_exercise_id, reps=None, weight_kg=None,
                duration_seconds=None, distance_m=None, is_completed=True):
        try:
            reps = int(reps) if reps not in (None, "") else None
            weight_kg = float(weight_kg) if weight_kg not in (None, "") else None
            duration_seconds = (
                int(duration_seconds) if duration_seconds not in (None, "") else None
            )
            distance_m = float(distance_m) if distance_m not in (None, "") else None
        except (TypeError, ValueError) as error:
            raise WorkoutValidationError("Nilai set harus berupa angka yang valid.") from error
        if reps is not None and reps <= 0:
            raise WorkoutValidationError("Repetisi harus lebih dari 0.")
        if weight_kg is not None and weight_kg < 0:
            raise WorkoutValidationError("Beban tidak boleh negatif.")
        if duration_seconds is not None and duration_seconds <= 0:
            raise WorkoutValidationError("Durasi harus lebih dari 0 detik.")
        if distance_m is not None and distance_m <= 0:
            raise WorkoutValidationError("Jarak harus lebih dari 0 meter.")
        if all(value is None for value in (reps, duration_seconds, distance_m)):
            raise WorkoutValidationError("Isi repetisi, durasi, atau jarak.")
        set_id = str(uuid4())
        with self.database.connect() as connection:
            row = connection.execute(
                """SELECT se.session_id, ws.status
                   FROM workout_session_exercises se
                   JOIN workout_sessions ws ON ws.id = se.session_id
                   WHERE se.id = ?""",
                (session_exercise_id,),
            ).fetchone()
            if not row or row["status"] != "in_progress":
                raise WorkoutValidationError("Exercise tidak berada pada sesi aktif.")
            number = connection.execute(
                """SELECT COALESCE(MAX(set_number), 0) + 1 AS next_number
                   FROM workout_sets WHERE session_exercise_id = ?""",
                (session_exercise_id,),
            ).fetchone()["next_number"]
            connection.execute(
                """INSERT INTO workout_sets
                   (id, session_exercise_id, set_number, reps, weight_kg,
                    duration_seconds, distance_m, is_completed)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (set_id, session_exercise_id, number, reps, weight_kg,
                 duration_seconds, distance_m, int(bool(is_completed))),
            )
        return set_id

    def finish_session(self, session_id, notes=""):
        with self.database.connect() as connection:
            row = connection.execute(
                "SELECT status FROM workout_sessions WHERE id = ?", (session_id,)
            ).fetchone()
            if not row or row["status"] != "in_progress":
                raise WorkoutValidationError("Sesi tidak ditemukan atau sudah selesai.")
            count = connection.execute(
                """SELECT COUNT(*) AS total FROM workout_sets ws
                   JOIN workout_session_exercises se
                     ON se.id = ws.session_exercise_id
                   WHERE se.session_id = ? AND ws.is_completed = 1""",
                (session_id,),
            ).fetchone()["total"]
            if count == 0:
                raise WorkoutValidationError("Catat minimal satu set selesai sebelum mengakhiri sesi.")
            connection.execute(
                """UPDATE workout_sessions SET status = 'completed',
                   finished_at = ?, notes = ? WHERE id = ?""",
                (_now(), str(notes).strip(), session_id),
            )
        return self.get_session(session_id)

    def get_session(self, session_id):
        with self.database.connect() as connection:
            session = connection.execute(
                """SELECT ws.*, u.display_name FROM workout_sessions ws
                   JOIN users u ON u.id = ws.user_id WHERE ws.id = ?""",
                (session_id,),
            ).fetchone()
            if not session:
                return None
            result = dict(session)
            exercises = connection.execute(
                """SELECT se.id AS session_exercise_id, se.sort_order,
                          e.id AS exercise_id, e.name, e.category, e.equipment
                   FROM workout_session_exercises se
                   JOIN exercises e ON e.id = se.exercise_id
                   WHERE se.session_id = ? ORDER BY se.sort_order""",
                (session_id,),
            ).fetchall()
            result["exercises"] = []
            for exercise in exercises:
                item = dict(exercise)
                item["sets"] = [
                    dict(row) for row in connection.execute(
                        """SELECT * FROM workout_sets
                           WHERE session_exercise_id = ? ORDER BY set_number""",
                        (item["session_exercise_id"],),
                    )
                ]
                result["exercises"].append(item)
        return result

    def list_history(self, limit=50):
        with self.database.connect() as connection:
            rows = connection.execute(
                """SELECT ws.id, ws.name, ws.training_mode, ws.started_at,
                          ws.finished_at, ws.status,
                          COUNT(DISTINCT se.id) AS exercise_count,
                          COUNT(s.id) AS completed_sets
                   FROM workout_sessions ws
                   LEFT JOIN workout_session_exercises se ON se.session_id = ws.id
                   LEFT JOIN workout_sets s
                     ON s.session_exercise_id = se.id AND s.is_completed = 1
                   WHERE ws.status = 'completed'
                   GROUP BY ws.id
                   ORDER BY ws.started_at DESC LIMIT ?""",
                (int(limit),),
            ).fetchall()
        return [dict(row) for row in rows]
