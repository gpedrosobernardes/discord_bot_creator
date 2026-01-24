import qtawesome
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QMainWindow,
    QTabWidget,
    QSplitter,
    QToolButton,
    QListView,
    QLineEdit,
    QMenu,
    QMenuBar,
    QHBoxLayout,
)
from qextrawidgets import QColorButton, QPasswordLineEdit, QSearchLineEdit

from source.qt.widgets.groups_list import QGroupsList
from source.qt.widgets.log_textedit import QLogTextEdit


class MainView(QMainWindow):
    """
    Main Window View for the Discord Bot Creator application.

    This class handles the main UI layout, including the menu bar,
    tabs for messages and groups, and the configuration panel.
    """

    def __init__(self):
        """Initializes the MainView."""
        super().__init__()

        self._init_ui()
        self._init_layout()
        self.translate_ui()

    def _init_ui(self):
        """Initialize widgets and configure their properties."""
        self.setMinimumSize(800, 600)
        self.resize(1000, 800)
        self.setWindowIcon(QIcon("assets/icons/window-icon.svg"))
        self.setWindowTitle("Discord Bot Creator")

        self._init_menus()
        self._init_controls()

    def _init_menus(self):
        """Initialize the menu bar and menus."""
        self.menu_bar = QMenuBar()
        self.setMenuBar(self.menu_bar)

        self.project_menu = QMenu(self.menu_bar)
        self.edit_menu = QMenu(self.menu_bar)
        self.help_menu = QMenu(self.menu_bar)

        self.menu_bar.addMenu(self.project_menu)
        self.menu_bar.addMenu(self.edit_menu)
        self.menu_bar.addMenu(self.help_menu)

    def _init_controls(self):
        """Initialize all UI controls."""
        # --- Left Side: Groups Tab ---
        self.search_groups = QSearchLineEdit()
        self.groups_list_widget = QGroupsList()
        self.config_group_button = QToolButton()
        self.quit_group_button = QToolButton()
        self.generate_invite_button = QToolButton()

        # --- Left Side: Messages Tab ---
        self.search_messages_line_edit = QSearchLineEdit()
        self.messages_list_view = QListView()

        self.new_message_tool_button = QToolButton()
        self.edit_message_tool_button = QToolButton()
        self.remove_message_tool_button = QToolButton()
        self.remove_all_message_tool_button = QToolButton()

        self.left_tab_widget = QTabWidget()
        self.left_tab_widget.setMinimumWidth(280)

        # --- Right Side ---
        self.logs_text_edit = QLogTextEdit()
        self.cmd_line_edit = QLineEdit()

        self.token_label = QLabel()
        self.token_line_edit = QPasswordLineEdit()
        self.token_line_edit.setMaxLength(100)
        
        # Bot Info Widget (Icon + Name)
        self.bot_info_widget = QWidget()
        self.bot_info_widget.setVisible(False)

        self.bot_icon_label = QLabel()
        self.bot_icon_label.setFixedSize(32, 32)
        self.bot_icon_label.setScaledContents(True)

        self.bot_name_label = QLabel()

        self._init_switch_button()

    def _init_switch_button(self):
        """Initialize the switch bot button with icons."""
        switch_icon = QIcon()
        pixmap_play = qtawesome.icon("fa6s.play").pixmap(QSize(48, 48))
        switch_icon.addPixmap(pixmap_play, QIcon.Mode.Normal, QIcon.State.Off)

        pixmap_stop = qtawesome.icon("fa6s.stop").pixmap(QSize(48, 48))
        switch_icon.addPixmap(pixmap_stop, QIcon.Mode.Normal, QIcon.State.On)

        self.switch_bot_button = QColorButton("#599E5E", "", "white", "#C94F4F")
        self.switch_bot_button.setCheckable(True)
        self.switch_bot_button.setIcon(switch_icon)

    def _init_layout(self):
        """Initialize Layouts and add widgets to them."""
        # Setup Bot Info Widget Layout
        bot_info_layout = QHBoxLayout(self.bot_info_widget)
        bot_info_layout.setContentsMargins(0, 0, 0, 0)
        bot_info_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bot_info_layout.addWidget(self.bot_icon_label)
        bot_info_layout.addWidget(self.bot_name_label)

        # 1. Create Left Panel (Tabs)
        messages_tab = self._create_messages_tab()
        groups_tab = self._create_groups_tab()

        self.left_tab_widget.addTab(messages_tab, "")
        self.left_tab_widget.addTab(groups_tab, "")

        # 2. Create Right Panel
        right_panel = self._create_right_panel()

        # 3. Main Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.left_tab_widget)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(1, 1)

        self.setCentralWidget(splitter)

    def _create_messages_tab(self) -> QWidget:
        """Create the messages tab widget."""
        # Toolbar
        toolbar_layout = QHBoxLayout()
        toolbar_layout.addStretch()
        for btn in (
            self.new_message_tool_button,
            self.edit_message_tool_button,
            self.remove_message_tool_button,
            self.remove_all_message_tool_button,
        ):
            toolbar_layout.addWidget(btn)

        # Main Layout
        layout = QVBoxLayout()
        layout.addWidget(self.search_messages_line_edit)
        layout.addWidget(self.messages_list_view)
        layout.addLayout(toolbar_layout)

        container = QWidget()
        container.setContentsMargins(5, 5, 5, 5)
        container.setLayout(layout)
        return container

    def _create_groups_tab(self) -> QWidget:
        """Create the groups tab widget."""
        # Toolbar
        toolbar_layout = QHBoxLayout()
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.config_group_button)
        toolbar_layout.addWidget(self.quit_group_button)
        toolbar_layout.addWidget(self.generate_invite_button)

        # Main Layout
        layout = QVBoxLayout()
        layout.addWidget(self.search_groups)
        layout.addWidget(self.groups_list_widget)
        layout.addLayout(toolbar_layout)

        container = QWidget()
        container.setContentsMargins(5, 5, 5, 5)
        container.setLayout(layout)
        return container

    def _create_right_panel(self) -> QWidget:
        """Create the right panel widget."""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        widgets = (
            self.logs_text_edit,
            self.cmd_line_edit,
            self.token_label,
            self.token_line_edit,
            self.bot_info_widget,
            self.switch_bot_button,
        )

        for widget in widgets:
            layout.addWidget(widget)

        container = QWidget()
        container.setMinimumWidth(520)
        container.setLayout(layout)
        return container

    def translate_ui(self):
        """Translate UI texts."""
        # Menus
        self.project_menu.setTitle(self.tr("Project"))
        self.edit_menu.setTitle(self.tr("Edit"))
        self.help_menu.setTitle(self.tr("Help"))

        # Tabs
        self.left_tab_widget.setTabText(0, self.tr("Messages"))
        self.left_tab_widget.setTabText(1, self.tr("Groups"))

        # Search Placeholders
        self.search_messages_line_edit.setPlaceholderText(self.tr("Search messages..."))
        self.search_groups.setPlaceholderText(self.tr("Search groups..."))

        # Right Panel
        self.cmd_line_edit.setPlaceholderText(self.tr("Type a command"))
        self.token_label.setText(self.tr("Token"))
        self.switch_bot_button.setText(self.tr("Turn on/off bot"))
        self.logs_text_edit.setPlaceholderText(self.tr("No logs at moment"))
