import sys
import time

from PyQt6.QtCore import QUrl, Qt, QSize, QSizeF, QRectF, pyqtSignal
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QButtonGroup, QLabel, QDialog, QDialogButtonBox, QVBoxLayout, \
    QTextBrowser, QTextEdit, QMessageBox, QFileDialog, QGraphicsScene, QGraphicsRectItem, QGraphicsItem
from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMessageBox
from func_ffprobe import *
from func_timeout import func_set_timeout, FunctionTimedOut
import threading
def ms_to_hours(millis):
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    hours = (millis / (1000 * 60 * 60)) % 24
    hours = int(hours)
    lay = millis - hours * 1000 * 60 * 60 - minutes * 1000 * 60 - seconds * 1000

    return ("%d:%d:%d.%d" % (hours, minutes, seconds, lay))
def name(millis):
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    hours = (millis / (1000 * 60 * 60)) % 24
    hours = int(hours)
    return ("%d—%d—%d" % (hours, minutes, seconds))

class temp_video_dialog(QMainWindow):
    def __init__(self,video_url='temp/temp.mp4'):
        super().__init__()
        self.ui=uic.loadUi("video_temp.ui")

        self.sld_video_pressed = False  # 判断当前进度条识别否被鼠标点击
        self.on_off = True
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 700, 394)
        self.video_widget = QGraphicsVideoItem()
        self.media_player = QMediaPlayer()
        self.scene.addItem(self.video_widget)
        self.video_url=video_url
        self.media_player.setSource(QUrl.fromLocalFile(self.video_url))
        self.media_player.setVideoOutput(self.video_widget)
        # self._audio_output = QAudioOutput()  ##
        # self.media_player.setAudioOutput(self._audio_output)  ##
        self.ui.graphicsView.setScene(self.scene)

        # 设置视图和视频项的布局选项
        self.ui.graphicsView.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_widget.setSize(QSizeF(self.ui.graphicsView.size()))

        self.ui.btn_play.clicked.connect(self.play_tog)  # play
        self.media_player.positionChanged.connect(self.changeSlide)  # change Slide

        self.ui.sld_video.setTracking(False)
        self.ui.sld_video.sliderReleased.connect(self.releaseSlider)
        self.ui.sld_video.sliderPressed.connect(self.pressSlider)
        self.ui.sld_video.sliderMoved.connect(self.moveSlider)  # 进度条拖拽跳转
        self.media_player.play()

    def show(self):
        self.ui.show()

    def moveSlider(self, position):
        self.sld_video_pressed = True
        if self.media_player.duration() > 0:  # 开始播放后才允许进行跳转
            video_position = int((position / 100) * self.media_player.duration())

            self.media_player.setPosition(video_position)
            self.ui.lab_video.setText("%.2f%%" % position)
            self.ui.lab_time.setText(ms_to_hours(position))

    def pressSlider(self):
        self.sld_video_pressed = True


    def releaseSlider(self):
        self.sld_video_pressed = False
    def set_video(self,video_fille):
        self.video_url = video_fille
        self.media_player.setSource(QUrl.fromLocalFile(self.video_url))

    def changeSlide(self, position):
        if not self.sld_video_pressed:  # 进度条被鼠标点击时不更新
            self.vidoeLength = self.media_player.duration()+0.1
            self.ui.sld_video.setValue(round((position/self.vidoeLength)*100))
            self.ui.lab_time.setText(ms_to_hours(position))
            self.ui.lab_video.setText("%.2f%%" % ((position/self.vidoeLength)*100))
            self.ui.lab_time_2.setText(ms_to_hours(self.media_player.duration()))


    def play_tog(self):

        if self.on_off:
            self.media_player.pause()
            self.on_off=False
        else:
            self.media_player.play()
            self.on_off = True




if __name__=="__main__":
    app=QApplication(sys.argv)
    # 将 excepthook 函数设置为全局异常处理函数
    window=temp_video_dialog()
    window.show()

    sys.exit(app.exec())

