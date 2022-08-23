from controller.gui_controller import GetAudioInfoWorker

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLineEdit,
    QMessageBox,
    QPushButton,
    QLabel,
    QDialog,
    QFormLayout
)


class AudioEditorDialog(QDialog):
    def __init__(self, x, y, width, height, audio_list):
        super(AudioEditorDialog, self).__init__()

        self.setGeometry(x, y, width, height)

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle('Редактирование аудиозаписей')
        self.setModal(True)

        self.settings_description = QLabel()

        description = ''

        for i in range(audio_list.count()):
            description += audio_list.item(i).text() + '\n'

        self.settings_description.setText(description)

        form = self.configure_form_layout()
        self.setLayout(form)

    def configure_form_layout(self):
        form = QFormLayout()
        form.setSpacing(20)

        form.addRow(self.settings_description)

        return form
