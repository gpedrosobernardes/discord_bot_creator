import qtawesome
from PySide6.QtCore import QSize, QRect
from PySide6.QtGui import QPainterPath, QPainter, QPixmap, Qt, QColor, QIcon
from PySide6.QtWidgets import QStyle


class PixmapHelper:
    @staticmethod
    def get_circular_pixmap(pixmap: QPixmap, size: int, dpr: float = 1.0) -> QPixmap:
        """
        Cria um pixmap circular (recorte central) com suporte a HiDPI,
        utilizando QStyle para calcular o alinhamento.
        """
        if pixmap.isNull():
            return pixmap

        # 1. Configurar tamanho físico para alta densidade (Retina/4K)
        physical_size = int(size * dpr)

        output = QPixmap(physical_size, physical_size)
        output.fill(Qt.GlobalColor.transparent)
        output.setDevicePixelRatio(dpr)

        # 2. Configurar o Painter
        painter = QPainter(output)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

        # 3. Aplicar o recorte Circular (em coordenadas lógicas)
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)

        # 4. Calcular o Recorte Central usando QStyle.alignedRect
        # Descobrimos o menor lado para criar um quadrado de corte
        min_side = min(pixmap.width(), pixmap.height())
        crop_size = QSize(min_side, min_side)

        # O QStyle calcula automaticamente o retângulo centralizado dentro da imagem original
        source_rect = QStyle.alignedRect(
            Qt.LayoutDirection.LeftToRight,
            Qt.AlignmentFlag.AlignCenter,
            crop_size,  # Tamanho do quadrado que queremos cortar
            pixmap.rect()  # Retângulo total da imagem original
        )

        # 5. Desenhar
        # A source_rect (centro da original) é desenhada na target_rect (círculo final)
        target_rect = QRect(0, 0, size, size)
        painter.drawPixmap(target_rect, pixmap, source_rect)

        painter.end()
        return output

    @staticmethod
    def create_icon_with_background(
            icon_name: str,
            bg_color: str,
            size: int = 48,
            dpr: float = 1.0,
            icon_color: str = "white",
            scale_factor: float = 0.6
    ) -> QIcon:
        """
        Cria um ícone de alta qualidade (HiDPI) com fundo.

        Args:
            size (int): Tamanho LÓGICO desejado (ex: 48).
            dpr (float): Device Pixel Ratio da janela (ex: 1.0, 1.25, 2.0).
        """
        # 1. Calcular o tamanho FÍSICO (Pixels reais)
        # Se size=48 e dpr=2 (tela 4K/Retina), criamos uma imagem de 96x96 pixels.
        physical_w = int(size * dpr)
        physical_h = int(size * dpr)

        # 2. Criar o Pixmap com tamanho físico
        final_pixmap = QPixmap(physical_w, physical_h)
        final_pixmap.fill(Qt.GlobalColor.transparent)

        # IMPORTANTE: Avisar o pixmap sobre a sua densidade de pixels.
        # Isso faz com que o QPainter 'pense' em coordenadas lógicas (48x48)
        # enquanto desenha em alta resolução (96x96).
        final_pixmap.setDevicePixelRatio(dpr)

        # 3. Iniciar Pintura
        painter = QPainter(final_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # 4. Desenhar Fundo (Usando coordenadas lógicas 0..size)
        painter.setBrush(QColor(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, size, size)

        # 5. Gerar o Ícone Interno (QtAwesome)
        # Precisamos pedir ao qtawesome um ícone no tamanho FÍSICO para garantir qualidade,
        # caso contrário ele gera um pequeno e estica (ficando borrado).
        logical_icon_size = int(size * scale_factor)
        physical_icon_size = int(logical_icon_size * dpr)

        icon = qtawesome.icon(icon_name, color=icon_color)
        # Geramos o pixmap bruto em alta resolução
        icon_pixmap_high_res = icon.pixmap(physical_icon_size, physical_icon_size)

        # Setamos o DPR no ícone interno também para o alinhamento funcionar corretamente
        icon_pixmap_high_res.setDevicePixelRatio(dpr)

        # 6. Centralizar com QStyle.alignedRect (Usando coordenadas lógicas)
        centered_rect = QStyle.alignedRect(
            Qt.LayoutDirection.LeftToRight,
            Qt.AlignmentFlag.AlignCenter,
            QSize(logical_icon_size, logical_icon_size),  # Tamanho lógico
            QRect(0, 0, size, size)  # Área lógica
        )

        # 7. Desenhar
        painter.drawPixmap(centered_rect, icon_pixmap_high_res)
        painter.end()

        return final_pixmap
