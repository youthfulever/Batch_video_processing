import sys
import time

from PyQt6.QtCore import QUrl, Qt, QSize, QSizeF, QRectF, pyqtSignal
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QButtonGroup, QLabel, QDialog, QDialogButtonBox, QVBoxLayout, \
    QTextBrowser, QTextEdit, QMessageBox, QFileDialog, QGraphicsScene, QGraphicsRectItem, QGraphicsItem, \
    QTableWidgetItem
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


def calculate_time_difference(time1, time2):
    format_str = '%H:%M:%S.%f'
    dt1 = datetime.strptime(time1, format_str)
    dt2 = datetime.strptime(time2, format_str)
    time_diff = dt2 - dt1

    return int(time_diff.total_seconds() * 1000)
from video_wenan import Ui_Dialog
class Wenan_dialog(Ui_Dialog,QDialog):
    def __init__(self, video_url='logo.mp4', out_time_ss=[], out_time_to=[], out_text=[]):

        super().__init__()
        super(Ui_Dialog).__init__()
        self.setupUi(self)
# class Wenan_dialog(QMainWindow):
#     Wenan_dialog_close = pyqtSignal(str)
#     def __init__(self, video_url='logo.mp4', out_time_ss=[], out_time_to=[], out_text=[]):
#         super().__init__()
#         self = uic.loadUi("data/ui/video_wenan.ui")

        self.sld_video_pressed = False  # 判断当前进度条识别否被鼠标点击
        self.on_off = True
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 700, 394)
        self.video_widget = QGraphicsVideoItem()
        self.media_player = QMediaPlayer()
        self.scene.addItem(self.video_widget)
        self.video_url = video_url
        self.media_player.setSource(QUrl.fromLocalFile(self.video_url))
        self.media_player.setVideoOutput(self.video_widget)
        self._audio_output = QAudioOutput()  ##
        self.media_player.setAudioOutput(self._audio_output)  ##
        self.graphicsView.setScene(self.scene)

        # 设置视图和视频项的布局选项
        self.graphicsView.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_widget.setSize(QSizeF(self.graphicsView.size()))
        self.btn_play.clicked.connect(self.play_tog)  # play
        self.media_player.positionChanged.connect(self.changeSlide)  # change Slide
        self.sld_video.setTracking(False)
        self.sld_video.sliderReleased.connect(self.releaseSlider)
        self.sld_video.sliderPressed.connect(self.pressSlider)
        self.sld_video.sliderMoved.connect(self.moveSlider)  # 进度条拖拽跳转
        self.media_player.play()

        # 00: 00:00, 01: 49:50, 搅拌车怎么是空的，梯子难缠的，我喜欢这又是什么车？呀
        # 01: 51:20, 03: 11:20, 赛跑开始别撞我憋死我了，

        # out_time_ss = ['00:00:00.000', '00:0:20.000']
        # out_time_to = ['00:01:50.000', '00:02:20.000']
        # out_text = ['搅拌车怎么是空的，梯子难缠的，我喜欢这又是什么车？呀', '赛跑开始别撞我憋死我了']
        self.init_table(out_time_ss, out_time_to, out_text)

    def init_table(self, out_time_ss, out_time_to, out_text):
        row_count = len(out_time_ss)
        self.tableWidget.setRowCount(row_count)  # 设置表格的行数
        # 设置固定行高
        row_height = 50  # 设置行高度为30像素
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHeight(row, row_height)

        row_name = []
        for i in range(row_count):
            row_name.append(str(i + 1))
        self.tableWidget.setVerticalHeaderLabels(row_name)
        line_count = 3
        self.tableWidget.setColumnCount(line_count)  # 设置表格的行数
        line_name = ['时间', '文案', '播放']
        self.tableWidget.setHorizontalHeaderLabels(line_name)
        # 列宽度
        self.tableWidget.setColumnWidth(0, 60)
        self.tableWidget.setColumnWidth(1, 260)
        self.tableWidget.setColumnWidth(2, 40)
        #
        # self.tableWidget.setItem(0, 0, QTableWidgetItem('hihiji'))
        # self.tableWidget.setItem(1, 1, QTableWidgetItem('temp'))
        for i in range(row_count):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(out_time_ss[i][0:-4] + '\n' + out_time_to[i][0:-4]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(out_text[i]))
            self.updateBtn = QtWidgets.QPushButton('跳转')
            self.updateBtn.clicked.connect(lambda: self.updateBtn_func(out_time_ss, out_time_to))
            # self.updateBtn.setStyleSheet('''height : 30px; ''')
            self.tableWidget.setCellWidget(i, 2, self.updateBtn)

    def updateBtn_func(self, out_time_ss, out_time_to):
        button = self.sender()
        if button:
            # 确定位置的时候这里是关键
            row = self.tableWidget.indexAt(button.pos()).row()
            # self.tableWidget.removeRow(row)
            # print(out_time_ss[row], out_time_to[row])
            # print(calculate_time_difference('00:00:00.00',out_time_ss[row]))
            self.media_player.setPosition(calculate_time_difference('00:00:00.00', out_time_ss[row]))

    def closeEvent(self, event):
        if self.on_off:
            self.media_player.pause()
            self.on_off = False
        event.accept()


    def moveSlider(self, position):
        self.sld_video_pressed = True
        if self.media_player.duration() > 0:  # 开始播放后才允许进行跳转
            video_position = int((position / 100) * self.media_player.duration())
            print(video_position)
            self.media_player.setPosition(video_position)
            self.lab_video.setText("%.2f%%" % position)
            self.lab_time.setText(ms_to_hours(position))

    def pressSlider(self):
        self.sld_video_pressed = True

    def releaseSlider(self):
        self.sld_video_pressed = False

    def set_video(self, video_fille):
        self.video_url = video_fille
        self.media_player.setSource(QUrl.fromLocalFile(self.video_url))

    def changeSlide(self, position):
        if not self.sld_video_pressed:  # 进度条被鼠标点击时不更新
            self.vidoeLength = self.media_player.duration() + 0.1
            self.sld_video.setValue(round((position / self.vidoeLength) * 100))
            self.lab_time.setText(ms_to_hours(position))
            self.lab_video.setText("%.2f%%" % ((position / self.vidoeLength) * 100))
            self.lab_time_2.setText(ms_to_hours(self.media_player.duration()))

    def play_tog(self):

        if self.on_off:
            self.media_player.pause()
            self.on_off = False
        else:
            self.media_player.play()
            self.on_off = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 将 excepthook 函数设置为全局异常处理函数
    window = Wenan_dialog()
    window.show()

    sys.exit(app.exec())
