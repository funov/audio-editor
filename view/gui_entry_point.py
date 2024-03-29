import sys
import os
from tempfile import TemporaryDirectory

import tomli

from slider import Slider
from utils import configure_button
from audio_editor_dialog import AudioEditorDialog
from controller import gui_controller

from PyQt5.QtCore import Qt, QUrl, QTimer, QThreadPool
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QFileDialog,
    QApplication,
    QGridLayout,
    QWidget,
    QLabel,
    QStyle,
    QListWidget
)


IS_DEBUG = False


class Window(QMainWindow):
    def __init__(self, app, temp_dir):
        super(Window, self).__init__()
        self.app = app
        self.temp_dir = temp_dir

        self.setWindowTitle("Audio Editor")
        self.init_center_geometry()

        self.title_label = QLabel("Audio Editor")
        self.title_label.setFont(QFont("Calibri", 20))
        self.title_label.setAlignment(Qt.AlignCenter)

        self.rewind_left_button = configure_button(
            self,
            self.move_backward,
            self.style().standardIcon(QStyle.SP_MediaSeekBackward)
        )

        self.rewind_right_button = configure_button(
            self,
            self.move_forward,
            self.style().standardIcon(QStyle.SP_MediaSeekForward)
        )

        self.play_button = configure_button(
            self,
            self.play_audio,
            self.style().standardIcon(QStyle.SP_MediaPlay),
            QFont("Calibri", 14),
        )

        self.edit_button = configure_button(
            self,
            self.open_edit_dialog,
            self.style().standardIcon(QStyle.SP_FileDialogDetailedView)
        )

        self.audio_selection_button = configure_button(
            self,
            self.open_audio_file,
            self.style().standardIcon(QStyle.SP_DirOpenIcon)
        )

        self.audio_line = Slider(Qt.Horizontal, self)
        self.audio_line.sliderMoved.connect(self.set_player_position)

        self.user_timer = QLabel(gui_controller.to_str_time(0, 0, 0))
        self.user_timer.setFont(QFont("Calibri", 14))
        self.user_timer.setAlignment(Qt.AlignCenter)

        self.reset_audio_line()

        self.audio_list = QListWidget(self)

        self.grid_layout = self.configure_grid_layout()

        self.player = QMediaPlayer(self)
        self.player.stateChanged.connect(self.change_play_state)

        self.duration = None
        self.timer = None
        self.edit_dialog = None

        self.threadpool = QThreadPool()
        self.start_play_position = 0
        self.is_playing = False
        self.path = ''

    def reset_audio_line(self):
        self.audio_line.setRange(0, 0)
        self.audio_line.setValue(0)
        self.user_timer.setText(gui_controller.to_str_time(0, 0, 0))

    def open_audio_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)

        audio_paths = file_dialog.getOpenFileNames(
            self,
            "Open files", '/home', 'Audio Files (*.mp3 *.wav)'
        )

        current_paths = [
            self.audio_list.item(i).text() for i in range(
                self.audio_list.count()
            )
        ]

        for path in audio_paths[0]:
            if path not in current_paths:
                self.audio_list.addItem(path)

    def play_audio(self):
        if self.audio_list.currentItem() is None:
            QMessageBox.question(
                self,
                'Информация',
                'Выберите одну аудио запись',
                QMessageBox.Ok
            )
            return

        path = self.audio_list.currentItem().text()
        if path != self.path:
            self.finish_audio()

        if not self.is_playing:
            self.change_play_state()

            url = QUrl.fromLocalFile(path)
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.player.setPosition(self.start_play_position)

            self.get_audio_line_length(path)
            self.path = path

            return

        self.change_play_state()
        self.pause_player()

    def set_player_position(self, position):
        self.player.setPosition(int(position))

    def pause_player(self):
        self.player.pause()
        paused = self.player.position()
        self.start_play_position = paused

    def init_new_timer(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.time_step)
        self.timer.start()

    def time_step(self):
        if self.is_playing:
            self.audio_line.setValue(self.audio_line.value() + 1000)
            self.user_timer.setText(
                gui_controller.to_str_time(
                    self.audio_line.value() // 1000, 0, 0
                )
            )

    def get_audio_line_length(self, path):
        worker = gui_controller.GetAudioInfoWorker(path, IS_DEBUG)
        worker.signals.result.connect(self.start_playing)
        self.threadpool.start(worker)

    def start_playing(self, audio_info):
        seconds_duration = audio_info.int_duration
        seconds_duration *= 1000
        self.duration = int(seconds_duration - seconds_duration % 1000)
        self.audio_line.setRange(0, self.duration)

        self.init_new_timer()
        self.player.play()

    def change_play_state(self):
        if self.duration is not None \
                and self.duration == self.audio_line.value():
            self.finish_audio()

        if self.player.state() == QMediaPlayer.PlayingState:
            icon = QStyle.SP_MediaPause
            self.is_playing = True
        else:
            icon = QStyle.SP_MediaPlay
            self.is_playing = False

        self.play_button.setIcon(self.style().standardIcon(icon))

    def finish_audio(self):
        self.duration = None
        self.start_play_position = 0
        self.player.stop()

        if self.timer is not None:
            self.timer.stop()

        self.reset_audio_line()

    def move_forward(self):
        self.audio_line.setValue(self.audio_line.value() + 10000)
        self.player.setPosition(self.player.position() + 10000)
        self.user_timer.setText(
            gui_controller.to_str_time(self.audio_line.value() // 1000, 0, 0)
        )

    def move_backward(self):
        self.audio_line.setValue(self.audio_line.value() - 10000)
        self.player.setPosition(self.player.position() - 10000)
        self.user_timer.setText(
            gui_controller.to_str_time(self.audio_line.value() // 1000, 0, 0)
        )

    def open_edit_dialog(self):
        pos_x, pos_y, window_w, window_h = self.get_dialog_params()

        if self.edit_dialog is None:
            self.edit_dialog = AudioEditorDialog(
                pos_x,
                pos_y,
                window_w,
                window_h,
                self,
                IS_DEBUG
            )

        self.edit_dialog.show()

    def get_dialog_params(self):
        screen_rect = self.screen().geometry()

        window_height = self.size().height() // 2
        window_width = self.size().width() // 2

        screen_center_x = screen_rect.width() // 2 - window_width // 2
        screen_center_y = screen_rect.height() // 2 - window_height // 2

        return screen_center_x, screen_center_y, window_width, window_height

    def init_center_geometry(self):
        screen_rect = self.screen().geometry()

        window_height = int(screen_rect.height() / 1.8)
        window_width = int(screen_rect.width() / 1.5)

        screen_center_x = screen_rect.width() // 2 - window_width // 2
        screen_center_y = screen_rect.height() // 2 - window_height // 2

        self.setGeometry(
            screen_center_x,
            screen_center_y,
            window_width,
            window_height
        )

    def configure_grid_layout(self):
        grid_layout = QGridLayout(self)
        grid_layout.setContentsMargins(
            self.size().height() // 10,
            self.size().height() // 10,
            self.size().height() // 10,
            self.size().height() // 10
        )

        widget = QWidget()
        self.setCentralWidget(widget)

        grid_layout.addWidget(self.title_label, 0, 0, 1, 9)
        grid_layout.addWidget(self.rewind_left_button, 1, 0, 1, 3)
        grid_layout.addWidget(self.rewind_right_button, 1, 6, 1, 3)
        grid_layout.addWidget(self.play_button, 1, 3, 1, 3)
        grid_layout.addWidget(self.audio_selection_button, 2, 0, 1, 2)
        grid_layout.addWidget(self.audio_line, 2, 2, 1, 5)
        grid_layout.addWidget(self.user_timer, 2, 7, 1, 1)
        grid_layout.addWidget(self.edit_button, 2, 8, 1, 1)
        grid_layout.addWidget(self.audio_list, 3, 0, 1, 9)

        self.centralWidget().setLayout(grid_layout)

        return grid_layout


if __name__ == '__main__':
    application = QApplication(sys.argv)

    try:
        current_dir = os.path.realpath('gui_entry_point.py')
        split_sep = os.sep + "view" + os.sep
        settings_path = os.path.join(
            current_dir.split(split_sep)[0],
            'settings.toml'
        )

        with open(settings_path, "rb") as f:
            toml_config = tomli.load(f)

        _debug = toml_config['start']['debug']

        if _debug not in [True, False]:
            print('В поле debug конфига должно быть значение True или False')
        else:
            IS_DEBUG = _debug
    except KeyError:
        print('Видимо вы забыли написать конфиг файл')

    with TemporaryDirectory() as temp_dir_name:
        if IS_DEBUG:
            print('Создана временная директория -', temp_dir_name)

        window = Window(application, temp_dir_name)
        window.show()
        sys.exit(application.exec_())
