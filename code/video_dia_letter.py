import sys
import time

from PyQt6.QtCore import QUrl, Qt, QSize, QSizeF, QRectF, pyqtSignal, QPointF
from PyQt6.QtGui import QBrush, QColor, QFont, QFontDatabase, QPixmap, QMovie
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QButtonGroup, QLabel, QDialog, QDialogButtonBox, QVBoxLayout, \
    QTextBrowser, QTextEdit, QMessageBox, QFileDialog, QGraphicsScene, QGraphicsRectItem, QGraphicsItem, QGraphicsView, \
    QGraphicsTextItem, QGraphicsPixmapItem, QGraphicsProxyWidget
from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMessageBox
from func_ffprobe import *
from func_timeout import func_set_timeout, FunctionTimedOut
import threading
from func_ffprobe import get_ratio


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


class letter_dialog(QMainWindow):
    letter_dialog_signal = pyqtSignal(str, float, float, float,float)

    def __init__(self, video_url='712.mp4'):
        super().__init__()
        self.ui = uic.loadUi("data/ui/video_letter.ui")

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
        # self._audio_output = QAudioOutput()  ##
        # self.media_player.setAudioOutput(self._audio_output)  ##
        self.ui.graphicsView.setScene(self.scene)

        # 设置视图和视频项的布局选项
        self.ui.graphicsView.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_widget.setSize(QSizeF(self.ui.graphicsView.size()))
        self.ui.ok.clicked.connect(self.bt_ok)  # play
        self.ui.btn_play.clicked.connect(self.play_tog)  # play
        self.media_player.positionChanged.connect(self.changeSlide)  # change Slide
        self.ui.sld_video.setTracking(False)
        self.ui.sld_video.sliderReleased.connect(self.releaseSlider)
        self.ui.sld_video.sliderPressed.connect(self.pressSlider)
        self.ui.sld_video.sliderMoved.connect(self.moveSlider)  # 进度条拖拽跳转
        self.media_player.play()
        # self.media_player.pause()
        self.dialog_type = ''
        self.ratio_w, self.ratio_h = get_ratio(self.video_url)
        self.text_size = 16
        self.ui.pb_larger.clicked.connect(self.set_larger)
        self.ui.pb_smaller.clicked.connect(self.set_smaller)
        self.text_item1 = None
        self.text_item2 = None
        self.text_item3 = None
        self.text_item4 = None
        self.check_item = None
        self.text_item1_flag = 0
        self.text_item2_flag = 0
        self.text_item3_flag = 0
        self.text_item4_flag = 0


        # self.add_Text(text_index='1', mytext='海阔天空')
        # self.add_Text(text_index='2', mytext='BB')
        # self.add_Text(text_index='3', mytext='CC')



    def get_video_paint(self):
        ratio_w, ratio_h = get_ratio(self.video_url)
        if ratio_w / ratio_h == 16 / 9:
            video_w = 700
            video_h = 394
        elif ratio_w / ratio_h > 16 / 9:
            video_w = 700
            video_h = ratio_h / ratio_w * video_w
        elif ratio_w / ratio_h < 16 / 9:
            video_h = 394
            video_w = ratio_w / ratio_h * video_h
        x = (700 - video_w) / 2
        y = (394 - video_h) / 2
        # print(x,y,video_w,video_h)
        return x, y, video_w, video_h

    def clear_item(self):
        if self.text_item1:
            self.scene.removeItem(self.text_item1)
        if self.text_item2:
            self.scene.removeItem(self.text_item2)
        if self.text_item3:
            self.scene.removeItem(self.text_item3)
        if self.text_item4:
            self.scene.removeItem(self.text_item4)

    def add_Text(self, text_index='1', mytext="海阔天空", color='white', font_family='仿宋', font_size='80', pos_x='0',
                 pos_y='0'):
        # 区分添加第几个文本
        setattr(self, f'text_item{text_index}_flag', 1)
        x, y, video_w, video_h = self.get_video_paint()
        self.dialog_type = 'text'
        if text_index == '1':
            self.text_color = QColor(color)
            self.text_item1 = QGraphicsTextItem(mytext)
            self.text_item1.setDefaultTextColor(self.text_color)
            self.text_item1.setPos(QPointF(x, y))
            self.font_family_1 = font_family
            self.text_size_1 = int(float(font_size) / self.ratio_h * 288)
            self.text_item1.setFont(QFont(self.font_family_1, self.text_size_1, weight=QFont.Weight.Bold))
            self.text_item1.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.text_item1.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            self.scene.addItem(self.text_item1)
            self.check_item = self.text_item1
        if text_index == '2':
            self.text_color = QColor(color)
            self.text_item2 = QGraphicsTextItem(mytext)
            self.text_item2.setDefaultTextColor(self.text_color)
            self.text_item2.setPos(QPointF(x, y))
            self.font_family_2 = font_family
            self.text_size_2 = int(float(font_size) / self.ratio_h * 288)
            self.text_item2.setFont(QFont(self.font_family_2, self.text_size_2, weight=QFont.Weight.Bold))
            self.text_item2.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.text_item2.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            self.scene.addItem(self.text_item2)
            self.check_item = self.text_item2
        if text_index == '3':
            self.text_color = QColor(color)
            self.text_item3 = QGraphicsTextItem(mytext)
            self.text_item3.setDefaultTextColor(self.text_color)
            self.text_item3.setPos(QPointF(x, y))
            self.font_family_3 = font_family
            self.text_size_3 = int(float(font_size) / self.ratio_h * 288)
            self.text_item3.setFont(QFont(self.font_family_3, self.text_size_3, weight=QFont.Weight.Bold))
            self.text_item3.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.text_item3.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            self.scene.addItem(self.text_item3)
            self.check_item = self.text_item3
        if text_index == '4':
            self.text_color = QColor(color)
            self.text_item4 = QGraphicsTextItem(mytext)
            self.text_item4.setDefaultTextColor(self.text_color)
            self.text_item4.setPos(QPointF(x, y))
            self.font_family_4 = font_family
            self.text_size_4 = int(float(font_size) / self.ratio_h * 288)
            self.text_item4.setFont(QFont(self.font_family_4, self.text_size_4, weight=QFont.Weight.Bold))
            self.text_item4.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.text_item4.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            self.scene.addItem(self.text_item4)
            self.check_item = self.text_item4

    def set_smaller(self):
        self.check_item = self.scene.selectedItems()[0]
        if self.dialog_type == 'text':
            self.scene.removeItem(self.check_item)
            if self.check_item == self.text_item1:
                self.text_size_1 -= 1
                temp_size = self.text_size_1
                temp_family = self.font_family_1
            if self.check_item == self.text_item2:
                self.text_size_2 -= 1
                temp_size = self.text_size_2
                temp_family = self.font_family_2
            if self.check_item == self.text_item3:
                self.text_size_3 -= 1
                temp_size = self.text_size_3
                temp_family = self.font_family_3
            if self.check_item == self.text_item4:
                self.text_size_4 -= 1
                temp_size = self.text_size_4
                temp_family = self.font_family_4
            self.check_item.setFont(QFont(temp_family, temp_size, weight=QFont.Weight.Bold))
            self.check_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.check_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            self.scene.addItem(self.check_item)

    def set_larger(self):
        self.check_item = self.scene.selectedItems()[0]
        if self.dialog_type == 'text':
            self.scene.removeItem(self.check_item)
            if self.check_item == self.text_item1:
                self.text_size_1 += 1
                temp_size = self.text_size_1
                temp_family = self.font_family_1

            if self.check_item == self.text_item2:
                self.text_size_2 += 1
                temp_size = self.text_size_2
                temp_family = self.font_family_2
            if self.check_item == self.text_item3:
                self.text_size_3 += 1
                temp_size = self.text_size_3
                temp_family = self.font_family_3
            if self.check_item == self.text_item4:
                self.text_size_4 += 1
                temp_size = self.text_size_4
                temp_family = self.font_family_4
            self.check_item.setFont(QFont(temp_family, temp_size, weight=QFont.Weight.Bold))
            # self.check_item.setFont(QFont(self.font_family_1, self.text_size_1, weight=QFont.Weight.Bold))
            self.check_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.check_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            self.scene.addItem(self.check_item)

    def close(self):

        self.ui.close()
        super().close()

    def show(self):
        self.ui.show()

    def bt_ok(self):

        x, y, video_w, video_h = self.get_video_paint()

        def check_temp(a, b):
            return (a - x) < 0 or (b - y) < 0 or (a - x) > video_w or (b - y) > video_h

        if self.dialog_type == 'text':
            if self.text_item1_flag == 1:
                if check_temp(self.text_item1.x(), self.text_item1.pos().y()):
                    reply = QMessageBox.question(self.ui, '提示框', '数值无效！', QMessageBox.StandardButton.Yes)
                else:
                    # print('text1', (self.text_item1.x() - x) / video_w,
                    #       (self.text_item1.pos().y() - y) / video_h,
                    #       self.text_item1.boundingRect().height() / video_h)
                    # print('text1', self.text_item1.x(), x,
                    #       self.text_item1.pos().y() , y,
                    #       self.text_item1.boundingRect().height())
                    self.letter_dialog_signal.emit('text1', (self.text_item1.x() - x) / video_w,
                          (self.text_item1.pos().y() - y) / video_h,
                          self.text_item1.boundingRect().height() / video_h,self.text_item1.boundingRect().width() / video_w)

            if self.text_item2_flag == 1:
                # print(self.text_item2.x(),self.text_item2)
                if check_temp(self.text_item2.x(), self.text_item2.pos().y()):
                    reply = QMessageBox.question(self.ui, '提示框', '数值无效！', QMessageBox.StandardButton.Yes)
                else:
                    self.letter_dialog_signal.emit('text2', (self.text_item2.x() - x) / video_w,
                          (self.text_item2.pos().y() - y) / video_h,
                          self.text_item2.boundingRect().height() / video_h,self.text_item1.boundingRect().width() / video_w)
                    # print(('text2', (self.text_item2.x() - x) / video_w,
                    #       (self.text_item2.pos().y() - y) / video_h,
                    #       self.text_item2.boundingRect().height() / video_h,self.text_item1.boundingRect().width() / video_w))
            if self.text_item3_flag == 1:
                if check_temp(self.text_item3.x(), self.text_item3.pos().y()):
                    reply = QMessageBox.question(self.ui, '提示框', '数值无效！', QMessageBox.StandardButton.Yes)
                else:
                    self.letter_dialog_signal.emit('text3', (self.text_item3.x() - x) / video_w,
                          (self.text_item3.pos().y() - y) / video_h,
                          self.text_item3.boundingRect().height() / video_h,self.text_item1.boundingRect().width() / video_w)
            if self.text_item4_flag == 1:
                if check_temp(self.text_item4.x(), self.text_item4.pos().y()):
                    reply = QMessageBox.question(self.ui, '提示框', '数值无效！', QMessageBox.StandardButton.Yes)
                else:
                    self.letter_dialog_signal.emit('text4', (self.text_item4.x() - x) / video_w,
                          (self.text_item4.pos().y() - y) / video_h,
                          self.text_item4.boundingRect().height() / video_h,self.text_item1.boundingRect().width() / video_w)
            self.close()

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

    def set_video(self, video_fille):
        self.video_url = video_fille
        self.media_player.setSource(QUrl.fromLocalFile(self.video_url))

    def changeSlide(self, position):
        if not self.sld_video_pressed:  # 进度条被鼠标点击时不更新
            self.vidoeLength = self.media_player.duration() + 0.1
            self.ui.sld_video.setValue(round((position / self.vidoeLength) * 100))
            self.ui.lab_time.setText(ms_to_hours(position))
            self.ui.lab_video.setText("%.2f%%" % ((position / self.vidoeLength) * 100))
            self.ui.lab_time_2.setText(ms_to_hours(self.media_player.duration()))

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
    window = letter_dialog("data/pre_video/916.mp4")
    window.show()

    sys.exit(app.exec())
