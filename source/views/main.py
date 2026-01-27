import qtawesome
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
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
    QGroupBox,
)
from qextrawidgets import QColorButton, QPasswordLineEdit, QSearchLineEdit
from qextrawidgets.icons import QThemeResponsiveIcon

from source.qt.helpers.pixmap import PixmapHelper
from source.qt.widgets.bot_info import BotInfoWidget
from source.qt.widgets.groups_list import QGroupsList
from source.qt.widgets.log_textedit import QLogTextEdit


class MainView(QMainWindow):
    """
    Main Window View for the Discord Bot Creator application.
    Refactored for better visual hierarchy and grouping.
    """

    def __init__(self):
        """Initializes the MainView."""
        super().__init__()

        self._init_ui()
        self._init_layout()
        self.translate_ui()

    def _init_ui(self):
        """Initialize widgets and configure their properties."""
        self.setMinimumSize(900, 650) # Aumentei um pouco o mínimo para conforto
        self.resize(1100, 800)
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
        self.messages_list_view.setEditTriggers(
            QListView.EditTrigger.DoubleClicked | QListView.EditTrigger.EditKeyPressed
        )

        self.new_message_tool_button = QToolButton()
        self.edit_message_tool_button = QToolButton()
        self.remove_message_tool_button = QToolButton()
        self.remove_all_message_tool_button = QToolButton()

        self.left_tab_widget = QTabWidget()
        self.left_tab_widget.setMinimumWidth(300)

        # --- Right Side ---
        self.logs_text_edit = QLogTextEdit()
        self.cmd_line_edit = QLineEdit()

        # Connection Group
        self.connection_group = QGroupBox() # Title defined in translate_ui
        self.token_label = QLabel()
        self.token_line_edit = QPasswordLineEdit()
        self.token_line_edit.setMaxLength(100)

        # Bot Info Widget (Icon + Name)
        self.bot_info_widget = BotInfoWidget()

        self.reset_bot_info()

        self._init_switch_button()

    def _init_switch_button(self):
        """Initialize the switch bot button with icons."""
        switch_icon = QThemeResponsiveIcon()
        pixmap_play = qtawesome.icon("fa6s.play", color="white").pixmap(QSize(24, 24))
        switch_icon.addPixmap(pixmap_play, QIcon.Mode.Normal, QIcon.State.Off)

        pixmap_stop = qtawesome.icon("fa6s.stop", color="white").pixmap(QSize(24, 24))
        switch_icon.addPixmap(pixmap_stop, QIcon.Mode.Normal, QIcon.State.On)

        # Ajustei as cores para ficarem mais suaves e profissionais
        self.switch_bot_button = QColorButton("#4CAF50", "", "white", "#F44336")
        self.switch_bot_button.setCheckable(True)
        self.switch_bot_button.setIcon(switch_icon)
        self.switch_bot_button.setMinimumHeight(45) # Botão mais robusto
        self.switch_bot_button.setCursor(Qt.CursorShape.PointingHandCursor)

    def _init_layout(self):
        """Initialize Layouts and add widgets to them."""
        # 1. Create Left Panel (Tabs)
        messages_tab = self._create_messages_tab()
        groups_tab = self._create_groups_tab()

        self.left_tab_widget.addTab(messages_tab, QThemeResponsiveIcon.fromAwesome("fa6s.message"), "")
        self.left_tab_widget.addTab(groups_tab, QThemeResponsiveIcon.fromAwesome("fa6s.users"), "")

        # 2. Create Right Panel
        right_panel = self._create_right_panel()

        # 3. Main Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.left_tab_widget)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1) # Esquerda cresce menos
        splitter.setStretchFactor(1, 3) # Direita tem prioridade de espaço (3x)

        self.setCentralWidget(splitter)

    def _create_messages_tab(self) -> QWidget:
        """Create the messages tab widget."""
        # Toolbar (Cleaned up)
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(2)
        toolbar_layout.addStretch()
        for btn in (
                self.new_message_tool_button,
                self.edit_message_tool_button,
                self.remove_message_tool_button,
                self.remove_all_message_tool_button,
        ):
            btn.setFixedSize(30, 30) # Tamanho uniforme
            toolbar_layout.addWidget(btn)

        # Main Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.addWidget(self.search_messages_line_edit)
        layout.addWidget(self.messages_list_view)
        layout.addLayout(toolbar_layout)

        container = QWidget()
        container.setLayout(layout)
        return container

    def _create_groups_tab(self) -> QWidget:
        """Create the groups tab widget."""
        # Toolbar
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(2)
        toolbar_layout.addStretch()
        for btn in (self.config_group_button, self.quit_group_button, self.generate_invite_button):
            btn.setFixedSize(30, 30)
            toolbar_layout.addWidget(btn)

        # Main Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.addWidget(self.search_groups)
        layout.addWidget(self.groups_list_widget)

        layout.addLayout(toolbar_layout)

        container = QWidget()
        container.setLayout(layout)
        return container

    def _create_right_panel(self) -> QWidget:
        """Create the right panel widget with improved grouping."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # --- Section 1: Connection Settings (Group Box) ---
        # Organiza o token dentro de uma caixa para não ficar "flutuando"
        conn_layout = QHBoxLayout()
        conn_layout.addWidget(self.token_label)
        conn_layout.addWidget(self.token_line_edit)
        self.connection_group.setLayout(conn_layout)

        # --- Section 2: Console (Logs + Command) ---
        console_layout = QVBoxLayout()
        console_layout.setSpacing(2) # Cmd colado no log
        console_layout.addWidget(QLabel(self.tr("System Logs:"))) # Label explícita
        console_layout.addWidget(self.logs_text_edit)
        console_layout.addWidget(self.cmd_line_edit)

        # --- Section 3: Action Area (Bot Info + Switch) ---
        action_layout = QHBoxLayout()
        action_layout.addWidget(self.bot_info_widget, stretch=True)
        action_layout.addWidget(self.switch_bot_button)

        # Adicionar tudo ao layout principal
        main_layout.addLayout(action_layout)
        main_layout.addWidget(self.connection_group)
        main_layout.addLayout(console_layout, stretch=True) # Log ocupa o espaço sobrando

        container = QWidget()
        container.setMinimumWidth(520)
        container.setLayout(main_layout)
        return container

    def set_bot_info(self, name: str, icon: QPixmap = None):
        """Sets the bot's name and icon and makes the widget visible."""
        dpr = self.devicePixelRatio()

        if not icon:
            icon = PixmapHelper.create_icon_with_background("fa6s.robot", "gray", 40, dpr)

        circular_icon = PixmapHelper.get_circular_pixmap(icon, 40, dpr)
        self.bot_info_widget.set_info(name, circular_icon)

    def reset_bot_info(self):
        """Resets the bot info widget to offline state."""
        self.set_bot_info(self.tr("Offline"))

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
        self.connection_group.setTitle(self.tr("Connection Settings"))
        self.cmd_line_edit.setPlaceholderText(self.tr("Type a command..."))
        self.token_label.setText(self.tr("Bot Token:"))
        self.switch_bot_button.setText(self.tr("Start Bot"))
        self.logs_text_edit.setPlaceholderText(self.tr("Waiting for bot to start..."))
