from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider


class Slider(QSlider):
    def __init__(self, orientation, main_window):
        self.main_window = main_window
        super(Slider, self).__init__(orientation, main_window)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            e.accept()
            x = e.pos().x()
            value = (self.maximum() - self.minimum()) * x / self.width() + self.minimum()
            self.setValue(int(value - value % 1000))
            self.main_window.set_player_position(self.value())
