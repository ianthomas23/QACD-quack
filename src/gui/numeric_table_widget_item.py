# Custom QTableWidgetItem that sorts numerically not alphabetically.

from PyQt5 import QtCore, QtWidgets


class NumericTableWidgetItem (QtWidgets.QTableWidgetItem):
    def __init__ (self, number):
        super(NumericTableWidgetItem, self).__init__('{:g}'.format(number))
        self._number = number

    def __lt__ (self, other):
        if (isinstance(other, NumericTableWidgetItem)):
            return self._number < other._number
        else:
            return QtGui.DoubleTableWidgetItem.__lt__(self, other)
