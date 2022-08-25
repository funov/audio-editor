from controller.gui_controller import GetAudioInfoWorker
from utils import configure_button

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLineEdit,
    QMessageBox,
    QPushButton,
    QLabel,
    QDialog,
    QFormLayout, QFrame, QWidget, QGridLayout
)


class AudioEditorDialog(QDialog):
    def __init__(self, x, y, width, height, audio_list):
        self.audio_list = audio_list

        super(AudioEditorDialog, self).__init__()

        self.setGeometry(x, y, width, height)

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle('Редактирование аудиозаписей')
        self.setModal(True)

        self.glue_button = configure_button(
            self,
            self.open_glue_dialog,
            name="Склейка"
        )
        self.crop_button = configure_button(
            self,
            self.open_crop_dialog,
            name="Разрез"
        )
        self.paste_button = configure_button(
            self,
            self.open_paste_dialog,
            name="Вставка"
        )
        self.reverse_button = configure_button(
            self,
            self.open_reverse_dialog,
            name="Аудио задом наперед"
        )
        self.speed_button = configure_button(
            self,
            self.open_speed_dialog,
            name="Изменение скорости"
        )
        self.volume_button = configure_button(
            self,
            self.open_volume_dialog,
            name="Изменение громкости"
        )
        self.convert_button = configure_button(
            self,
            self.open_convert_dialog,
            name="Конвертация"
        )

        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        self.frame = QFrame()
        self.form = self.configure_form_layout()
        self.frame.setLayout(self.form)
        self.main_layout.addWidget(self.frame, 0, 0, 1, 1)

    def configure_form_layout(self):
        form = QFormLayout()
        form.setSpacing(20)

        form.addRow(self.convert_button)
        form.addRow(self.glue_button)
        form.addRow(self.crop_button)
        form.addRow(self.paste_button)
        form.addRow(self.reverse_button)
        form.addRow(self.speed_button)
        form.addRow(self.volume_button)

        return form

    def open_convert_dialog(self):
        pass

    def open_crop_dialog(self):
        self.frame.hide()

        self.settings_description = QLabel()
        description = ''

        for i in range(self.audio_list.count()):
            description += self.audio_list.item(i).text() + '\n'

        self.settings_description.setText(description)

        self.main_layout.addWidget(self.settings_description, 0, 0, 1, 1)
        self.main_layout.addWidget(self.glue_button, 0, 1, 1, 1)

    def open_glue_dialog(self):
        self.settings_description.hide()
        self.frame.show()

    def open_paste_dialog(self):
        pass

    def open_reverse_dialog(self):
        pass

    def open_speed_dialog(self):
        pass

    def open_volume_dialog(self):
        pass
