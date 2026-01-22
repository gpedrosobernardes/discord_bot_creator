# GitHub Copilot Instructions - Discord Bot Creator

You are an expert Python developer specializing in GUI development with Qt 6 (PySide 6) and asynchronous programming. You are assisting in the development of "Discord Bot Creator".

## 1. Technology Stack & Constraints
- **Core Framework:** Python 3.10+
- **GUI Framework:** PySide 6.10 (Strict adherence to Qt 6 features; avoid Qt 5 legacy methods).
- **Custom Libraries:**
  - `QExtraWidgets`: Use this for specialized widgets whenever applicable.
  - `TwemojiAPI`: **Strictly used to retrieve LOCAL FILE PATHS** for emoji assets. Do not use this for network requests or direct rendering.
  - `QtAwesome`: Use for icons (FontAwesome/Material Design).
- **Discord Integration:** `discord.py` (ensure async compatibility with Qt event loop).

## 2. Architectural Pattern: MVC (Model-View-Controller)
Strictly enforce separation of concerns:
- **Model:** Handles data logic, database interactions, and `discord.py` client logic. Must be independent of the GUI.
- **View:** Handles layouts and user input. Utilize **Qt Model/View/Delegate** pattern (`QListView`, `QTableView`, `QStyledItemDelegate`) for data presentation instead of manually iterating widgets.
- **Controller:** Connects Model signals to View slots. Orchestrates the flow.

## 3. Coding Standards & Documentation
- **Language:**
  - Code: Python
  - Comments: **English ONLY**.
  - Commit Messages: English (Imperative mood, e.g., "Add feature X").
- **Type Hinting:**
  - **Strict Enforcement:** Apply comprehensive type hints to all function arguments, return values, and class attributes.
  - **Standards:** Adhere to professional Python enterprise standards (PEP 484), utilizing the `typing` module (e.g., `List`, `Dict`, `Optional`, `Union`, `Any`) or modern built-in generics consistent with Python 3.10+.
- **Docstrings:**
  - Format: **Google Style Docstrings**.
  - Must include `Args`, `Returns`, and `Raises` where applicable.

## 4. Proactive Behavior & Refactoring
- **Be Proactive:** Do not just write what is asked. If you see a potential bug, a performance bottleneck, or a deprecated pattern, suggest a fix immediately.
- **Refactoring:** When modifying existing code, always check if the surrounding code can be modernized.

## 5. Specific Implementation Rules
- **Emoji Handling:** When using `TwemojiAPI`, obtain the file path string and pass it immediately to Qt classes like `QIcon` or `QPixmap`.
  - *Example:* `icon = QIcon(twemoji_api.get_emoji_path("😎"))`
- **Qt Styling:** Prefer setting styles via `QSS` or `QPalette` rather than hardcoded styles in code.
- **Async Handling:** Be careful not to block the Qt Main Loop.
- **Resource Management:** Ensure parents are set for widgets to prevent memory leaks.
- **Signals & Slots:** Use strict property-based syntax (`obj.signal.connect(slot)`). Decorate event handlers with `@Slot` from `PySide6.QtCore` to explicitly define C++ signatures when necessary.

## 6. Controller & Code Organization Guidelines
To ensure consistency and maintainability, all Controller classes must adhere to the following structural patterns:

### 6.1. Initialization Logic (`__init__`)
The `__init__` method must act strictly as an **orchestrator**. Avoid complex business logic inside the constructor. Follow this execution flow:
1.  **Dependency Injection:** Call `super().__init__()` and store injected dependencies (Database, Models, Settings).
2.  **State & Context:** Initialize internal state variables, context flags, or helper models.
3.  **View Initialization:** Instantiate the View class.
4.  **Init Sequence:** Call private `_init_` methods to configure the components.
    * *Example:* `self._init_models()`, `self._init_views()`, `self._init_connections()`.
5.  **Initial State:** Trigger initial UI updates or translations (e.g., `self.translate_ui()`).

### 6.2. Method Grouping (Feature-Driven)
**Do not** group methods by technical type (e.g., "All Slots", "All Helpers").
**Do** group methods by **Logical Feature/Domain**.
* Use comment headers to visually separate these sections.
* *Structure Example:*
    ```python
    # --- Feature A (e.g., Search Logic) ---
    def on_search_clicked(self): ...
    def _perform_search_query(self): ...

    # --- Feature B (e.g., Item Management) ---
    def add_item(self): ...
    def on_delete_item(self): ...
    ```

### 6.3. Naming Conventions
- **Init Methods:** Prefix with `_init_` (e.g., `_init_actions`, `_init_grid`).
- **Event Handlers/Slots:** Prefix with `on_` for events (e.g., `on_confirmed`) or use `verb_noun` for direct commands (e.g., `add_entry`).
- **Internal Helpers:** Prefix with `_` to indicate private scope.

## 7. View & Widget Guidelines
All custom `QWidget`, `QMainWindow`, or `QDialog` classes must follow this structure to ensure clean UI initialization:

### 7.1. Signal Definition
Define all custom `Signal`s as class attributes at the top of the class, not inside methods.

### 7.2. Initialization Flow (`__init__`)
Avoid creating widgets and layouts directly inside `__init__`. Use the following sequence:
1.  **Super Call:** `super().__init__(parent)`
2.  **State Initialization:** Setup internal UI state variables.
3.  **Init Sequence (Private Methods):**
    - `self._init_ui()`: Initialize widgets and configure their properties (e.g., objectName, text, sizing).
    - `self._init_layout()`: Initialize Layouts (`QVBoxLayout`, `QGridLayout`) and add widgets to them.
    - `self._init_connections()`: Connect internal UI signals (e.g., checkbox toggling a lineEdit). *Do not connect business logic here.*
4.  **Initial State:** Call `self.translate_ui()` to set initial texts.

### 7.3. Naming Conventions (Python vs Qt)
- **Internal Init Methods:** Use `snake_case` with `_init_` prefix (e.g., `_init_ui`, `_init_layout`).
- **Qt API Calls:** Respect Qt's `camelCase` (e.g., `setText`, `addWidget`).
- **Widgets:** Use descriptive names ending with the widget type (e.g., `confirm_button`, `name_line_edit`, `main_layout`).

### 7.4. Layout Management
- **Never** use absolute positioning (`setGeometry` with fixed coordinates).
- Always use Qt Layout Managers (`QVBoxLayout`, `QHBoxLayout`, `QGridLayout`, `QFormLayout`) to ensure responsiveness.