import logging

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QPlainTextEdit


class LogHighlighter(QSyntaxHighlighter):
    """
    Camada responsável por colorir o texto dinamicamente.
    Ele não olha para o texto, mas sim para o 'Estado do Bloco' (UserState).
    """

    def __init__(self, document):
        super().__init__(document)

        self._formats = {
            Qt.ColorScheme.Dark: {
                logging.INFO: self._create_text_char_format("#ffffff"),
                logging.DEBUG: self._create_text_char_format("#929EA8"),
                logging.ERROR: self._create_text_char_format("#FC6E77"),
                logging.WARNING: self._create_text_char_format("#FFC107"),
            },
            Qt.ColorScheme.Light: {
                logging.INFO: self._create_text_char_format("#000000"),
                logging.DEBUG: self._create_text_char_format("#5A6269"),
                logging.ERROR: self._create_text_char_format("#B62A37"),
                logging.WARNING: self._create_text_char_format("#8B6702"),
            },
        }

    @staticmethod
    def _create_text_char_format(color: str, bold: bool = False) -> QTextCharFormat:
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        if bold:
            fmt.setFontWeight(QFont.Weight.Bold)
        return fmt

    def highlightBlock(self, text: str):
        """
        Chamado automaticamente pelo Qt para cada linha visível.
        Aplica a formatação baseada no 'currentBlockState'.
        """
        # O UserState contém o logging.LEVEL que definimos ao inserir o texto
        level = self.currentBlockState()

        # Pega o esquema atual do sistema (ou o forçado pela demo)
        scheme = QApplication.styleHints().colorScheme()

        # Fallback se o esquema for desconhecido
        if scheme not in self._formats:
            scheme = Qt.ColorScheme.Light

        current_theme_formats = self._formats[scheme]

        # Se houver uma cor definida para este nível neste tema, aplica
        if level in current_theme_formats:
            self.setFormat(
                0,  # Início (caractere 0)
                len(text),  # Tamanho (linha toda)
                current_theme_formats[level],
            )


class QLogTextEdit(QPlainTextEdit):
    def __init__(self, parent=None, max_line_count: int = 2000):
        super().__init__(parent)
        self.setReadOnly(True)
        self.document().setMaximumBlockCount(max_line_count)

        # 1. Instala o Highlighter no documento deste widget
        self.highlighter = LogHighlighter(self.document())

        # 2. Conecta mudança de tema
        QApplication.styleHints().colorSchemeChanged.connect(self._on_theme_changed)

    @Slot(str, int)
    def add_log(self, message: str, level: int = logging.INFO):
        """
        Adiciona texto puro e marca o estado do bloco.
        """
        self.appendPlainText(message)

        # Pega o bloco que acabamos de criar
        block = self.document().lastBlock()

        # 1. Define o estado (Isso não dispara o repaint visual sozinho)
        block.setUserState(level)

        # 2. FORÇA o highlighter a repintar APENAS este bloco agora que ele tem estado
        self.highlighter.rehighlightBlock(block)

    @Slot()
    def _on_theme_changed(self):
        # Apenas avisa o highlighter para atualizar as cores internas e redesenhar
        self.highlighter.rehighlight()
