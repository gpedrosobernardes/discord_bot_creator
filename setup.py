from cx_Freeze import setup, Executable

# Tenta importar a função que ajuda a localizar plugins do Qt
try:
    from cx_Freeze.hooks import get_qt_plugins_paths
except ImportError:
    get_qt_plugins_paths = None

# Lista inicial de arquivos
include_files = [
    ("assets/", "assets"),
    ("translations/build", "translations/build"),
    ("THIRD-PARTY.txt", "THIRD-PARTY.txt"),
]

# SEGURANÇA EXTRA: Incluir plugins vitais (Platforms, Styles, ImageFormats)
# Isso previne o erro "Qt platform plugin could not be initialized"
if get_qt_plugins_paths:
    # Inclui todos os plugins de plataforma (essencial para Windows/Linux/Mac)
    include_files += get_qt_plugins_paths("PySide6", "platforms")

    # Inclui plugins de imagens (necessário para seus ícones .ico e .svg)
    include_files += get_qt_plugins_paths("PySide6", "imageformats")

    # Inclui estilos (opcional, mas bom para garantir a aparência nativa)
    include_files += get_qt_plugins_paths("PySide6", "styles")

setup(
    name="Discord Bot Creator",
    version="2.0.0",
    description="Discord Bot Creator",
    options={
        "build_exe": {
            "include_files": include_files,
            "packages": ["audioop", "sqlite3"],
            "excludes": ["tkinter"] # Opcional: reduz o tamanho final removendo o Tkinter
        }
    },
    executables=[
        Executable(
            "main.py",
            target_name="Discord Bot Creator.exe",
            icon="assets/icons/logo.ico",
            base="gui",
        )
    ]
)