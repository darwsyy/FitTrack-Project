# Changelog

## Unreleased

### Added
- Added the initial Kivy app shell with Home, Cardio, Workout, Food, and Sleep navigation.
- Added Profile and Settings placeholder pages.
- Added light and dark presentation palettes.
- Added reusable card, button, text input, chart container, empty state, and loading state components.
- Added initial Home dashboard placeholders with explicit no-data messaging.
- Documented initial UI direction, design tokens, and Phase 1 manual test steps.

### Tests
- Added app shell, navigation, theme toggle, and reusable component tests.
- Latest automated result: 4 tests passed.


### Fixed
- Fixed theme switching to update existing widgets in place instead of rebuilding the root application.
- Preserved the active page and navigation state when switching light/dark themes.
- Added a portrait desktop preview configuration (390 x 844 px) to make mobile-first layout checks easier.
- Updated UI guidance to distinguish desktop preview from actual Android device validation.


## Phase 2 — Onboarding & Local Database

### Added
- Added versioned SQLite schema migration (v1) and foreign-key enforcement.
- Added local profile repository and input validation.
- Added first-run onboarding and editable profile screen.
- Added optional height/weight measurement history.
- Added JSON export and two-step local data deletion.
- Added database, validation, persistence, export, deletion, and UI tests.
- Documented database and privacy behavior.


### UI access fix
- Added a visible Setelan button to the top bar so users can open Settings and reach the light/dark theme control.
- Added a regression test for opening Settings from the top bar.


## Phase 3 - Workout Module (implementation ready for manual review)

### Added
- Added SQLite schema migration v2 for exercise catalogue, workout templates, sessions, session exercises, and sets.
- Added a seeded exercise catalogue for gym and home training.
- Added PPL, Upper/Lower, Full Body, and home workout templates.
- Added custom routine creation.
- Added workout session creation from a template or an empty session.
- Added exercise selection and set logging with reps, optional weight, and duration.
- Added session completion rules, history, and session detail display.
- Added Workout screen UI and local persistence.

### Tests
- Added repository tests for catalogue seeding, template filtering, custom routines, session persistence, set validation, completion, history, and deletion cascade.
- Added UI integration tests for workout navigation, session logging, and custom routine creation.
- Added migration v3 to safely add `workout_templates.user_id` to existing v2 databases without deleting user data.
- Added a regression test that upgrades a legacy v2 database and verifies existing template data is preserved.
- Fixed the migration to tolerate fresh v2 databases where the column is already present.
- Latest automated verification after the fix: 37 tests passed; compileall, pip check, and git diff --check passed.
- Existing desktop database upgraded to schema v3; existing profile record was preserved.
- Manual UI review is still required before Phase 3 is marked complete.
