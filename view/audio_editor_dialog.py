import os

from PyQt5.QtGui import QPixmap, QImage

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

        self.show_spectrogram_panel_button = configure_button(
            self,
            self.show_spectrogram_panel,
            name="Спектрограмма"
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
        self.dialog = None

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
        form.addRow(self.show_spectrogram_panel_button)
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

        self._show_standard_placement()

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

        self._show_standard_placement()

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

        self._show_standard_placement()

        self.hide()

    def _show_standard_placement(self):
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

    def show_spectrogram_panel(self):
        self.remove_layout_widgets()

        self.current_edit_widgets = [
            configure_button(
                self.main_window,
                self.prepare_to_spectrogram,
                name='Показать спектрограмму'
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

        if len(paths) == 0:
            self.empty_combo_box()
            return

        self.name = gui_controller.Utils.get_file_name() + '.mp3'

        worker = gui_controller.GlueAudioWorker(
            paths,
            f'{self.main_window.temp_dir}{os.sep}{self.name}'
        )

        worker.signals.finished.connect(self.add_result_to_audio_list)
        self.main_window.threadpool.start(worker)

    def add_new_glue_variant(self):
        for i in range(1, 5):
            if not self.current_edit_widgets[i].isVisible():
                self.current_edit_widgets[i].show()
                break

    def value_error(self):
        QMessageBox.question(
            self.main_window,
            'Некорректные данные',
            'Проверьте введенные значения',
            QMessageBox.Ok
        )

    def empty_combo_box(self):
        QMessageBox.question(
            self.main_window,
            'Некорректные данные',
            'Похоже вы ничего не выбрали',
            QMessageBox.Ok
        )

    def apply_paste(self):
        target_audio_path = self.current_edit_widgets[0].currentText()
        input_audio_path = self.current_edit_widgets[2].currentText()
        paste_time = self.current_edit_widgets[1].text()

        if target_audio_path == '' or input_audio_path == '':
            self.empty_combo_box()
            return

        self.name = gui_controller.Utils.get_file_name() + '.mp3'

        worker = gui_controller.PasteAudioWorker(
            target_audio_path,
            input_audio_path,
            f'{self.main_window.temp_dir}{os.sep}{self.name}',
            paste_time
        )

        self._start_worker(worker)

    def apply_reverse(self):
        self._crop_and_reverse_apply(gui_controller.ReverseAudioWorker)

    def apply_crop(self):
        self._crop_and_reverse_apply(gui_controller.CropAudioWorker)

    def apply_speed(self):
        speed = self.current_edit_widgets[3].text()

        self._apply_value(speed, gui_controller.ChangeSpeedWorker)

    def apply_volume(self):
        volume = self.current_edit_widgets[3].text()

        self._apply_value(volume, gui_controller.ChangeVolumeWorker)

    def _crop_and_reverse_apply(self, handler):
        input_audio_path, start_time, end_time = self._get_base_values()

        if input_audio_path == '':
            self.empty_combo_box()
            return

        worker = handler(
            input_audio_path,
            f'{self.main_window.temp_dir}{os.sep}{self.name}',
            start_time,
            end_time
        )

        self._start_worker(worker)

    def _apply_value(self, value, handler):
        input_audio_path, start_time, end_time = self._get_base_values()

        if input_audio_path == '':
            self.empty_combo_box()
            return

        worker = handler(
            input_audio_path,
            f'{self.main_window.temp_dir}{os.sep}{self.name}',
            value,
            start_time,
            end_time
        )

        self._start_worker(worker)

    def _start_worker(self, worker):
        worker.signals.finished.connect(self.add_result_to_audio_list)
        worker.signals.error.connect(self.value_error)
        self.main_window.threadpool.start(worker)

    def _get_base_values(self):
        input_audio_path = self.current_edit_widgets[0].currentText()
        start_time = self.current_edit_widgets[1].text()
        end_time = self.current_edit_widgets[2].text()

        if start_time == '00:00:00':
            start_time = None

        if end_time == '00:00:00':
            end_time = None

        self.name = gui_controller.Utils.get_file_name() + '.mp3'

        return input_audio_path, start_time, end_time

    def apply_convert_to_mp3(self):
        self._apply_convert('.mp3')

    def apply_convert_to_wav(self):
        self._apply_convert('.wav')

    def _apply_convert(self, file_extension):
        input_audio_path = self.current_edit_widgets[0].currentText()

        if input_audio_path == '':
            self.empty_combo_box()
            return

        self.name = gui_controller.Utils.get_file_name() + file_extension

        worker = gui_controller.ConvertAudioWorker(
            input_audio_path,
            f'{self.main_window.temp_dir}{os.sep}{self.name}'
        )

        worker.signals.finished.connect(self.add_result_to_audio_list)
        self.main_window.threadpool.start(worker)

    def apply_save(self):
        if self.main_window.audio_list.currentItem() is None:
            self.empty_combo_box()
            return

        current_item = self.main_window.audio_list.currentItem().text()

        if self.main_window.temp_dir.replace(os.sep, '/') in current_item:
            file_path = QFileDialog.getExistingDirectory(self)

            if file_path == '':
                return

            src = self.main_window.audio_list.currentItem().text()
            src_row = self.main_window.audio_list.currentRow()

            destination = gui_controller.Utils.replace_with_rename(
                src,
                file_path
            )

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

    def prepare_to_spectrogram(self):
        if self.main_window.audio_list.currentItem() is None:
            self.empty_combo_box()
            return

        current_item = self.main_window.audio_list.currentItem().text()

        self.name = gui_controller.Utils.get_file_name() + '.wav'

        worker = gui_controller.ConvertAudioWorker(
            current_item,
            f'{self.main_window.temp_dir}{os.sep}{self.name}'
        )

        worker.signals.finished.connect(self.apply_show_spectrogram)
        self.main_window.threadpool.start(worker)

    def apply_show_spectrogram(self):
        name = gui_controller.Utils.get_file_name() + '.png'

        worker = gui_controller.GetSpectrogramWorker(
            f'{self.main_window.temp_dir}{os.sep}{self.name}',
            f'{self.main_window.temp_dir}{os.sep}{name}'
        )

        self.name = name

        worker.signals.finished.connect(self.show_spectrogram)
        self.main_window.threadpool.start(worker)

    def show_spectrogram(self):
        self.dialog = QDialog()
        self.dialog.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.dialog.setWindowTitle('Спектрограмма')

        dialog_layout = QFormLayout()
        self.dialog.setLayout(dialog_layout)

        image = QImage(f'{self.main_window.temp_dir}{os.sep}{self.name}')
        pixmap = QPixmap.fromImage(image)
        label = QLabel()
        label.setPixmap(pixmap)

        save_spectrogram_button = configure_button(
            self,
            self.save_spectrogram,
            name="Сохранить спектрограмму"
        )

        dialog_layout.addRow(label)
        dialog_layout.addRow(save_spectrogram_button)

        self.dialog.exec()

    def save_spectrogram(self):
        file_path = QFileDialog.getExistingDirectory(self)

        if file_path == '':
            return

        picture_path = f'{self.main_window.temp_dir}{os.sep}{self.name}'

        gui_controller.Utils.replace_with_rename(
            picture_path,
            file_path
        )

        QMessageBox.question(
            self,
            'Информация',
            'Аудио сохранено',
            QMessageBox.Ok
        )

        self.dialog.close()

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
        audio_name = f'{self.main_window.temp_dir}{os.sep}{self.name}'
        audio_name = audio_name.replace(os.sep, '/')

        for widget in self.current_edit_widgets:
            if type(widget) is QComboBox:
                widget.addItem(audio_name)

        audio_list = [
            self.main_window.audio_list.item(i).text() for i in range(
                self.main_window.audio_list.count()
            )
        ]

        if audio_name not in audio_list:
            self.main_window.audio_list.addItem(audio_name)
