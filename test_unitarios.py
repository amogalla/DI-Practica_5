import sys
import unittest

from PySide6.QtWidgets import QApplication, QWidget

from main import MainWindow


class AnimatedToggleTestCase(unittest.TestCase):

    def test_filaInicial(self):
        window = MainWindow()
        self.assertEqual(window.fila, -1)
        
    def test_textoBotonGrafica(self):
        window = MainWindow()
        self.assertEqual(window.boton.text(), "Generar acta de evaluación")
        
    def test_textoBotonGenerarActa(self):
        window = MainWindow()
        self.assertEqual(window.botonGrafica.text(), "Gráfica de alumnos matriculados en cada itinerario")

    def test_seleccionInicial(self):
        window = MainWindow()
        result = window.tabla.selectionModel().currentIndex().row()
        self.assertEqual(result, -1)

    def test_labelInicial(self):
        window = MainWindow()
        result = window.label.text()
        self.assertEqual(result, "ID")

    def test_comboBoxInicial(self):
        window = MainWindow()
        result = window.comboBox_curso.currentText()
        self.assertEqual(result, "3º ESO")

    def test_numAlumnosInicial(self):
        window = MainWindow()
        result = window.num_alumnos()
        self.assertEqual(result, 15)

    #def test_numAlumnosTrasAñadir(self):
    #    window = MainWindow()
    #    resultInicial = window.num_alumnos()

    #    window.nueva()
        
    #    resultFinal = window.num_alumnos()
    #    self.assertEqual(resultInicial , resultFinal)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    unittest.main()