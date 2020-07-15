import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt, QTimer
import random
import time
from pygame import mixer
from mutagen.mp3 import MP3
import style    # style.py file holds the style settings

music_list = []
mixer.init()    # initialize mixer
slider_level = 0
play_clicked = 0
count = 0


class Player(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Player")
        self.setGeometry(450, 150, 480, 700)
        self.ui()
        self.show()

    def ui(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # ############ Progress Bar #############################
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(style.progressbar_style())  # using function from our style.py file

        # ############ Timer ####################################
        self.timer = QTimer()
        self.timer.setInterval(1000)  # how often to update the progress bar (1s = 1000ms)
        self.timer.timeout.connect(self.update_progress_bar)

        # ###################### Labels ########################
        self.song_timer_label = QLabel("00:00")
        self.song_length_label = QLabel("/ 00:00")

        # ###################### Buttons ########################
        # We use QToolButtons instead of QPushbuttons this time - better when buttons have images (otherwise, similar)
        self.add_button = QToolButton() # create a button
        self.add_button.setIcon(QIcon("icons/add.png"))    # add an icon for the button
        self.add_button.setIconSize(QSize(48, 48))
        self.add_button.setToolTip("Add Songs")
        self.add_button.clicked.connect(self.add_song)

        self.shuffle_button = QToolButton()
        self.shuffle_button.setIcon(QIcon('icons/shuffle.png'))
        self.shuffle_button.setIconSize(QSize(48, 48))
        self.shuffle_button.setToolTip('Shuffle Playlist')
        self.shuffle_button.clicked.connect(self.shuffle_playlist)

        self.previous_button = QToolButton()
        self.previous_button.setIcon(QIcon('icons/previous.png'))
        self.previous_button.setIconSize(QSize(48, 48))
        self.previous_button.setToolTip('Previous Song')
        self.previous_button.clicked.connect(self.previous_song)

        self.next_button = QToolButton()
        self.next_button.setIcon(QIcon('icons/next.png'))
        self.next_button.setIconSize(QSize(48, 48))
        self.next_button.setToolTip('Next Song')
        self.next_button.clicked.connect(self.next_song)

        self.play_button = QToolButton()
        self.play_button.setIcon(QIcon('icons/play.png'))
        self.play_button.setIconSize(QSize(64, 64))
        self.play_button.setToolTip('Play')
        self.play_button.clicked.connect(self.play_song)

        self.mute_button = QToolButton()
        self.mute_button.setIcon(QIcon('icons/unmuted.png'))
        self.mute_button.setIconSize(QSize(24, 24))
        self.mute_button.setToolTip('Mute')
        self.mute_button.clicked.connect(self.mute_volume)

        # ################## Volume slider #####################
        self.volume_slider = QSlider(Qt.Horizontal)  # create slider and set it to be horizontal
        self.volume_slider.setValue(70)  # set initial value slider position at 70 so that not too loud and not too low
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setToolTip(f'Volume: {self.volume_slider.value()}%')
        mixer.music.set_volume(0.7)  # mixer volume range is between 0 and 1. 0.7 value is same as setVolume(70)
        self.volume_slider.valueChanged.connect(self.set_volume)

        # ################## Playlist ##########################
        self.playlist = QListWidget()
        self.playlist.doubleClicked.connect(self.double_click)  # play song by double-clicking its name in the playlist
        self.playlist.setStyleSheet(style.playlist_style())

    def layouts(self):
        # ############ Creating layouts #########################
        self.main_layout = QVBoxLayout()
        self.top_main_layout = QVBoxLayout()
        # we cannot use StyleSheet on layouts, but can use QGroupBox to put those layouts in and then apply styles on it
        self.top_groupbox = QGroupBox("Music Player")
        self.top_groupbox.setStyleSheet(style.groupbox_style())  # we use the function from our style.py file
        # groupbox_style() function has no self. prefix and includes (), as it will be created outside our current class
        self.top_layout = QHBoxLayout()
        self.middle_layout = QHBoxLayout()
        self.bottom_layout = QVBoxLayout()

        # ############ Adding widgets to layouts #################
        # ============= Top layout widgets =======================
        self.top_layout.addWidget(self.progress_bar)
        self.top_layout.addWidget(self.song_timer_label)
        self.top_layout.addWidget(self.song_length_label)

        # ============= Middle layout widgets ====================
        self.middle_layout.addStretch()
        self.middle_layout.addWidget(self.add_button)
        self.middle_layout.addWidget(self.shuffle_button)
        self.middle_layout.addWidget(self.play_button)
        self.middle_layout.addWidget(self.previous_button)
        self.middle_layout.addWidget(self.next_button)
        self.middle_layout.addWidget(self.volume_slider)
        self.middle_layout.addWidget(self.mute_button)
        self.middle_layout.addStretch()

        # ============= Bottom layout widgets ====================
        self.bottom_layout.addWidget(self.playlist)

        # ############ Adding child layouts to main layout ######
        self.top_main_layout.addLayout(self.top_layout)
        self.top_main_layout.addLayout(self.middle_layout)
        self.top_groupbox.setLayout(self.top_main_layout)
        self.main_layout.addWidget(self.top_groupbox, 25)   # though note Groupbox is a widget, NOT a layout
        self.main_layout.addLayout(self.bottom_layout, 75)
        self.setLayout(self.main_layout)

    def add_song(self):
        directory = QFileDialog.getOpenFileNames(self, "Add Song", "", "Audio files (*.wav, *.ogg, *.mp3)")
        for song in directory[0]:
            filename = os.path.basename(song)
            self.playlist.addItem(filename)
            music_list.append(song)

    def shuffle_playlist(self):
        random.shuffle(music_list)
        self.playlist.clear()
        for song in music_list:
            filename = os.path.basename(song)
            self.playlist.addItem(filename)

    def double_click(self):
        global play_clicked
        global count

        index = self.playlist.currentRow()
        try:
            self.list_index = music_list[index]
            mixer.music.load(str(self.list_index))
            mixer.music.play()
            self.play_button.setIcon(QIcon('icons/pause.png'))
            self.play_button.setToolTip('Pause')
            count = 0  # reset progress bar counter before a new song starts
            self.timer.start()
            song = MP3(str(music_list[index]))
            self.song_length = round(song.info.length)  # rounding the duration to seconds only (no decimal point)
            self.progress_bar.setValue(0)   # reset progress bar before a new song starts
            self.progress_bar.setMaximum(self.song_length)
            minute, sec = divmod(self.song_length, 60)  # convert seconds to min:sec
            self.song_length_label.setText(f"/ {minute:02d}:{sec}")
            play_clicked = 1
        except:
            QMessageBox.information(self, "Warning", "File not selected or cannot be played")

    def play_song(self):
        global play_clicked
        if play_clicked == 0:
            self.double_click()
        elif play_clicked == 1:
            mixer.music.pause()
            self.play_button.setIcon(QIcon('icons/play.png'))
            self.play_button.setToolTip('Resume')
            self.timer.stop()
            play_clicked = 2
        else:
            index = self.playlist.currentRow()
            if music_list[index] == self.list_index:
                mixer.music.unpause()
                self.play_button.setIcon(QIcon('icons/pause.png'))
                self.play_button.setToolTip('Pause')
                self.timer.start()
                play_clicked = 1
            else:
                self.double_click()

    def set_volume(self):
        self.mute_button.setIcon(QIcon('icons/unmuted.png'))
        volume = self.volume_slider.value()
        self.volume_slider.setToolTip(f'Volume: {volume}%')
        mixer.music.set_volume(volume / 100)

    def mute_volume(self):
        global slider_level
        volume_level = mixer.music.get_volume()
        if volume_level != 0:
            slider_level = self.volume_slider.value()
            mixer.music.set_volume(0.0)
            self.volume_slider.setValue(0)
            self.mute_button.setIcon(QIcon('icons/mute.png'))
            self.mute_button.setToolTip('Unmute')
        else:
            mixer.music.set_volume(slider_level / 100)
            self.volume_slider.setValue(slider_level)
            self.mute_button.setIcon(QIcon('icons/unmuted.png'))
            self.mute_button.setToolTip('Mute')

    def update_progress_bar(self):
        global count
        count += 1
        self.progress_bar.setValue(count)
        self.song_timer_label.setText(time.strftime("%M:%S", time.gmtime(count)))   # use time functions to get min:sec
        if count == self.song_length:
            self.timer.stop()

    def previous_song(self):
        current_row = self.playlist.currentRow()
        items = self.playlist.count()
        if current_row == 0:
            current_row = items
        current_row -= 1
        self.playlist.setCurrentRow(current_row)
        self.double_click()

    def next_song(self):
        current_row = self.playlist.currentRow()
        current_row += 1
        items = self.playlist.count()
        if current_row == items:
            current_row = 0
        self.playlist.setCurrentRow(current_row)
        self.double_click()


def main():
    app = QApplication(sys.argv)
    window = Player()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
