import sys
from functools import partial
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont
from pyskyq.remote import press_remote
from pyskyq.constants import REMOTECOMMANDS

SKYQ_HOST = "192.168.0.7"  # Replace with your SkyQ box IP

def send_command(cmd=None):
    try:
        if cmd is not None:
            press_remote(SKYQ_HOST, cmd)
    except Exception:
        pass  # completely silent

layout = [
    [None, "Sky", None, "Exit"],
    ["Power", None, "Input", None],
    ["Rewind", "Play/Pause", "Fast Forward", None],
    [None, "Up", None, None],
    ["Left", "Select", "Right", None],
    [None, "Down", None, None],
    ["Back", "Home", "Sidebar", None],
    ["Vol Up", "Mic", "Ch Up", None],
    ["Vol Down", "Record", "Ch Down", None],
    ["Mute", "Help", "Search", "Info"],
    ["Red", "Green", "Yellow", "Blue"],
    ["1", "2", "3", None],
    ["4", "5", "6", None],
    ["7", "8", "9", None],
    [None, "0", None, None]
]

command_map = {
    "Int": REMOTECOMMANDS.interactive,
    "BoxOffice": REMOTECOMMANDS.boxoffice,
    "Services": REMOTECOMMANDS.services,
    "TVGuide": REMOTECOMMANDS.tvguide,
    "Text": REMOTECOMMANDS.text,
    "Sky": REMOTECOMMANDS.sky,
    "Power": REMOTECOMMANDS.power,
    "Rewind": REMOTECOMMANDS.rewind,
    "Play/Pause": REMOTECOMMANDS.play,
    "Fast Forward": REMOTECOMMANDS.fastforward,
    "Up": REMOTECOMMANDS.up,
    "Down": REMOTECOMMANDS.down,
    "Left": REMOTECOMMANDS.left,
    "Right": REMOTECOMMANDS.right,
    "Select": REMOTECOMMANDS.select,
    "Back": REMOTECOMMANDS.dismiss,
    "Home": REMOTECOMMANDS.home,
    "Sidebar": REMOTECOMMANDS.sidebar,
    "Ch Up": REMOTECOMMANDS.channelup,
    "Ch Down": REMOTECOMMANDS.channeldown,
    "Help": REMOTECOMMANDS.help,
    "Search": REMOTECOMMANDS.search,
    "Info": REMOTECOMMANDS.i,
    "Red": REMOTECOMMANDS.red,
    "Green": REMOTECOMMANDS.green,
    "Yellow": REMOTECOMMANDS.yellow,
    "Blue": REMOTECOMMANDS.blue,
    "Record": REMOTECOMMANDS.record,
    "0": REMOTECOMMANDS.zero,
    "1": REMOTECOMMANDS.one,
    "2": REMOTECOMMANDS.two,
    "3": REMOTECOMMANDS.three,
    "4": REMOTECOMMANDS.four,
    "5": REMOTECOMMANDS.five,
    "6": REMOTECOMMANDS.six,
    "7": REMOTECOMMANDS.seven,
    "8": REMOTECOMMANDS.eight,
    "9": REMOTECOMMANDS.nine
}

button_labels = {
    "Int": "Int", "BoxOffice": "BoxOf", "Services": "Serv", "TVGuide": "Guide", "Text": "txt",
    "Power": "⏻", "Rewind": "⏪", "Play/Pause": "⏯", "Fast Forward": "⏩",
    "Up": "⬆️", "Down": "⬇️", "Left": "⬅️", "Right": "➡️", "Select": "⚪",
    "Back": "🔙", "Home": "🏠", "Sidebar": "•••", "Ch Up": "Ʌ", "Ch Down": "V",
    "Help": "❓", "Search": "🔍", "Info": "ℹ️",
    "Red": "🔴", "Green": "🟢", "Yellow": "🟡", "Blue": "🔵", "Record": "Ⓡ",
    "0": "0", "1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6",
    "7": "7", "8": "8", "9": "9", "Sky": "Sky", "Input": "→▭",
    "Vol Up": "🔊", "Vol Down": "🔉", "Mute": "🔇", "Mic": "🎤", "Exit": "❌", "none": ""
}

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QSpacerItem, QSizePolicy

class SkyRemote(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sky Remote Control")
        grid = QGridLayout()
        self.setLayout(grid)

        font = QFont("Segoe UI Emoji", 12, QFont.Weight.Bold)

        for r, row in enumerate(layout):
            for c, label in enumerate(row):
                if label is None:
                    spacer = QSpacerItem(40, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                    grid.addItem(spacer, r, c)
                elif label == "Exit":
                    btn = QPushButton("❌")
                    btn.setFont(font)
                    btn.setFixedSize(55, 35)
                    btn.clicked.connect(self.close)
                    grid.addWidget(btn, r, c)
                else:
                    cmd = command_map.get(label)
                    btn = QPushButton(button_labels.get(label, label))
                    btn.setFont(font)
                    btn.setFixedSize(55, 35)
                    btn.clicked.connect(partial(send_command, cmd))
                    grid.addWidget(btn, r, c)

        for i in range(max(len(r) for r in layout)):
            grid.setColumnStretch(i, 1)
        for i in range(len(layout)):
            grid.setRowStretch(i, 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SkyRemote()
    win.show()
    sys.exit(app.exec())
