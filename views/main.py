import qtawesome
from PySide6.QtCore import QCoreApplication, QSize, QTranslator, QObject
from PySide6.QtGui import QIcon, Qt, QAction
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
from qextrawidgets.icons import QThemeResponsiveIcon

from widgets.groups_list import QGroupsList
from widgets.log_textedit import QLogTextEdit


class MainView(QObject):
    def __init__(self):
        super().__init__()
        # window
        self.window = QMainWindow()
        self.window.setMinimumSize(800, 600)
        self.window.resize(1000, 800)
        self.window.setWindowIcon(QIcon("source/icons/window-icon.svg"))
        self.window.setWindowTitle("Discord Bot Creator")

        # actions

        # file actions
        self.new_file_action = QAction()

        self.load_file_action = QAction()

        self.save_file_action = QAction()

        self.save_as_file_action = QAction()

        self.config_action = QAction()

        self.exit_action = QAction()

        # message actions
        self.new_message_action = QAction(
            icon=QThemeResponsiveIcon.fromAwesome("fa6s.plus"),
            shortcut="Ctrl+N",
        )

        self.edit_message_action = QAction(
            icon=QThemeResponsiveIcon.fromAwesome("fa6s.pencil"),
            shortcut="Ctrl+E",
        )

        self.remove_message_action = QAction(
            icon=QThemeResponsiveIcon.fromAwesome("fa6s.minus"),
            shortcut="Delete",
        )

        self.remove_all_message_action = QAction(
            icon=QThemeResponsiveIcon.fromAwesome("fa6s.trash"),
            shortcut="Ctrl+Delete",
        )

        # group actions
        self.config_group_action = QAction(
            icon=QThemeResponsiveIcon.fromAwesome("fa6s.gear"),
        )

        self.quit_group_action = QAction(
            icon=QThemeResponsiveIcon.fromAwesome("fa6s.arrow-right-from-bracket"),
        )

        # help actions
        self.credits_action = QAction()
        self.logs_action = QAction()
        self.project_action = QAction()
        self.report_bug_action = QAction()
        self.discord_applications_action = QAction()

        # menu
        self.menu_bar = QMenuBar()

        self.file_menu = QMenu(self.menu_bar)

        self.edit_menu = QMenu(self.menu_bar)

        self.help_menu = QMenu(self.menu_bar)

        # left widgets

        # group tab
        self.search_groups = QSearchLineEdit()

        self.groups_list_widget = QGroupsList()

        self.config_group_button = QToolButton()
        self.config_group_button.setDefaultAction(self.config_group_action)

        self.quit_group_button = QToolButton()
        self.quit_group_button.setDefaultAction(self.quit_group_action)

        # message tab
        self.search_messages_line_edit = QSearchLineEdit()

        self.messages_list_view = QListView()

        self.new_message_tool_button = QToolButton()
        self.new_message_tool_button.setDefaultAction(self.new_message_action)

        self.edit_message_tool_button = QToolButton()
        self.edit_message_tool_button.setDefaultAction(self.edit_message_action)

        self.remove_message_tool_button = QToolButton()
        self.remove_message_tool_button.setDefaultAction(self.remove_message_action)

        self.remove_all_message_tool_button = QToolButton()
        self.remove_all_message_tool_button.setDefaultAction(
            self.remove_all_message_action
        )

        # right widgets
        self.logs_text_edit = QLogTextEdit()
        self.cmd_line_edit = QLineEdit()

        self.token_label = QLabel()

        self.token_line_edit = QPasswordLineEdit()
        self.token_line_edit.setMaxLength(100)

        switch_icon = QIcon()

        pixmap_play = qtawesome.icon("fa6s.play").pixmap(QSize(48, 48))
        switch_icon.addPixmap(pixmap_play, QIcon.Mode.Normal, QIcon.State.Off)

        pixmap_stop = qtawesome.icon("fa6s.stop").pixmap(QSize(48, 48))
        switch_icon.addPixmap(pixmap_stop, QIcon.Mode.Normal, QIcon.State.On)

        self.switch_bot_button = QColorButton("#599E5E", "", "white", "#C94F4F")
        self.switch_bot_button.setCheckable(True)
        self.switch_bot_button.setIcon(switch_icon)

        self.left_tab_widget = QTabWidget()

        self.setup_menus()
        self.setup_layout()
        self.translate_ui()
        self.window.show()

    def setup_menus(self):
        self.window.setMenuBar(self.menu_bar)

        self.menu_bar.addMenu(self.file_menu)
        self.menu_bar.addMenu(self.edit_menu)
        self.menu_bar.addMenu(self.help_menu)

        self.file_menu.addActions(
            (
                self.new_file_action,
                self.load_file_action,
                self.save_file_action,
                self.save_as_file_action,
                self.config_action,
                self.exit_action,
            )
        )

        self.edit_menu.addActions(
            (
                self.new_message_action,
                self.remove_all_message_action,
            )
        )

        self.help_menu.addActions(
            (
                self.discord_applications_action,
                self.logs_action,
                self.credits_action,
                self.project_action,
                self.report_bug_action,
            )
        )

    def setup_layout(self):
        # left frame
        group_tool_buttons_horizontal_layout = QHBoxLayout()
        group_tool_buttons_horizontal_layout.addStretch()
        for widget in (
            self.config_group_button,
            self.quit_group_button,
        ):
            group_tool_buttons_horizontal_layout.addWidget(widget)

        group_vertical_layout = QVBoxLayout()
        for widget in (
            self.search_groups,
            self.groups_list_widget,
        ):
            group_vertical_layout.addWidget(widget)
        group_vertical_layout.addLayout(group_tool_buttons_horizontal_layout)

        groups_widget = QWidget()
        groups_widget.setContentsMargins(5, 5, 5, 5)
        groups_widget.setLayout(group_vertical_layout)

        # message tab
        message_tool_buttons_horizontal_layout = QHBoxLayout()
        message_tool_buttons_horizontal_layout.addStretch()

        for widget in (
            self.new_message_tool_button,
            self.edit_message_tool_button,
            self.remove_message_tool_button,
            self.remove_all_message_tool_button,
        ):
            message_tool_buttons_horizontal_layout.addWidget(widget)

        message_vertical_layout = QVBoxLayout()
        for widget in (
            self.search_messages_line_edit,
            self.messages_list_view,
        ):
            message_vertical_layout.addWidget(widget)
        message_vertical_layout.addLayout(message_tool_buttons_horizontal_layout)

        messages_widget = QWidget()
        messages_widget.setContentsMargins(5, 5, 5, 5)
        messages_widget.setLayout(message_vertical_layout)

        self.left_tab_widget.setMinimumWidth(280)
        self.left_tab_widget.addTab(messages_widget, "")
        self.left_tab_widget.addTab(groups_widget, "")

        # right frame
        right_vertical_box_layout = QVBoxLayout()
        right_vertical_box_layout.setContentsMargins(10, 10, 10, 10)
        for widget in (
            self.logs_text_edit,
            self.cmd_line_edit,
            self.token_label,
            self.token_line_edit,
            self.switch_bot_button,
        ):
            right_vertical_box_layout.addWidget(widget)

        right_widget = QWidget()
        right_widget.setMinimumWidth(520)
        right_widget.setLayout(right_vertical_box_layout)

        # splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.left_tab_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(1, 1)
        self.window.setCentralWidget(splitter)

    def translate_ui(self):
        self.new_file_action.setText(self.tr("New file"))
        self.load_file_action.setText(self.tr("Load"))
        self.save_file_action.setText(self.tr("Save"))
        self.save_as_file_action.setText(self.tr("Save as"))
        self.config_action.setText(self.tr("Configuration"))
        self.exit_action.setText(self.tr("Exit"))
        self.new_message_action.setText(self.tr("New message"))
        self.edit_message_action.setText(self.tr("Edit message"))
        self.remove_message_action.setText(self.tr("Remove message"))
        self.remove_all_message_action.setText(self.tr("Remove all messages"))
        self.config_group_action.setText(self.tr("Config group"))
        self.quit_group_action.setText(self.tr("Quit group"))
        self.credits_action.setText(self.tr("Credits"))
        self.logs_action.setText(self.tr("Logs"))
        self.project_action.setText(self.tr("Project"))
        self.report_bug_action.setText(self.tr("Report bug"))
        self.discord_applications_action.setText(self.tr("Discord applications"))
        self.file_menu.setTitle(self.tr("File"))
        self.edit_menu.setTitle(self.tr("Edit"))
        self.help_menu.setTitle(self.tr("Help"))
        self.left_tab_widget.setTabText(0, self.tr("Messages"))
        self.left_tab_widget.setTabText(1, self.tr("Groups"))
        self.cmd_line_edit.setPlaceholderText(self.tr("Type a command"))
        self.token_label.setText(self.tr("Token"))
        self.switch_bot_button.setText(self.tr("Turn on/off bot"))
        self.logs_text_edit.setPlaceholderText(self.tr("No logs at moment"))
