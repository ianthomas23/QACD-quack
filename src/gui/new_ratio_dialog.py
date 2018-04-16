from collections import Counter
from PyQt5 import QtCore, QtGui, QtWidgets

from .ui_new_ratio_dialog import Ui_NewRatioDialog


class NewRatioDialog(QtWidgets.QDialog, Ui_NewRatioDialog):
    def __init__(self, project, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.project = project

        # Elements making up new ratio.  Is None if using a preset as the
        # elements are determined from the name.
        self.ratio_elements = None

        self.okButton = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        self.nameEdit.textChanged.connect(self.update_buttons)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.currentChanged.connect(self.change_tab)

        # Preset tab.
        for preset in self.project.get_valid_preset_ratios():
            self.presetList.addItem(preset)

        self.presetList.itemSelectionChanged.connect(self.change_preset)

        # Custom tab.
        self.element_combos = (self.elementACombo, self.elementBCombo,
                               self.elementCCombo, self.elementDCombo)
        elements = self.project.elements
        nelements = len(elements)
        for index, combo in enumerate(self.element_combos):
            combo.addItems(elements)
            combo.setCurrentIndex(index % nelements)

        self.customTypeCombo.currentIndexChanged.connect(self.change_custom_type)
        for combo in self.element_combos:
            combo.currentIndexChanged.connect(self.change_element)

        # Common controls.
        names = self.project.get_correction_model_names()
        self.correctionModelCombo.addItem(None)
        self.correctionModelCombo.addItems(names)

        # Force correct initial display.
        self.change_custom_type()
        self.change_preset()
        self.update_buttons()

    def accept(self):
        try:
            # Validation.
            is_preset = self.ratio_elements is None

            name = self.nameEdit.text().strip()
            if len(name) < 1:
                raise RuntimeError('No ratio name specified')

            if name in self.project.ratios:
                raise RuntimeError("The ratio name '{}' has already been used".format(name))

            if not is_preset:
                counter = Counter(self.ratio_elements)
                if len(counter) != len(self.ratio_elements):
                    repeats = [elem for elem in sorted(counter) if counter[elem] > 1]
                    raise RuntimeError('The following elements are repeated in the formula: ' + \
                        ', '.join(repeats))

            correction_model = self.correctionModelCombo.currentText()
            if correction_model:
                model_elements = self.project.get_correction_model_elements(correction_model)
                if is_preset:
                    raise RuntimeError('Correction models are not yet implemented for presets')
                    if name not in model_elements:
                        raise RuntimeError("Correction model '{}' does not include preset '{}'".format( \
                            correction_model, name))
                else:
                    missing = [el for el in self.ratio_elements if el not in model_elements]
                    if len(missing) > 0:
                        raise RuntimeError("Correction model '{}' does not include the following elements: {}".format( \
                            correction_model, ', '.join(missing)))

            super().accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))

    def change_custom_type(self):
        nelements = self.customTypeCombo.currentIndex() + 2
        for index, combo in enumerate(self.element_combos):
            combo.setEnabled(index < nelements)
        self.change_element()  # Update formula label.

    def change_element(self):
        nelements = self.customTypeCombo.currentIndex() + 2
        self.ratio_elements = [combo.currentText() for combo in self.element_combos[:nelements]]
        self.formulaLabel.setText(self.project.get_formula_from_elements(self.ratio_elements))

    def change_preset(self):
        item = self.presetList.currentItem()
        self.ratio_elements = None
        if item is None:
            self.formulaLabel.setText(None)
            self.nameEdit.setText(None)
        else:
            preset_name = item.text()
            self.formulaLabel.setText(self.project.get_preset_formula(preset_name))
            self.nameEdit.setText(preset_name)

    def change_tab(self):
        tab_index = self.tabWidget.currentIndex()
        if tab_index == 0:
            self.change_preset()
        else:  # tab_index == 1
            self.change_custom_type()
            self.nameEdit.setText(None)

    def update_buttons(self):
        self.okButton.setEnabled(len(self.nameEdit.text()) > 0 and
                                 len(self.formulaLabel.text()) > 0)
