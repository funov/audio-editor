import os

from utils import configure_button
from controller import gui_controller

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QComboBox,
    QLineEdit,
    QStyle,
    QFileDialog,
    QMessageBox,
    QLabel
)


class AudioEditorDialog(QDialog):
    def __init__(self, x, y, width, height, main_window):
        super(AudioEditorDialog, self).__init__()

        self.setGeometry(x, y, width, height)

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle('Редактирование аудиозаписей')
        self.setModal(True)

        self.show_glue_panel_button = configure_button(
            self,
            self.show_glue_panel,
            name="Склейка"
        )
        self.show_crop_panel_button = configure_button(
            self,
            self.show_crop_panel,
            name="Разрез"
        )
        self.show_paste_panel_button = configure_button(
            self,
            self.show_paste_panel,
            name="Вставка"
        )
        self.show_reverse_panel_button = configure_button(
            self,
            self.show_reverse_panel,
            name="Аудио задом наперед"
        )
        self.show_speed_panel_button = configure_button(
            self,
            self.show_speed_panel,
            name="Изменение скорости"
        )
        self.show_volume_panel_button = configure_button(
            self,
            self.show_volume_panel,
            name="Изменение громкости"
        )
        self.show_convert_panel_button = configure_button(
            self,
            self.show_convert_panel,
            name="Конвертация"
        )

        self.show_save_panel_button = configure_button(
            self,
            self.show_save_panel,
            name="Сохранение"
        )

        self.remove_editor_panel_button = configure_button(
            self,
            self.remove_editor_panel,
            name="Убрать панель редактора"
        )

        self.main_window = main_window

        self.form = self.configure_form_layout()
        self.setLayout(self.form)

        self.current_edit_widgets = []
        self.name = None

    def configure_form_layout(self):
        form = QFormLayout()
        form.setSpacing(20)

        form.addRow(self.show_glue_panel_button)
        form.addRow(self.show_crop_panel_button)
        form.addRow(self.show_paste_panel_button)
        form.addRow(self.show_reverse_panel_button)
        form.addRow(self.show_speed_panel_button)
        form.addRow(self.show_volume_panel_button)
        form.addRow(self.show_convert_panel_button)
        form.addRow(self.show_save_panel_button)
        form.addRow(QLabel())
        form.addRow(self.remove_editor_panel_button)

        return form

    def show_glue_panel(self):
        self.remove_layout_widgets()

        self.current_edit_widgets = []

        for i in range(4):
            self.current_edit_widgets.append(self.configure_combo_box())

        self.current_edit_widgets.append(
            configure_button(
                self.main_window,
                self.add_new_glue_variant,
                icon=self.main_window.style().standardIcon(
                    QStyle.SP_ToolBarHorizontalExtensionButton
                )
            )
        )
        self.current_edit_widgets.append(
            configure_button(
                self.main_window,
                self.apply_glue,
                name='Склеить'
            )
        )

        for i in range(3):
            self.current_edit_widgets[i + 1].hide()

        for i in range(4):
            self.main_window.grid_layout.addWidget(
                self.current_edit_widgets[i],
                4, i * 2, 1, 2
            )

        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[4],
            4, 8, 1, 1
        )
        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[5],
            5, 0, 1, 9
        )

        self.hide()

    def show_crop_panel(self):
        self.remove_layout_widgets()

        self.current_edit_widgets = [
            self.configure_combo_box(),
            QLineEdit('00:00:00'),
            QLineEdit('00:00:00'),
            configure_button(
                self.main_window,
                self.apply_crop,
                name='Разрезать'
            ),
            QLabel('Оставьте 00:00:00, если не хотите ничего менять'),
            QLabel('Начало'),
            QLabel('Конец')
        ]

        for i in range(2):
            self.current_edit_widgets[i + 1].setInputMask("00:00:00")

        for i in range(3):
            self.main_window.grid_layout.addWidget(
                self.current_edit_widgets[i],
                5, i * 3, 1, 3
            )

        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[3],
            6, 0, 1, 9
        )

        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[4],
            4, 0, 1, 3
        )
        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[5],
            4, 3, 1, 3
        )
        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[6],
            4, 6, 1, 3
        )

        self.hide()

    def show_paste_panel(self):
        self.remove_layout_widgets()

        self.current_edit_widgets = [
            self.configure_combo_box(),
            QLineEdit('00:00:00'),
            self.configure_combo_box(),
            configure_button(
                self.main_window,
                self.apply_paste,
                name='Вставить'
            ),
            QLabel('Куда вставлять'),
            QLabel('Время'),
            QLabel('Что вставлять')
        ]

        self.current_edit_widgets[1].setInputMask("00:00:00")

        for i in range(3):
            self.main_window.grid_layout.addWidget(
                self.current_edit_widgets[i],
                5, i * 3, 1, 3
            )

        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[3],
            6, 0, 1, 9
        )

        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[4],
            4, 0, 1, 3
        )
        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[5],
            4, 3, 1, 3
        )
        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[6],
            4, 6, 1, 3
        )

        self.hide()

    def show_reverse_panel(self):
        self.remove_layout_widgets()

        self.current_edit_widgets = [
            self.configure_combo_box(),
            QLineEdit('00:00:00'),
            QLineEdit('00:00:00'),
            configure_button(
                self.main_window,
                self.apply_reverse,
                name='Развернуть'
            ),
            QLabel('Оставьте 00:00:00, если хотите перевернуть полностью'),
            QLabel('Начало'),
            QLabel('Конец')
        ]

        self.current_edit_widgets[1].setInputMask("00:00:00")

        for i in range(3):
            self.main_window.grid_layout.addWidget(
                self.current_edit_widgets[i],
                5, i * 3, 1, 3
            )

        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[3],
            6, 0, 1, 9
        )

        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[4],
            4, 0, 1, 3
        )
        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[5],
            4, 3, 1, 3
        )
        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[6],
            4, 6, 1, 3
        )

        self.hide()

    def show_speed_panel(self):
        self.remove_layout_widgets()

        self.current_edit_widgets = [
            self.configure_combo_box(),
            QLineEdit("00:00:00"),
            QLineEdit("00:00:00"),
            QLineEdit(),
            configure_button(
                self.main_window,
                self.apply_speed,
                name='Изменить скорость'
            ),
            QLabel('Оставьте 00:00:00, если хотите изменить полностью'),
            QLabel('Начало'),
            QLabel('Конец'),
            QLabel('Значение от 0.5 до 10 раз'),
        ]

        for i in range(2):
            self.current_edit_widgets[i + 1].setInputMask("00:00:00")

        self.show_change_value_panel()

        self.hide()

    def show_volume_panel(self):
        self.remove_layout_widgets()

        self.current_edit_widgets = [
            self.configure_combo_box(),
            QLineEdit("00:00:00"),
            QLineEdit("00:00:00"),
            QLineEdit(),
            configure_button(
                self.main_window,
                self.apply_volume,
                name='Изменить громкость'
            ),
            QLabel('Оставьте 00:00:00, если хотите изменить полностью'),
            QLabel('Начало'),
            QLabel('Конец'),
            QLabel('Значение от -30дБ до 30дБ'),
        ]

        for i in range(2):
            self.current_edit_widgets[i + 1].setInputMask("00:00:00")

        self.show_change_value_panel()

        self.hide()

    def show_change_value_panel(self):
        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[0],
            5, 0, 1, 3
        )
        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[5],
            4, 0, 1, 3
        )

        for i in range(3):
            self.main_window.grid_layout.addWidget(
                self.current_edit_widgets[i + 1],
                5, (i + 1) * 2 + 1, 1, 2
            )
            self.main_window.grid_layout.addWidget(
                self.current_edit_widgets[i + 6],
                4, (i + 1) * 2 + 1, 1, 2
            )

        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[4],
            6, 0, 1, 9
        )

    def show_convert_panel(self):
        self.remove_layout_widgets()

        self.current_edit_widgets = [
            self.configure_combo_box(),
            configure_button(
                self.main_window,
                self.apply_convert_to_wav,
                name='Конвертировать в .wav'
            ),
            configure_button(
                self.main_window,
                self.apply_convert_to_mp3,
                name='Конвертировать в .mp3'
            ),
        ]

        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[0],
            4, 0, 1, 9
        )
        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[1],
            5, 0, 1, 9
        )
        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[2],
            6, 0, 1, 9
        )

        self.hide()

    def show_save_panel(self):
        self.remove_layout_widgets()

        self.current_edit_widgets = [
            configure_button(
                self.main_window,
                self.apply_save,
                name='Сохранить'
            ),
        ]

        self.main_window.grid_layout.addWidget(
            self.current_edit_widgets[0],
            4, 0, 1, 9
        )

        self.hide()

    def remove_editor_panel(self):
        self.remove_layout_widgets()
        self.hide()

    def apply_glue(self):
        paths = []

        for i in range(len(self.current_edit_widgets) - 2):
            text = self.current_edit_widgets[i].currentText()
            if text != '':
                paths.append(text)

        self.name = gui_controller.Utils.get_file_name()

        worker = gui_controller.GlueAudioWorker(
            paths,
            f'{self.main_window.temp_dir}{os.sep}{self.name}.mp3'
        )

        worker.signals.finished.connect(self.add_result_to_audio_list)
        self.main_window.threadpool.start(worker)

    def add_new_glue_variant(self):
        for i in range(1, 5):
            if not self.current_edit_widgets[i].isVisible():
                self.current_edit_widgets[i].show()
                break

    def apply_crop(self):
        input_audio_path = self.current_edit_widgets[0].currentText()
        start_time = self.current_edit_widgets[1].text()
        end_time = self.current_edit_widgets[2].text()

        if start_time == '00:00:00':
            start_time = None

        if end_time == '00:00:00':
            end_time = None

        self.name = gui_controller.Utils.get_file_name()

        worker = gui_controller.CropAudioWorker(
            input_audio_path,
            f'{self.main_window.temp_dir}{os.sep}{self.name}.mp3',
            start_time,
            end_time
        )

        worker.signals.finished.connect(self.add_result_to_audio_list)
        worker.signals.error.connect(self.value_error)
        self.main_window.threadpool.start(worker)

    def value_error(self):
        QMessageBox.question(
            self.main_window,
            'Некорректные данные',
            'Проверьте введенные значения',
            QMessageBox.Ok
        )

    def apply_paste(self):
        target_audio_path = self.current_edit_widgets[0].currentText()
        input_audio_path = self.current_edit_widgets[2].currentText()
        paste_time = self.current_edit_widgets[1].text()

        self.name = gui_controller.Utils.get_file_name()

        worker = gui_controller.PasteAudioWorker(
            target_audio_path,
            input_audio_path,
            f'{self.main_window.temp_dir}{os.sep}{self.name}.mp3',
            paste_time
        )

        worker.signals.finished.connect(self.add_result_to_audio_list)
        worker.signals.error.connect(self.value_error)
        self.main_window.threadpool.start(worker)

    def apply_reverse(self):
        input_audio_path = self.current_edit_widgets[0].currentText()
        start_time = self.current_edit_widgets[1].text()
        end_time = self.current_edit_widgets[2].text()

        if start_time == '00:00:00':
            start_time = None

        if end_time == '00:00:00':
            end_time = None

        self.name = gui_controller.Utils.get_file_name()

        worker = gui_controller.ReverseAudioWorker(
            input_audio_path,
            f'{self.main_window.temp_dir}{os.sep}{self.name}.mp3',
            start_time,
            end_time
        )

        worker.signals.finished.connect(self.add_result_to_audio_list)
        worker.signals.error.connect(self.value_error)
        self.main_window.threadpool.start(worker)

    def apply_speed(self):
        input_audio_path = self.current_edit_widgets[0].currentText()
        start_time = self.current_edit_widgets[1].text()
        end_time = self.current_edit_widgets[2].text()
        speed = self.current_edit_widgets[3].text()

        if start_time == '00:00:00':
            start_time = None

        if end_time == '00:00:00':
            end_time = None

        self.name = gui_controller.Utils.get_file_name()

        worker = gui_controller.ChangeSpeedWorker(
            input_audio_path,
            f'{self.main_window.temp_dir}{os.sep}{self.name}.mp3',
            speed,
            start_time,
            end_time
        )

        worker.signals.finished.connect(self.add_result_to_audio_list)
        worker.signals.error.connect(self.value_error)
        self.main_window.threadpool.start(worker)

    def apply_volume(self):
        input_audio_path = self.current_edit_widgets[0].currentText()
        start_time = self.current_edit_widgets[1].text()
        end_time = self.current_edit_widgets[2].text()
        volume = self.current_edit_widgets[3].text()

        if start_time == '00:00:00':
            start_time = None

        if end_time == '00:00:00':
            end_time = None

        self.name = gui_controller.Utils.get_file_name()

        worker = gui_controller.ChangeVolumeWorker(
            input_audio_path,
            f'{self.main_window.temp_dir}{os.sep}{self.name}.mp3',
            volume,
            start_time,
            end_time
        )

        worker.signals.finished.connect(self.add_result_to_audio_list)
        worker.signals.error.connect(self.value_error)
        self.main_window.threadpool.start(worker)

    def apply_convert_to_mp3(self):
        input_audio_path = self.current_edit_widgets[0].currentText()

        self.name = gui_controller.Utils.get_file_name()

        worker = gui_controller.ConvertAudioWorker(
            input_audio_path,
            f'{self.main_window.temp_dir}{os.sep}{self.name}.mp3'
        )

        worker.signals.finished.connect(self.add_result_to_audio_list)
        self.main_window.threadpool.start(worker)

    def apply_convert_to_wav(self):
        input_audio_path = self.current_edit_widgets[0].currentText()

        self.name = gui_controller.Utils.get_file_name()

        worker = gui_controller.ConvertAudioWorker(
            input_audio_path,
            f'{self.main_window.temp_dir}{os.sep}{self.name}.wav'
        )

        worker.signals.finished.connect(self.add_result_to_audio_list)
        self.main_window.threadpool.start(worker)

    def apply_save(self):
        if self.main_window.temp_dir.replace(os.sep, '/') in self.main_window.audio_list.currentItem().text():
            file_path = QFileDialog.getExistingDirectory(self)

            if file_path == '':
                return

            src = self.main_window.audio_list.currentItem().text()
            src_row = self.main_window.audio_list.currentRow()

            destination = gui_controller.Utils.replace_with_rename(src, file_path)

            self.main_window.audio_list.takeItem(src_row)
            self.main_window.audio_list.addItem(destination)

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
        for widget in self.current_edit_widgets:
            widget.hide()
            self.main_window.grid_layout.removeWidget(widget)

    def configure_combo_box(self):
        combo_box = QComboBox()

        combo_box.addItem('')
        for i in range(self.main_window.audio_list.count()):
            combo_box.addItem(self.main_window.audio_list.item(i).text())

        return combo_box

    def add_result_to_audio_list(self):
        audio_name = f'{self.main_window.temp_dir}{os.sep}{self.name}.mp3'.replace(os.sep, '/')

        for widget in self.current_edit_widgets:
            if str(type(widget)) == "<class 'PyQt5.QtWidgets.QComboBox'>":
                widget.addItem(audio_name)

        audio_list = [self.main_window.audio_list.item(i).text() for i in range(self.main_window.audio_list.count())]

        if audio_name not in audio_list:
            self.main_window.audio_list.addItem(audio_name)
