import sys

from PyQt5.QtCore import Qt, QThreadPool, QUrl
from PyQt5.QtGui import QPixmap, QImage, QFont
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
    QScrollArea, QStyle, QListWidget, QSlider
)
from PyQt5.uic.properties import QtCore


class Window(QMainWindow):
    def __init__(self, app):
        super(Window, self).__init__()
        self.app = app

        self.setWindowTitle("Audio Editor")
        self.init_center_geometry()

        self.state = "Play"
        self.position = 0

        self.title_label = QLabel("Audio Editor")
        self.title_label.setFont(QFont("Calibri", 20))
        self.title_label.setAlignment(Qt.AlignCenter)

        self.rewind_left_button = QPushButton(self)
        self.rewind_left_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.rewind_left_button.clicked.connect(self.move_backward)

        self.rewind_right_button = QPushButton(self)
        self.rewind_right_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.rewind_right_button.clicked.connect(self.move_forward)

        self.play_button = QPushButton("Play", self)
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.setFont(QFont("Calibri", 14))
        self.play_button.clicked.connect(self.play_audio)

        self.audio_selection_button = QPushButton(self)
        self.audio_selection_button.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        self.audio_selection_button.clicked.connect(self.open_audio_file)

        self.audio_line = QSlider(Qt.Horizontal, self)
        self.audio_line.setRange(0, 0)
        # self.audio_line.sliderMoved.connect(self.set_position)

        self.audio_list = QListWidget(self)

        self.grid_layout = self.configure_grid_layout()

        self.player = QMediaPlayer(self)
        self.player.positionChanged.connect(self.move_slider)
        self.player.durationChanged.connect(self.init_audio_line_length)
        self.player.stateChanged.connect(self.change_state_icon)

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
        else:
            path = self.audio_list.currentItem().text()

        if self.state == "Play":
            self.play_button.setText("Pause")
            self.state = "Pause"
            url = QUrl.fromLocalFile(path)
            content = QMediaContent(url)
            self.player.setMedia(content)
            if self.position != 0:
                self.player.setPosition(self.position)
                self.player.play()
        else:
            self.play_button.setText("Play")
            self.state = "Play"
            self.player.pause()
            paused = self.player.position()
            self.position = paused

    def set_position(self, position):
        self.player.setPosition(position)

    def move_slider(self):
        print(1)
        self.audio_line.setValue(self.player.position())

    def init_audio_line_length(self, duration):
        print(duration)
        self.audio_line.setRange(0, duration)

        if self.position == 0:
            self.player.setPosition(self.position)
            self.player.play()

    def change_state_icon(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            icon = QStyle.SP_MediaPause
        else:
            icon = QStyle.SP_MediaPlay

        self.play_button.setIcon(self.style().standardIcon(icon))

    def move_forward(self):
        self.player.setPosition(int(self.player.position()) + 1000)

    def move_backward(self):
        self.player.setPosition(int(self.player.position()) - 1000)

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
