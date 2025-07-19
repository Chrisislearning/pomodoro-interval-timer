
from PySide6.QtWidgets import QWidget, QTimeEdit, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout, QCheckBox, QDialog, QDialogButtonBox
from PySide6.QtCore import Qt, QSize, QTime, QTimer, Signal

class Timer(QWidget):
    renamed = Signal(str, str)

    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.initial_time = QTime(0, 0, 0)
        self.timer = None
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        title_bar = QWidget()
        title_layout = QHBoxLayout()
        title_bar.setLayout(title_layout)
        main_layout.addWidget(title_bar)
        self.title = QLabel()
        title_layout.addWidget(self.title, alignment=Qt.AlignHCenter)
        title_rename = QPushButton('rename...')
        title_rename.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        title_layout.addWidget(title_rename)
        title_rename.clicked.connect(self.rename_timer)
        timer_group = QWidget()
        group_layout = QGridLayout()
        timer_group.setLayout(group_layout)
        label = QLabel('set time:')
        group_layout.addWidget(label, 0, 0)
        self.setting_time = QTimeEdit()
        self.setting_time.setDisplayFormat('mm:ss')
        group_layout.addWidget(self.setting_time, 0, 1)
        self.setting_time.userTimeChanged.connect(self.time_changed)
        self.time_label = QLabel('00:00')
        group_layout.addWidget(self.time_label, 0, 2)
        button_start = QPushButton('start')
        group_layout.addWidget(button_start, 0, 3)
        button_start.clicked.connect(self.countdown)
        button_pause = QPushButton('pause')
        group_layout.addWidget(button_pause, 0, 4)
        button_pause.clicked.connect(self.time_paused)
        button_reset = QPushButton('reset')
        group_layout.addWidget(button_reset, 0, 5)
        button_reset.clicked.connect(self.time_resetted)
        self.sound_checkbox = QCheckBox('play a sound at the end')
        group_layout.addWidget(self.sound_checkbox, 1, 0, 1, 3)
        file_button = QPushButton('choose a sound file')
        group_layout.addWidget(file_button, 1, 5)
        self.next_button = QCheckBox('start next timer automatically')
        group_layout.addWidget(self.next_button, 2, 0, 1, 3)
        main_layout.addWidget(timer_group)

    def time_changed(self):
        self.initial_time = self.setting_time.time()
        self.time_label.setText(self.initial_time.toString('mm:ss'))

    def countdown(self):
        if self.initial_time == QTime(0, 0, 0):
            return
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        if self.initial_time > QTime(0, 0, 0):
            self.initial_time = self.initial_time.addSecs(-1)
            self.time_label.setText(self.initial_time.toString('mm:ss'))
        if self.initial_time == QTime(0, 0, 0):
            if self.timer:
                self.timer.stop()
            self.time_label.setText('00:00')
            if self.next_button.isChecked():
                self.start_next_timer()

    def start_next_timer(self):
        if not self.parent_window:
            return
        timers = list(self.parent_window.timers_dict.values())
        try:
            index = timers.index(self)
            if index + 1 < len(timers):
                next_timer = timers[index + 1]
                next_timer.countdown()
        except ValueError:
            print("Timer not found in parent's list.")
        else:
            pass

    def time_paused(self):
        if self.timer:
            self.timer.stop()

    def time_resetted(self):
        if self.timer:
            self.timer.stop()
        reset = QTime(0, 0, 0)
        self.setting_time.setTime(reset)
        self.time_label.setText('00:00')
        self.initial_time = reset

    def rename_timer(self):
        dialog = Rename(self)
        if dialog.exec():
            new_name = dialog.new_name.text()
            old_name = self.title.text()
            self.title.setText(new_name)
            self.renamed.emit(old_name, new_name)

class Rename(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('rename the timer')
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout = QVBoxLayout()
        self.new_name = QLineEdit()
        layout.addWidget(self.new_name)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
        
