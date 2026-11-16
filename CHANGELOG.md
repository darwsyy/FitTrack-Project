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
