"""Input validation for onboarding and profile editing."""
import math


class ProfileValidationError(ValueError):
    """Raised when profile input is missing or invalid."""


EXPERIENCE_LEVELS = {"unspecified", "beginner", "intermediate", "advanced"}
TRAINING_MODES = {"gym", "home", "both"}


def _optional_positive_number(value, field_name, maximum):
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ProfileValidationError(
            f"{field_name} harus berupa angka."
        ) from exc
    if not math.isfinite(number) or number <= 0 or number > maximum:
        raise ProfileValidationError(
            f"{field_name} harus lebih dari 0 dan tidak melebihi {maximum:g}."
        )
    return number


def validate_profile(values):
    """Normalize and validate profile fields without judging body metrics."""
    display_name = str(values.get("display_name", "")).strip()
    if not display_name:
        raise ProfileValidationError("Nama tampilan wajib diisi.")
    if len(display_name) > 40:
        raise ProfileValidationError("Nama tampilan maksimal 40 karakter.")

    experience_level = values.get("experience_level") or "unspecified"
    training_mode = values.get("preferred_training_mode") or "both"
    if experience_level not in EXPERIENCE_LEVELS:
        raise ProfileValidationError("Pilihan pengalaman olahraga tidak valid.")
    if training_mode not in TRAINING_MODES:
        raise ProfileValidationError("Pilihan jenis latihan tidak valid.")

    return {
        "display_name": display_name,
        "experience_level": experience_level,
        "preferred_training_mode": training_mode,
        "height_cm": _optional_positive_number(
            values.get("height_cm"), "Tinggi badan", 250
        ),
        "weight_kg": _optional_positive_number(
            values.get("weight_kg"), "Berat badan", 500
        ),
    }
