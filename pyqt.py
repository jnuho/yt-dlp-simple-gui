import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QLineEdit, QPushButton, QLabel, QProgressBar, 
                           QHBoxLayout)  # Added QHBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal
import yt_dlp

# UpdateWorker and DownloadWorker classes remain the same
class UpdateWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def run(self):
        try:
            # Try to use uv with absolute path first, fall back to pip if it fails
            try:
               # Determine uv path based on operating system
                print(sys.platform)
                username = os.getlogin()  # Works on both Windows and Unix-like systems
                if sys.platform == "win32":
                    uv_path = f"C:/Users/{username}/.local/bin/uv.exe"
                else:
                    uv_path = f"/Users/{username}/.local/bin/uv"
                subprocess.run([uv_path, "pip", "install", "--upgrade", "yt-dlp"], 
                             check=True, capture_output=True)
            except (FileNotFoundError, subprocess.CalledProcessError):
                # uv failed, use standard pip instead
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], 
                             check=True, capture_output=True)
            self.finished.emit()
        except subprocess.CalledProcessError as e:
            self.error.emit(f"Update failed: {e.stderr.decode() if e.stderr else str(e)}")
        except Exception as e:
            self.error.emit(f"Update failed: {str(e)}")

class DownloadWorker(QThread):
    progress = pyqtSignal(dict)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def progress_hook(self, d):
        self.progress.emit(d)

    def run(self):
        try:
            download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            ydl_opts = {
                'format': 'bestvideo[ext=webm]+bestaudio[ext=m4a]/best',
                'merge_output_format': 'mp4',
                'progress_hooks': [self.progress_hook],
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s')
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

class YouTubeDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 600, 200)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create URL input
        self.url_label = QLabel("Enter YouTube URL:")
        self.url_input = QLineEdit()
        
        # Create horizontal layout for buttons
        button_layout = QHBoxLayout()
        
        # Create download button
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.start_download)
        
        # Create exit button
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)  # QMainWindow's close method
        
        # Add buttons to horizontal layout
        button_layout.addWidget(self.download_button)
        button_layout.addWidget(self.exit_button)

        # Create progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        # Create status label
        self.status_label = QLabel("")

        # Add widgets to main layout
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addLayout(button_layout)  # Add the horizontal button layout
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)

        self.worker = None
        self.update_worker = None
        
        # Start update check when application launches
        self.check_for_updates()

    def check_for_updates(self):
        self.download_button.setEnabled(False)
        self.status_label.setText("Checking for yt-dlp updates...")
        
        self.update_worker = UpdateWorker()
        self.update_worker.finished.connect(self.update_finished)
        self.update_worker.error.connect(self.update_error)
        self.update_worker.start()

    def update_finished(self):
        self.download_button.setEnabled(True)
        self.status_label.setText("yt-dlp updated successfully!")

    def update_error(self, error_message):
        self.download_button.setEnabled(True)
        self.status_label.setText(f"Update error: {error_message}")

    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            self.status_label.setText("Please enter a valid URL")
            return

        self.download_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_label.setText("Downloading...")

        self.worker = DownloadWorker(url)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.download_finished)
        self.worker.error.connect(self.download_error)
        self.worker.start()

    def update_progress(self, d):
        if d['status'] == 'downloading':
            try:
                percentage = d['_percent_str'].replace('%','').strip()
                self.progress_bar.setValue(float(percentage))
            except:
                pass

    def download_finished(self):
        self.download_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("Download completed!")
        self.url_input.clear()

    def download_error(self, error_message):
        self.download_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Error: {error_message}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec())