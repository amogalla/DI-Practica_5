import sys
from PySide6.QtWidgets import QApplication

from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

from main import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    
    i = 1
    window.nueva()
    window.modificar()
    while(i <= 3000):
        window.nueva()
        window.modificar()
        i = i+1
        print("Inserción", i, "realizada con éxito.")
    
    window.show()
    sys.exit(app.exec())
