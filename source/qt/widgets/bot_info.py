from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout


class BotInfoWidget(QWidget):
    """
    Widget dedicado a exibir o ícone e o nome do Bot.
    Atributos internos encapsulados com underscore (_).
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._init_layout()

    def _init_ui(self):
        """Inicializa os componentes visuais."""
        # Configuração do Ícone (Privado)
        self._bot_icon_label = QLabel()
        self._bot_icon_label.setFixedSize(42, 42)
        self._bot_icon_label.setScaledContents(True)

        # Configuração do Nome (Privado)
        self._bot_name_label = QLabel()
        self._bot_name_label.setText("Bot Name")

        # Configuração da Fonte
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)

        self._bot_name_label.setFont(font)

    def _init_layout(self):
        """Organiza o layout horizontal."""
        layout = QHBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 5, 0, 5)

        layout.addWidget(self._bot_icon_label)
        layout.addWidget(self._bot_name_label)

    def set_info(self, name: str, icon_pixmap: QPixmap = None):
        """
        Método público para atualizar as informações.
        Quem usa a classe não acessa os labels diretamente.
        """
        self._bot_name_label.setText(name)

        if icon_pixmap and not icon_pixmap.isNull():
            self._bot_icon_label.setPixmap(icon_pixmap)
        else:
            self._bot_icon_label.clear()

    def clear_info(self):
        """Limpa as informações internas."""
        self._bot_name_label.clear()
        self._bot_icon_label.clear()