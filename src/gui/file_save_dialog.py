from PyQt5 import QtWidgets
import re


# Overriding implementation of QFileDialog because getSaveFileName does not
# automatically add the file extension (known bug in Qt).
class FileSaveDialog(QtWidgets.QFileDialog):
    def __init__(self, parent, caption, directory, filter_):
        super(FileSaveDialog, self).__init__(parent, caption, directory, filter_)
        self.filterSelected.connect(self.on_filter_selected)

    def on_filter_selected(self, filter_):
        match = re.search('\(\*\.(\w+)\)', filter_)
        if match:
            self.setDefaultSuffix(match.group(1))

    @staticmethod
    def getSaveFileName(parent, caption, directory, filter_,
                        selected_filter=None, options=None):
        dialog = FileSaveDialog(parent, caption, directory, filter_)
        dialog.setOptions(options)
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        if not selected_filter:
            selected_filter = filter_.split(';;')[0]
        dialog.selectNameFilter(selected_filter)
        dialog.on_filter_selected(selected_filter)

        if dialog.exec():
            return dialog.selectedFiles()[0], dialog.selectedNameFilter()
        else:
            return None, None
