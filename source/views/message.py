from PySide6.QtCore import (
    QRegularExpression,
    QSize,
    Qt,
)
from PySide6.QtGui import (
    QIcon,
    QRegularExpressionValidator,
)
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QToolButton,
    QVBoxLayout,
    QWidget,
)
from qextrawidgets.gui.icons import QThemeResponsiveIcon
from qextrawidgets.widgets.miscellaneous.accordion import QAccordion
from qextrawidgets.widgets.views.grid_icon_view import QGridIconView

from source.core.constants import Actions, Punishment, WhereReact, WhereReply
from source.qt.widgets.condition_form import QConditionForm
from source.qt.widgets.reply_form import QReplyForm


class MessageView(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
        self.setWindowIcon(QIcon("assets/icons/window-icon.svg"))
        self.setMinimumSize(900, 700)
        self.resize(1000, 800)

        # --- WIDGETS ---

        # 1. Identificação
        self.name_text = QLabel()
        self.name_line_edit = QLineEdit()
        name_entry_validator = QRegularExpressionValidator(
            QRegularExpression(r"[A-zÀ-ú0-9 ]+")
        )
        self.name_line_edit.setMaxLength(40)
        self.name_line_edit.setValidator(name_entry_validator)

        # 2. Configurações (Comboboxes e Spins)
        self.settings_group = QGroupBox()

        self.action_label = QLabel()
        self.action_combobox = QComboBox()
        self.action_combobox.insertItems(0, map(str, Actions))

        self.punishment_label = QLabel()
        self.punishment_combobox = QComboBox()
        self.punishment_combobox.insertItems(0, map(str, Punishment))

        self.where_reply_label = QLabel()
        self.where_reply_combobox = QComboBox()
        self.where_reply_combobox.insertItems(0, map(str, WhereReply))

        self.where_react_label = QLabel()
        self.where_react_combobox = QComboBox()
        self.where_react_combobox.insertItems(0, map(str, WhereReact))

        self.delay_label = QLabel()
        self.delay_spin_box = QSpinBox()
        self.delay_spin_box.setRange(0, 3600)

        # 3. Conteúdo Principal (Acordeão e seus filhos)
        self.listbox_conditions = QConditionForm()

        # Widget de Reações (Layout interno)
        self.reactions_widget = QWidget()
        self.reactions_grid = QGridIconView(self, QSize(40, 40))
        self.add_reaction_button = QToolButton()
        self.add_reaction_button.setIcon(
            QThemeResponsiveIcon.fromAwesome("fa6s.face-smile")
        )
        self.add_reaction_button.setIconSize(QSize(20, 20))

        self.listbox_replies = QReplyForm()

        self.accordion = QAccordion()
        listbox_accordion_item = self.accordion.addSection("", self.listbox_conditions)
        self.accordion.addSection("", self.reactions_widget)
        self.accordion.addSection("", self.listbox_replies)
        self.accordion.setAnimationEnabled(False)
        listbox_accordion_item.setExpanded(True)

        # 4. Botões de Ação (Alterado)
        self.cancel_button = QPushButton()
        self.confirm_button = QPushButton()

        # Conexões padrão (opcional, mas recomendado para dialogs)
        self.cancel_button.clicked.connect(self.reject)
        self.confirm_button.clicked.connect(self.accept)

        self.setup_layout()

    def setup_layout(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Layout das reações
        reactions_layout = QHBoxLayout()
        reactions_layout.addWidget(self.reactions_grid)
        reactions_layout.addWidget(
            self.add_reaction_button, 0, Qt.AlignmentFlag.AlignTop
        )
        self.reactions_widget.setLayout(reactions_layout)

        # --- BLOCO 1: Identificação ---
        name_layout = QVBoxLayout()
        name_layout.setSpacing(5)
        self.name_text.setStyleSheet("font-weight: bold;")
        name_layout.addWidget(self.name_text)
        name_layout.addWidget(self.name_line_edit)
        main_layout.addLayout(name_layout)

        # --- BLOCO 2: Painel de Configurações (Grid) ---
        grid_settings = QGridLayout()
        grid_settings.setVerticalSpacing(10)
        grid_settings.setHorizontalSpacing(20)

        # Linha 0
        grid_settings.addWidget(self.action_label, 0, 0)
        grid_settings.addWidget(self.action_combobox, 0, 1)
        grid_settings.addWidget(self.punishment_label, 0, 2)
        grid_settings.addWidget(self.punishment_combobox, 0, 3)
        grid_settings.addWidget(self.delay_label, 0, 4)
        grid_settings.addWidget(self.delay_spin_box, 0, 5)

        # Linha 1
        grid_settings.addWidget(self.where_reply_label, 1, 0)
        grid_settings.addWidget(self.where_reply_combobox, 1, 1)
        grid_settings.addWidget(self.where_react_label, 1, 2)
        grid_settings.addWidget(self.where_react_combobox, 1, 3)

        grid_settings.setColumnStretch(1, 1)
        grid_settings.setColumnStretch(3, 1)
        grid_settings.setColumnStretch(5, 1)

        self.settings_group.setLayout(grid_settings)
        main_layout.addWidget(self.settings_group)

        # --- BLOCO 3: Conteúdo Expansível ---
        main_layout.addWidget(self.accordion, 1)

        # --- BLOCO 4: Rodapé (Botões à Direita) ---
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()  # Empurra tudo para a direita
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.confirm_button)

        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def translate_ui(self):
        self.setWindowTitle(self.tr("Message Rule"))
        self.name_text.setText(self.tr("Rule Name"))
        self.name_line_edit.setPlaceholderText(self.tr("Ex: Anti-Spam Filter"))
        self.name_line_edit.setToolTip(
            self.tr("The name can include letters (with accents), numbers, and spaces.")
        )

        self.settings_group.setTitle(self.tr("Rule Configuration"))

        for i, text in enumerate(
            [self.tr("Conditions (Triggers)"), self.tr("Reactions"), self.tr("Replies")]
        ):
            self.accordion.setSectionTitle(i, text)

        self.action_label.setText(self.tr("Action:"))
        for i, text in enumerate([self.tr("Pin"), self.tr("Delete"), self.tr("None")]):
            self.action_combobox.setItemText(i, text)

        self.punishment_label.setText(self.tr("Punishment:"))
        for i, text in enumerate([self.tr("Kick"), self.tr("Ban"), self.tr("None")]):
            self.punishment_combobox.setItemText(i, text)

        self.where_reply_label.setText(self.tr("Reply Scope:"))
        for i, text in enumerate(
            [
                self.tr("Group"),
                self.tr("Private"),
                self.tr("Same Channel"),
                self.tr("Both"),
                self.tr("None"),
            ]
        ):
            self.where_reply_combobox.setItemText(i, text)

        self.where_react_label.setText(self.tr("React Target:"))
        for i, text in enumerate([self.tr("Author"), self.tr("Bot"), self.tr("None")]):
            self.where_react_combobox.setItemText(i, text)

        self.delay_label.setText(self.tr("Execution Delay:"))

        # Tradução dos botões
        self.cancel_button.setText(self.tr("Cancel"))
        self.confirm_button.setText(self.tr("Confirm"))

        self.delay_spin_box.setSuffix(self.tr(" s", "Unit: Seconds"))

        self.listbox_conditions.translate_ui()
