from PyQt5.QtWidgets import QPushButton


def configure_button(self, clicked_event, icon=None, font=None, name=None):
    if name is not None:
        button = QPushButton(name, self)
    else:
        button = QPushButton(self)

    if font is not None:
        button.setFont(font)

    if icon is not None:
        button.setIcon(icon)

    button.clicked.connect(clicked_event)

    return button
