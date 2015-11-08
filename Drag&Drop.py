#!/usr/bin/env python
from PyQt4 import QtGui
from threading import Thread
from time import sleep


class Label(QtGui.QLabel):

    """Crear Drag&Drop"""

    def __init__(self, *args):
        super().__init__(*args)
        self.lastX = None
        self.lastY = None

    def mouseMoveEvent(self, e):
        if self.lastX is None and self.lastY is None:
            self.lastX = e.x()
            self.lastY = e.y()

        else:
            difX = e.x() - self.lastX
            difY = e.y() - self.lastY

            self.move(self.x() + difX, self.y() + difY)

    def mouseDoubleClickEvent(self, e):
        """
        Al doble click sobre la etiqueta cambia entre negrita y no negrita.
        """
        print(dir(e))
        isBold = self.font().bold()
        font = QtGui.QFont()
        font.setBold(not isBold)
        self.setFont(font)


class Ventana(QtGui.QWidget):

    def __init__(self, *args):
        super().__init__(*args)
        self.resize(200, 200)
        self.setWindowTitle('Hola')
        self.setup()
        self.show()
        self.left, self.right = False, False
        self.up, self.down = False, False
        Thread(target=self.moverLabel, daemon=True).start()

    def moverLabel(self):
        """
        Permite movimiento de una etiqueta por medio de las teclas (flechas).
        """
        while True:
            x = self.label.x()
            y = self.label.y()

            delta = 2

            # movimientos lineales
            if self.left and not(self.right or self.up or self.down):
                self.label.move(x - delta, y)
            elif self.right and not(self.left or self.up or self.down):
                self.label.move(x + delta, y)
            elif self.up and not(self.right or self.left or self.down):
                self.label.move(x, y - delta)
            elif self.down and not(self.right or self.up or self.left):
                self.label.move(x, y + delta)

            # movimientos diagonales
            elif self.right and self.up and not(self.down or self.left):
                self.label.move(x + delta, y - delta)
            elif self.right and self.down and not(self.up or self.left):
                self.label.move(x + delta, y + delta)
            elif self.left and self.up and not(self.down or self.right):
                self.label.move(x - delta, y - delta)
            elif self.left and self.down and not(self.up or self.right):
                self.label.move(x - delta, y + delta)

            sleep(0.01)

    def setup(self):
        self.label = Label(self)
        self.label.move(70, 80)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setText('Felipe')

        lab = Label(self)
        lab.setText('Garrido')

    def keyPressEvent(self, e):
        if (e.key() == 16777234):
            self.left = True
        elif (e.key() == 16777235):
            self.up = True
        elif (e.key() == 16777236):
            self.right = True
        elif(e.key() == 16777237):
            self.down = True

    def keyReleaseEvent(self, e):
        if (e.key() == 16777234):
            self.left = False
        elif (e.key() == 16777235):
            self.up = False
        elif (e.key() == 16777236):
            self.right = False
        elif(e.key() == 16777237):
            self.down = False

app = QtGui.QApplication([])
a = Ventana()
app.exec_()
