import sys
from math import ceil
from slider import Slider

from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QFileDialog,
    QApplication,
    QPushButton,
    QGridLayout,
    QWidget,
    QLabel,
    QStyle,
    QListWidget
)


class Window(QMainWindow):
    def __init__(self, app):
        super(Window, self).__init__()
        self.app = app

        self.setWindowTitle("Audio Editor")
        self.init_center_geometry()

        self.title_label = QLabel("Audio Editor")
        self.title_label.setFont(QFont("Calibri", 20))
        self.title_label.setAlignment(Qt.AlignCenter)

        self.rewind_left_button = self.configure_button(
            self.style().standardIcon(QStyle.SP_MediaSeekBackward),
            self.move_backward
        )

        self.rewind_right_button = self.configure_button(
            self.style().standardIcon(QStyle.SP_MediaSeekForward),
            self.move_forward
        )

        self.play_button = self.configure_button(
            self.style().standardIcon(QStyle.SP_MediaPlay),
            self.play_audio,
            QFont("Calibri", 14),
            "Play"
        )

        self.audio_selection_button = self.configure_button(
            self.style().standardIcon(QStyle.SP_DirOpenIcon),
            self.open_audio_file
        )

        self.audio_line = Slider(Qt.Horizontal, self)
        self.audio_line.sliderMoved.connect(self.set_player_position)
        self.reset_audio_line()

        self.audio_list = QListWidget(self)

        self.grid_layout = self.configure_grid_layout()

        self.player = QMediaPlayer(self)
        self.player.stateChanged.connect(self.change_play_state)

        self.is_playing = False
        self.start_play_position = 0
        self.duration = None
        self.timer = None
        self.path = ''

    def configure_button(self, icon, clicked_event, font=None, name=None):
        if name is not None:
            button = QPushButton(name, self)
        else:
            button = QPushButton(self)

        if font is not None:
            button.setFont(font)

        button.setIcon(icon)
        button.clicked.connect(clicked_event)

        return button

    def reset_audio_line(self):
        self.audio_line.setRange(0, 0)
        self.audio_line.setValue(0)

    def open_audio_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        audio_paths = file_dialog.getOpenFileNames(self, "Open files", '/home', 'Audio Files (*.mp3 *.wav)')
        self.audio_list.addItems(audio_paths[0])

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
            self.path = path

        if not self.is_playing:
            self.change_play_state()

            url = QUrl.fromLocalFile(self.path)
            content = QMediaContent(url)

            self.player.setMedia(content)
            self.init_audio_line_length()
            self.player.setPosition(self.start_play_position)

            self.init_new_timer()
            self.player.play()
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
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.time_step)
        self.timer.start()

    def time_step(self):
        if self.is_playing:
            self.audio_line.setValue(self.audio_line.value() + 100)

    def init_audio_line_length(self):
        # TODO duration from ffmpeg
        input_ = 7.25

        self.duration = ceil(input_) * 1000
        self.audio_line.setRange(0, self.duration)

    def change_play_state(self):
        if self.duration is not None and self.duration - self.audio_line.value() <= 1000:
            self.finish_audio()

        if self.player.state() == QMediaPlayer.PlayingState:
            icon = QStyle.SP_MediaPause
            self.is_playing = True
            self.play_button.setText("Pause")
        else:
            icon = QStyle.SP_MediaPlay
            self.is_playing = False
            self.play_button.setText("Play")

        self.play_button.setIcon(self.style().standardIcon(icon))

    def finish_audio(self):
        self.duration = None
        self.start_play_position = 0
        self.player.stop()

        if self.timer is not None:
            self.timer.stop()

        self.reset_audio_line()

    def move_forward(self):
        self.audio_line.setValue(self.audio_line.value() + 100)
        self.player.setPosition(self.audio_line.value())

    def move_backward(self):
        self.audio_line.setValue(self.audio_line.value() - 100)
        self.player.setPosition(self.audio_line.value())

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
        grid_layout.addWidget(self.audio_line, 2, 2, 1, 7)
        grid_layout.addWidget(self.audio_list, 3, 0, 1, 9)

        self.centralWidget().setLayout(grid_layout)

        return grid_layout


if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = Window(application)
    window.show()
    sys.exit(application.exec_())
