from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider

from model.time_utils import to_str_time


class Slider(QSlider):
    def __init__(self, orientation, main_window):
        self.main_window = main_window
        super(Slider, self).__init__(orientation, main_window)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            e.accept()
            x = e.pos().x()
            _max = self.maximum()
            _min = self.minimum()
            value = (_max - _min) * x / self.width() + _min
            audio_line_value = int(value - value % 1000)

            self.setValue(audio_line_value)
            self.main_window.user_timer.setText(
                to_str_time(audio_line_value // 1000, 0, 0)
            )
            self.main_window.set_player_position(audio_line_value)
