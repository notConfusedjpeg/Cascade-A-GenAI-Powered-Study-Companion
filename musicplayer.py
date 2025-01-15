import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFileDialog, QDialog, QGridLayout, QSizePolicy, QMenu, QAction, QHBoxLayout, QMessageBox, QListWidget, QListWidgetItem, QPushButton, QSlider
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QTime, QTimer
from PyQt5.QtGui import QPixmap
import os
import resourcesCascade
import random
from tinytag import TinyTag

class PlaylistWindow(QDialog):
    playlist_clicked = pyqtSignal(int)

    def __init__(self, folder_path):
        super().__init__()
        icon = QtGui.QIcon(":/images/images for cascade/icon-musical-notes.png")
        self.setWindowIcon(icon)
        self.setWindowTitle("Playlists")
        self.setFixedSize(200, 200)

        self.layout = QGridLayout()
        self.folder_path = folder_path

        self.playlists = [("Lofi For Cascade", "Lofi For Cascade"), ("Playlist 2", None)]

        for i, (name, folder_name) in enumerate(self.playlists):
            if folder_name:
                image_path = self.load_album_art(os.path.join(self.folder_path, folder_name))
                if image_path:
                    image_label = QLabel()
                    pixmap = QPixmap(image_path).scaledToHeight(100)
                    image_label.setPixmap(pixmap)
                    image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                else:
                    image_label = QLabel("No Image Available")
            else:
                image_label = QLabel("No Image Available")

            playlist_button = QPushButton(name)
            playlist_button.clicked.connect(lambda state, x=i: self.playlist_clicked.emit(x))

            self.layout.addWidget(image_label, i, 0)
            self.layout.addWidget(playlist_button, i, 1)

        self.setLayout(self.layout)

    def load_album_art(self, playlist_folder_path):
        for file in os.listdir(playlist_folder_path):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                return os.path.join(playlist_folder_path, file)
        return None

class QueueWindow(QDialog):
    song_selected = pyqtSignal(str, str)  # Signal to send song and artist names

    def __init__(self, playlist):
        super().__init__()
        self.setWindowTitle("Queue")
        self.setFixedSize(400, 600)
        self.layout = QVBoxLayout()
        self.setStyleSheet("background-color: #d4a1d6;")

        self.bg_label = QLabel(self)
        self.bg_pixmap = QPixmap(":/images/bg_music.png").scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        self.bg_label.setPixmap(self.bg_pixmap)
        self.bg_label.setGeometry(self.rect())
        self.bg_label.lower()

        self.queue_list = QListWidget(self)
        for index in range(playlist.mediaCount()):
            media = playlist.media(index)
            media_path = media.canonicalUrl().toLocalFile()
            tag = TinyTag.get(media_path)
            song_name = tag.title if tag.title else "Unknown Title"
            artist_name = tag.artist if tag.artist else "Unknown Artist"
            list_item = QListWidgetItem(f"{song_name} - {artist_name}")
            self.queue_list.addItem(list_item)

        self.queue_list.itemClicked.connect(self.play_selected_song)
        
        # Clear Queue Button
        self.clear_queue_button = QPushButton("Clear Queue", self)
        self.clear_queue_button.clicked.connect(self.clear_queue)
        self.layout.addWidget(self.clear_queue_button, alignment=Qt.AlignTop | Qt.AlignRight)
        
        self.layout.addWidget(self.queue_list)
        self.setLayout(self.layout)
        self.playlist = playlist

    def play_selected_song(self, item):
        index = self.queue_list.row(item)
        self.playlist.setCurrentIndex(index)
        
        # Emit signal with song and artist names
        song_artist_text = item.text()
        song_name, artist_name = song_artist_text.split(" - ")
        self.song_selected.emit(song_name, artist_name)

    def clear_queue(self):
        self.queue_list.clear()
        self.playlist.clear()


