import sys
import json
import os
from functools import partial
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QDialogButtonBox
)

from PyQt6.QtGui import QFont

from pyskyq.remote import press_remote
from pyskyq.constants import REMOTECOMMANDS

CONFIG_FILE = "config.json"


# =========================
# Load / Save IP
# =========================
def load_ip():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get("skyq_ip")
        except Exception:
            return None
    return None


def save_ip(ip):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"skyq_ip": ip}, f)


# =========================
# Global IP variable
# =========================
SKYQ_HOST = load_ip()


# =========================
# Send remote command
# =========================
def send_command(cmd=None):
    global SKYQ_HOST

    try:
        if cmd is not None and SKYQ_HOST:
            press_remote(SKYQ_HOST, cmd)
    except Exception:
        pass


# =========================
# Button layout
# =========================
layout = [
    [None, "Sky", "IP", "Exit"],
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


# =========================
# Command map
# =========================
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


# =========================
# Button labels
# =========================
button_labels = {
    "Int": "Int",
    "BoxOffice": "BoxOf",
    "Services": "Serv",
    "TVGuide": "Guide",
    "Text": "txt",
    "Power": "⏻",
    "Rewind": "⏪",
    "Play/Pause": "⏯",
    "Fast Forward": "⏩",
    "Up": "⬆️",
    "Down": "⬇️",
    "Left": "⬅️",
    "Right": "➡️",
    "Select": "⚪",
    "Back": "🔙",
    "Home": "🏠",
    "Sidebar": "•••",
    "Ch Up": "Ʌ",
    "Ch Down": "V",
    "Help": "❓",
    "Search": "🔍",
    "Info": "ℹ️",
    "Red": "🔴",
    "Green": "🟢",
    "Yellow": "🟡",
    "Blue": "🔵",
    "Record": "Ⓡ",
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "Sky": "Sky",
    "Input": "→▭",
    "Vol Up": "🔊",
    "Vol Down": "🔉",
    "Mute": "🔇",
    "Mic": "🎤",
    "Exit": "❌",
    "IP": "IP"
}


# =========================
# Main window
# =========================
class SkyRemote(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sky Remote Control")

        # Ask for IP on first launch
        self.ensure_ip_exists()

        grid = QGridLayout()
        self.setLayout(grid)

        font = QFont("Segoe UI Emoji", 12, QFont.Weight.Bold)

        for r, row in enumerate(layout):
            for c, label in enumerate(row):

                if label is None:
                    spacer = QSpacerItem(
                        40,
                        40,
                        QSizePolicy.Policy.Expanding,
                        QSizePolicy.Policy.Expanding
                    )
                    grid.addItem(spacer, r, c)

                elif label == "Exit":
                    btn = QPushButton("❌")
                    btn.setFont(font)
                    btn.setFixedSize(55, 35)
                    btn.clicked.connect(self.close)
                    grid.addWidget(btn, r, c)

                elif label == "IP":
                    btn = QPushButton("IP")
                    btn.setFont(font)
                    btn.setFixedSize(55, 35)
                    btn.clicked.connect(self.change_ip)
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

    # =========================
    # Ask for IP if missing
    # =========================
    def ensure_ip_exists(self):
        global SKYQ_HOST

        if not SKYQ_HOST:
            self.change_ip(first_time=True)

    # =========================
    # Change IP dialog
    # =========================
    def change_ip(self, first_time=False):
        global SKYQ_HOST

        dialog = QDialog(self)
        dialog.setWindowTitle("Sky Q IP Address")

        layout = QVBoxLayout(dialog)

        label = QLabel("Enter Sky Q IP address:")
        layout.addWidget(label)

        ip_input = QLineEdit()
        ip_input.setPlaceholderText("e.g. 192.168.0.7")

        # Grey italic placeholder style
        ip_input.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
            }
        """)

        if SKYQ_HOST:
            ip_input.setText(SKYQ_HOST)

        layout.addWidget(ip_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )

        layout.addWidget(buttons)

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec():
            ip = ip_input.text().strip()

            if ip:
                SKYQ_HOST = ip
                save_ip(SKYQ_HOST)

                QMessageBox.information(
                    self,
                    "Saved",
                    f"Sky Q IP saved:\n{SKYQ_HOST}"
                )

            elif first_time:
                QMessageBox.warning(
                    self,
                    "Required",
                    "You must enter an IP address."
                )

                self.change_ip(first_time=True)

        elif first_time:
            QMessageBox.warning(
                self,
                "Required",
                "You must enter an IP address."
            )

            self.change_ip(first_time=True)

# =========================
# Start app
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = SkyRemote()
    win.show()

    sys.exit(app.exec())