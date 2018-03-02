from PyQt5 import QtCore, QtWidgets, QtGui
import string

from src.model.elements import element_properties
from src.model.qacd_project import QACDProject
from .matplotlib_widget import MatplotlibWidget, PlotType
from .ui_main_window import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)

        self.actionProjectNew.triggered.connect(self.on_project_new)
        self.actionProjectOpen.triggered.connect(self.on_project_open)
        self.actionProjectClose.triggered.connect(self.on_project_close)

        self.plotTypeComboBox.currentIndexChanged.connect(self.on_change_plot_type)
        self.rawElementList.itemSelectionChanged.connect( \
            lambda: self.on_change_list_item('raw'))

        # Set initial width of tabWidget.  Needs improvement.
        self.splitter.setSizes([50, 100])

        self._project = None

        # Current data to display.
        self._array = None
        self._array_stats = None
        self._type = None
        self._element = None

        self.update_title()

    def on_change_list_item(self, type_):
        if self._project is not None:
            self._type = type_
            self._element = self.rawElementList.currentItem().text()
            if self._type == 'raw':
                if self._element == 'Total':
                    self._array, self._array_stats = \
                        self._project.get_raw_total(want_stats=True)
                else:
                    self._array, self._array_stats = \
                        self._project.get_raw(self._element, want_stats=True)
            else:
                raise RuntimeError('Not implemented ' + type_)

        self.update_matplotlib_widget()

    def on_change_plot_type(self):
        self.update_matplotlib_widget()

    def on_project_close(self):
        if self._project is not None:
            self._project = None
            self._array = None
            self._array_stats = None
            self._type = None
            self._element = None

            self.rawElementList.clear()

            self.update_matplotlib_widget()
            self.update_title()

    def on_project_new(self):
        print('Project | New')

        # Need to wrap project functions (except read-only ones) in try..except
        # block.

        # Delete previous project first????
        self._project = QACDProject()  # Check can create project.
        #print(self.project)
        self._project.set_filename('example.quack')
        self._project.import_raw_csv_files('test_data')  # Need progress bar...
        print(self._project.elements)

        # Enable tab if not already present.

        type_ = 'raw'
        element_list = self.rawElementList
        want_total = True

        # Delete contents of list.
        element_list.clear()

        # Fill element list in tab.  And set tooltips.
        for i, element in enumerate(self._project.elements):
            element_list.addItem(element)
            name = element_properties[element][0]
            element_list.item(i).setToolTip(name)
        if want_total:
            element_list.addItem('Total')
            element_list.item(i+1).setToolTip(f'Sum of all {type_} element maps')

        # Bring tab to front.
        self.tabWidget.setCurrentIndex(0)

        self.update_title()

    def on_project_open(self):
        print('Project | Open')

    def update_matplotlib_widget(self):
        if self._type is None:
            self.matplotlibWidget.clear()
        else:
            plot_type = PlotType(self.plotTypeComboBox.currentIndex())
            if self._element == 'Total':
                name = 'total'
            else:
                name = element_properties[self._element][0]
            title = f'{string.capwords(self._type)} {name}'
            self.matplotlibWidget.update(plot_type, self._array,
                                         self._array_stats, title)

    def update_title(self):
        title = 'QACD quack'
        if self._project is not None:
            title += ' - ' + self._project.filename
        self.setWindowTitle(title)
