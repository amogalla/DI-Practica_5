from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QMainWindow
from pathlib import Path
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings

class ListadoPDF(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Informe")

        self.web = QWebEngineView()
        self.web.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        ruta = Path("Acta_cumplimentada.pdf")
        ruta.absolute().as_uri()
        self.web.load(QUrl(ruta.absolute().as_uri()))
        self.setCentralWidget(self.web)