class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music Player")
        self.setGeometry(100, 100, 700, 400)
        self.setStyleSheet("background-color: #d4a1d6;")

        self.layout = QVBoxLayout(self)

        self.music_title = QLabel("Music", self)  # Create the label and set its text
        self.music_title.setStyleSheet("background: transparent;\n"
"font: 25pt \"Montserrat\";\n"
"font-weight: bold;\n"
"color: rgb(167, 145, 203);\n"
"qproperty-alignment: AlignRight;\n"
"")
        self.layout.addWidget(self.music_title)

        # Hamburger Menu
        self.hamburger_menu_label = QLabel(self)
        self.hamburger_menu_icon = QPixmap(":/images/Menu.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.hamburger_menu_label.setPixmap(self.hamburger_menu_icon)
        self.hamburger_menu_label.setCursor(Qt.PointingHandCursor)
        self.hamburger_menu_label.mousePressEvent = self.open_menu
        self.hamburger_menu_label.setStyleSheet("background: none;")
        self.layout.addWidget(self.hamburger_menu_label, alignment=Qt.AlignTop | Qt.AlignRight)

        # Background Image
        self.bg_label = QLabel(self)
        self.bg_pixmap = QPixmap(":/images/bg_music.png").scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        self.bg_label.setPixmap(self.bg_pixmap)
        self.bg_label.setGeometry(self.rect())
        self.bg_label.lower()  # Make sure the background is behind other widgets

        # Album Art Container
        self.album_art_container = QWidget(self)
        self.album_art_container.setStyleSheet("background: transparent;")  # Remove any default container background
        self.album_art_container.setFixedSize(200, 150)  # Set a fixed size for the container

        # Album Art
        self.album_art_label = QLabel(self.album_art_container)
        self.album_art_label.setPixmap(QPixmap(":/images/images for cascade/default_album_art.png"))
        pixmap = QPixmap(":/images/images for cascade/default_album_art.png")
        scaled_pixmap = pixmap.scaledToWidth(200)  # Resize to 300 pixels wide
        self.album_art_label.setPixmap(scaled_pixmap)
        self.album_art_label.setStyleSheet("background: transparent;")
        self.album_art_label.setAlignment(Qt.AlignCenter)  # Center the album art within the container

        # Add the container to the main layout
        self.layout.addWidget(self.album_art_container, alignment=Qt.AlignCenter)

        # Song and Artist Labels
        self.song_label = QLabel("Song Name", self)
        self.artist_label = QLabel("Artist Name", self)

        self.song_label.setStyleSheet("font-size: 24px; background: none; color: white;")
        self.artist_label.setStyleSheet("font-size: 18px; background: none; color: white;")

        # Positioning song and artist labels
        self.song_label.setAlignment(Qt.AlignCenter)
        self.artist_label.setAlignment(Qt.AlignCenter)

        # Seek Bar
        self.seek_slider = QSlider(Qt.Horizontal, self)
        self.seek_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: none;
                background: #fff;
                height: 10px;
                border-radius: 0px;  }
            QSlider::sub-page:horizontal {
                background: #3b5998;
                border: none;
                height: 10px;
                border-radius: 0px;  }
            QSlider::add-page:horizontal {
                background: #fff;
                border: none;
                height: 10px;
                border-radius: 0px;  }
            QSlider::handle:horizontal {
                background: #3b5998;
                border: none;
                width: 15px;
                margin-top: -2px;
                margin-bottom: -2px;
                border-radius: 50%;  }
            QSlider::handle:horizontal:hover {
                background: #4a70c4;
                border: none;
                border-radius: 50%;  }
            QSlider::handle:horizontal:focus {
                border: none;
            }
        """)
        self.seek_slider.sliderMoved.connect(self.set_position)

        self.elapsed_time_label = QLabel("0:00", self)
        self.total_time_label = QLabel("0:00", self)
        self.elapsed_time_label.setStyleSheet("font-size: 20px; background: none; color: white;")
        self.total_time_label.setStyleSheet("font-size: 20px; background: none; color: white;")

        time_layout = QHBoxLayout()
        time_layout.addWidget(self.elapsed_time_label)
        time_layout.addWidget(self.seek_slider)
        time_layout.addWidget(self.total_time_label)

        # Play Controls Icons
        self.shuffle_icon = QPixmap(":/images/Shuffle.png")
        self.prev_icon = QPixmap(":/images/Previous.png")
        self.play_icon = QPixmap(":/images/Play.png")
        self.pause_icon = QPixmap(":/images/images for cascade/Pause.png")
        self.next_icon = QPixmap(":/images/Next.png")
        self.repeat_icon = QPixmap(":/images/Repeat.png")

        self.shuffle_label = QLabel(self)
        self.shuffle_label.setPixmap(self.shuffle_icon)
        self.shuffle_label.setCursor(Qt.PointingHandCursor)
        self.shuffle_label.mousePressEvent = self.shuffle_playlist
        self.shuffle_label.setStyleSheet("background: none;")

        self.prev_label = QLabel(self)
        self.prev_label.setPixmap(self.prev_icon)
        self.prev_label.setCursor(Qt.PointingHandCursor)
        self.prev_label.mousePressEvent = self.prev_song
        self.prev_label.setStyleSheet("background: none;")

        self.play_label = QLabel(self)
        self.play_label.setPixmap(self.play_icon)
        self.play_label.setCursor(Qt.PointingHandCursor)
        self.play_label.mousePressEvent = self.play_song
        self.play_label.setStyleSheet("background: none;")

        self.pause_label = QLabel(self)
        self.pause_label.setPixmap(self.pause_icon)
        self.pause_label.setCursor(Qt.PointingHandCursor)
        self.pause_label.mousePressEvent = self.pause_song
        self.pause_label.setStyleSheet("background: none;")
        self.pause_label.hide()  

        self.next_label = QLabel(self)
        self.next_label.setPixmap(self.next_icon)
        self.next_label.setCursor(Qt.PointingHandCursor)
        self.next_label.mousePressEvent = self.next_song
        self.next_label.setStyleSheet("background: none;")

        self.repeat_label = QLabel(self)
        self.repeat_label.setPixmap(self.repeat_icon)
        self.repeat_label.setCursor(Qt.PointingHandCursor)
        self.repeat_label.mousePressEvent = self.toggle_repeat
        self.repeat_label.setStyleSheet("background: none;")

        # Positioning Controls
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.shuffle_label)
        control_layout.addWidget(self.prev_label)
        control_layout.addWidget(self.play_label)
        control_layout.addWidget(self.pause_label)
        control_layout.addWidget(self.next_label)
        control_layout.addWidget(self.repeat_label)

        self.layout.addWidget(self.album_art_label)
        self.layout.addWidget(self.song_label)
        self.layout.addWidget(self.artist_label)
        self.layout.addLayout(time_layout)
        self.layout.addLayout(control_layout)

        self.setLayout(self.layout)

        self.playlist_folder = r"data"
        self.playlist_window = PlaylistWindow(self.playlist_folder)
        self.playlist_window.playlist_clicked.connect(self.open_playlist)  # Correctly connect the signal

        # Create the media player
        self.player = QMediaPlayer(self)
        self.playlist = QMediaPlaylist(self)
        self.player.setPlaylist(self.playlist)

        self.player.mediaStatusChanged.connect(self.update_song_info)
        self.player.stateChanged.connect(self.toggle_play_pause_button)  # Connect to toggle play/pause button
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)

        self.current_song_index = 0
        self.repeat_mode = False

    def resizeEvent(self, event):
        self.bg_pixmap = QPixmap(":/images/bg_music.png").scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        self.bg_label.setPixmap(self.bg_pixmap)
        self.bg_label.setGeometry(self.rect())
        super().resizeEvent(event)

    def prev_song(self, event):
        if self.current_song_index > 0:
            self.current_song_index -= 1
            self.playlist.setCurrentIndex(self.current_song_index)
            self.player.play()

    def next_song(self, event):
        if self.current_song_index < self.playlist.mediaCount() - 1:
            self.current_song_index += 1
            self.playlist.setCurrentIndex(self.current_song_index)
            self.player.play()

    def set_position(self, position):
        self.player.setPosition(position)

    def update_position(self, position):
        self.seek_slider.setValue(position)
        self.elapsed_time_label.setText(self.format_time(position))

    def update_duration(self, duration):
        self.seek_slider.setRange(0, duration)
        self.total_time_label.setText(self.format_time(duration))

    def format_time(self, ms):
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02}"

    def open_playlist(self, playlist_index):
        if playlist_index == 1:  # Playlist 2 is not available
            QMessageBox.information(self, "Playlist Unavailable", "Playlist 2 is not available yet.")
            return

        playlist_paths = [
            os.path.join(self.playlist_folder, "Lofi For Cascade")
        ]

        playlist_path = playlist_paths[playlist_index]
        self.playlist.clear()

        # Add all song files from the directory to the playlist
        for file in os.listdir(playlist_path):
            if file.lower().endswith(('.mp3', '.wav', '.m4a')):
                file_url = QUrl.fromLocalFile(os.path.join(playlist_path, file))
                file_content = QMediaContent(file_url)
                self.playlist.addMedia(file_content)

        self.current_song_index = 0
        self.playlist.setCurrentIndex(self.current_song_index)
        self.update_song_info(QMediaPlayer.PlayingState)  # Pass a dummy media status
        self.player.play()  # Start playing the first song in the playlist

    def open_menu(self, event):
        # Create the menu
        menu = QMenu(self)

        # Add actions to the menu
        add_songs_action = QAction("Add Songs", self)
        playlist_page_action = QAction("Playlist Page", self)
        view_queue_action = QAction("View Queue", self)

        add_songs_action.triggered.connect(self.add_songs)
        playlist_page_action.triggered.connect(self.open_playlist_window)
        view_queue_action.triggered.connect(self.view_queue)

        menu.addAction(add_songs_action)
        menu.addAction(playlist_page_action)
        menu.addAction(view_queue_action)

        # Adjust the position to be relative to the hamburger icon
        position = self.hamburger_menu_label.mapToGlobal(self.hamburger_menu_label.rect().bottomLeft())
        menu.exec_(position)

    def add_songs(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Audio Files (*.mp3 *.wav *.m4a)")
        if file_dialog.exec_():
            file_urls = file_dialog.selectedUrls()

            for file_url in file_urls:
                file_path = file_url.toLocalFile()

                if os.path.exists(file_path):
                    file_url = QUrl.fromLocalFile(file_path)
                    file_content = QMediaContent(file_url)

                    self.playlist.addMedia(file_content)

                    tag = TinyTag.get(file_path)
                    song_name = tag.title if tag.title else "Unknown Title"
                    artist_name = tag.artist if tag.artist else "Unknown Artist"

                    if self.playlist.mediaCount() == 1:
                        self.song_label.setText(song_name)
                        self.artist_label.setText(artist_name)

                    # If a song is already playing, keep the current song labels
                    if self.player.state() == QMediaPlayer.PlayingState:
                        current_media = self.playlist.currentMedia()
                        if not current_media.isNull():
                            current_media_path = current_media.canonicalUrl().toLocalFile()
                            if current_media_path == file_path:
                                self.song_label.setText(song_name)
                                self.artist_label.setText(artist_name)

                    # If the playlist was empty and we added a song, start playing it
                    if self.playlist.mediaCount() == 1:
                        self.playlist.setCurrentIndex(0)
                        self.player.play()

                else:
                    QMessageBox.warning(self, "File Not Found", f"File not found: {file_path}")

            if self.playlist.mediaCount() > 1:
                QMessageBox.information(self, "Songs Added", "Songs added to the playlist.")


    def open_playlist_window(self):
        self.playlist_window.exec_()

    def view_queue(self):
        queue_window = QueueWindow(self.playlist)
        queue_window.song_selected.connect(self.update_song_labels)  # Connect to update song labels
        queue_window.exec_()

    def play_song(self, event):
        self.player.play()

    def pause_song(self, event):
        self.player.pause()
        

    def shuffle_playlist(self, event):
        if self.playlist.mediaCount() == 0:
            QMessageBox.information(self, "Shuffle Playlist", "No songs in the playlist to shuffle.")
            return

        indices = list(range(self.playlist.mediaCount()))
        random.shuffle(indices)
        media_list = []

        # Collect media in the shuffled order
        for index in indices:
            media = self.playlist.media(index)
            media_list.append(media)

        self.playlist.clear()  # Clear the current playlist

        # Add the media back in shuffled order
        for media in media_list:
            self.playlist.addMedia(media)

        self.current_song_index = 0
        self.playlist.setCurrentIndex(self.current_song_index)  # Reset to the first song
        self.player.play()  # Start playing the first song

    def toggle_repeat(self, event):
        if self.repeat_mode:
            self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
            self.repeat_mode = False
        else:
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
            self.repeat_mode = True

    def toggle_play_pause_button(self, state):
        if state == QMediaPlayer.PlayingState:
            self.play_label.hide()
            self.pause_label.show()
        else:
            self.pause_label.hide()
            self.play_label.show()

    def update_song_info(self, status):
        song_name = "Unknown Title"
        artist_name = "Unknown Artist"

        if status == QMediaPlayer.BufferedMedia or status == QMediaPlayer.LoadedMedia:
            if self.player.state() != QMediaPlayer.StoppedState:
                current_media = self.playlist.currentMedia()
                if not current_media.isNull():
                    media_path = current_media.canonicalUrl().toLocalFile()
                    if os.path.exists(media_path):
                        try:
                            tag = TinyTag.get(media_path)
                            song_name = tag.title if tag.title else "Unknown Title"
                            artist_name = tag.artist if tag.artist else "Unknown Artist"
                        except Exception as e:
                            error_message = str(e)
                            if "0x80040266" in error_message:
                                reply = QMessageBox.question(self, 'Error: DirectShowPlayerService::doRender',
                                                            "DirectShowPlayerService::doRender: Unknown error 0x80040266\n"
                                                            "You may need additional codecs to play this file.\n"
                                                            "Do you want to download and install K-Lite Codec Pack?",
                                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                                if reply == QMessageBox.Yes:
                                    import webbrowser
                                    webbrowser.open("https://files2.codecguide.com/K-Lite_Codec_Pack_1840_Basic.exe")
                                    QMessageBox.information(self, "Installation Required",
                                                            "Please download and install the K-Lite Codec Pack to play the file.")
                    else:
                        QMessageBox.warning(self, "File Not Found", f"File not found: {media_path}")

        self.song_label.setText(song_name)
        self.artist_label.setText(artist_name)



    def update_song_labels(self, song_name, artist_name):
        self.song_label.setText(song_name)
        self.artist_label.setText(artist_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicPlayer()
    window.show()
    sys.exit(app.exec_())

