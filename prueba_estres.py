import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlRelationalTableModel

from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

from main import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    
    iteracion = 1
    while(iteracion <= 1000000):
        query = QSqlQuery("SELECT nombre, apellidos FROM alumnos",db=window.db)
        while query.next():
            nom=query.value(0)
            apellidos = query.value(1)
            print(nom, " ", apellidos)
        iteracion = iteracion + 1
    print("Consultas realizadas con éxito.")


    window.show()
    sys.exit(app.exec())