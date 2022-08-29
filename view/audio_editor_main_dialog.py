import os
from tempfile import TemporaryDirectory
from time import time

from utils import configure_button
from controller import gui_controller

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QComboBox,
    QLineEdit,
    QStyle, QLabel, QPushButton, QFileDialog, QMessageBox
)


class AudioEditorDialog(QDialog):
    def __init__(self, x, y, width, height, main_window_layout, main_window):
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

        self.remove_editor_panel_button = configure_button(
            self,
            self.remove_editor_panel,
            name="Убрать панель редактора"
        )

        self.add_save_panel_button = configure_button(
            self,
            self.add_save_panel,
            name="Сохранение"
        )

        self.main_window_layout = main_window_layout
        self.main_window = main_window

        self.form = self.configure_form_layout()
        self.setLayout(self.form)

        self.current_widgets = []
        self.name = None

    def configure_form_layout(self):
        form = QFormLayout()
        form.setSpacing(20)

        form.addRow(self.glue_button)
        form.addRow(self.crop_button)
        form.addRow(self.paste_button)
        form.addRow(self.reverse_button)
        form.addRow(self.speed_button)
        form.addRow(self.volume_button)
        form.addRow(self.convert_button)
        form.addRow(self.remove_editor_panel_button)
        form.addRow(self.add_save_panel_button)

        return form

    def add_save_panel(self):
        self.remove_layout_widgets()

        self.current_widgets = [
            configure_button(self.main_window, self.save_audio, name='Сохранить'),
        ]

        self.main_window_layout.addWidget(self.current_widgets[0], 4, 0, 1, 9)

        self.hide()

    def save_audio(self):
        if self.main_window.temp_dir.replace(os.sep, '/') in self.main_window.audio_list.currentItem().text():
            file_path = QFileDialog.getExistingDirectory(self)

            if file_path == '':
                return

            src = self.main_window.audio_list.currentItem().text()
            src_row = self.main_window.audio_list.currentRow()
            dst = file_path + '/' + self.main_window.audio_list.currentItem().text().split('/')[-1]

            os.replace(src, dst)

            self.main_window.audio_list.takeItem(src_row)
            self.main_window.audio_list.addItem(dst)

            QMessageBox.question(
                self,
                'Информация',
                'Аудио сохранено',
                QMessageBox.Ok
            )
        else:
            QMessageBox.question(
                self,
                'Информация',
                'Это аудио и так сохранено',
                QMessageBox.Ok
            )

    def remove_layout_widgets(self):
        for widget in self.current_widgets:
            widget.hide()
            self.main_window_layout.removeWidget(widget)

    def remove_editor_panel(self):
        self.remove_layout_widgets()
        self.hide()

    def open_crop_dialog(self):
        self.remove_layout_widgets()

        self.current_widgets = [
            QComboBox(),
            QLineEdit(),
            QLineEdit(),
            configure_button(self.main_window, self.apply_crop, name='Подтвердить'),
        ]

        self.main_window_layout.addWidget(self.current_widgets[0], 4, 0, 1, 3)
        self.main_window_layout.addWidget(self.current_widgets[1], 4, 3, 1, 3)
        self.main_window_layout.addWidget(self.current_widgets[2], 4, 6, 1, 3)
        self.main_window_layout.addWidget(self.current_widgets[3], 5, 0, 1, 9)

        self.hide()

    def open_glue_dialog(self):
        self.remove_layout_widgets()

        self.current_widgets = [
            self.configure_combo_box(),
            self.configure_combo_box(),
            self.configure_combo_box(),
            self.configure_combo_box(),
            configure_button(self.main_window, self.add_new_glue_variant, icon=self.main_window.style().standardIcon(QStyle.SP_ToolBarHorizontalExtensionButton)),
            configure_button(self.main_window, self.apply_glue, name='Подтвердить'),
        ]

        self.current_widgets[1].hide()
        self.current_widgets[2].hide()
        self.current_widgets[3].hide()

        self.main_window_layout.addWidget(self.current_widgets[0], 4, 0, 1, 2)
        self.main_window_layout.addWidget(self.current_widgets[1], 4, 2, 1, 2)
        self.main_window_layout.addWidget(self.current_widgets[2], 4, 4, 1, 2)
        self.main_window_layout.addWidget(self.current_widgets[3], 4, 6, 1, 2)
        self.main_window_layout.addWidget(self.current_widgets[4], 4, 8, 1, 1)
        self.main_window_layout.addWidget(self.current_widgets[5], 5, 0, 1, 9)

        self.hide()

    def configure_combo_box(self):
        combo_box = QComboBox()

        combo_box.addItem('')
        for i in range(self.main_window.audio_list.count()):
            combo_box.addItem(self.main_window.audio_list.item(i).text())

        return combo_box

    def add_new_glue_variant(self):
        for i in range(1, 5):
            if not self.current_widgets[i].isVisible():
                self.current_widgets[i].show()
                break

    def apply_glue(self):
        paths = []

        for i in range(len(self.current_widgets) - 2):
            text = self.current_widgets[i].currentText()
            if text != '':
                paths.append(text)

        self.name = str(time()).replace('.', '')
        worker = gui_controller.GlueAudioWorker(paths, f'{self.main_window.temp_dir}{os.sep}{self.name}.mp3')
        worker.signals.finished.connect(self.add_result_to_audio_list)
        self.main_window.threadpool.start(worker)

    def add_result_to_audio_list(self):

        str = f'{self.main_window.temp_dir}{os.sep}{self.name}.mp3'.replace(os.sep, '/')

        for i in range(4):
            self.current_widgets[i].addItem(str)

        if str not in [self.main_window.audio_list.item(i).text() for i in range(self.main_window.audio_list.count())]:
            self.main_window.audio_list.addItem(str)

    def apply_crop(self):
        pass

    def open_paste_dialog(self):
        pass

    def open_reverse_dialog(self):
        pass

    def open_speed_dialog(self):
        pass

    def open_volume_dialog(self):
        pass

    def open_convert_dialog(self):
        pass
