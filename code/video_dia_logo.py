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


class water_dialog(QMainWindow):
    water_dialog_signal = pyqtSignal(str, float, float, float)

    def __init__(self, video_url='712.mp4'):
        super().__init__()
        self.ui = uic.loadUi("data/ui/video_logo.ui")

        self.sld_video_pressed = False  # 判断当前进度条识别否被鼠标点击
        self.on_off = True
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 700, 394)
        self.video_widget = QGraphicsVideoItem()
        self.media_player = QMediaPlayer()
        self.scene.addItem(self.video_widget)
        self.video_url = video_url
        self.media_player.setSource(QUrl.fromLocalFile(self.video_url))
        # self._audio_output = QAudioOutput()  ##
        # self.media_player.setAudioOutput(self._audio_output)  ##
        self.media_player.setVideoOutput(self.video_widget)
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

        self.dialog_type = ''

        self.text_size = 16
        self.ui.pb_larger.clicked.connect(self.set_larger)
        self.ui.pb_smaller.clicked.connect(self.set_smaller)
        self.text_item = None
        self.pixmapitem_gif = None
        self.pixmapitem = None
        self.add_Text()
        # self.get_video_paint()
        # self.add_pic('heng.jpg')
        # self.add_gif()

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
        if self.text_item:
            self.scene.removeItem(self.text_item)
        if self.pixmapitem_gif:
            self.scene.removeItem(self.pixmapitem_gif)
        if self.pixmapitem:
            self.scene.removeItem(self.pixmapitem)

    def add_Text(self, mytext="Hello, world!"):
        x, y, video_w, video_h = self.get_video_paint()
        self.clear_item()
        self.dialog_type = 'text'
        self.text_color = QColor("white")
        self.text_item = QGraphicsTextItem(mytext)
        self.text_item.setDefaultTextColor(self.text_color)
        self.text_item.setPos(QPointF(x, y))
        font_id = QFontDatabase.addApplicationFont("data/font/焦糖下午茶.ttf")
        # Get the font family name from the loaded font
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.text_item.setFont(QFont(self.font_family, 16, weight=QFont.Weight.Bold))
        self.text_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.text_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.scene.addItem(self.text_item)

    def add_gif(self, my_gif="test.gif"):
        x, y, video_w, video_h = self.get_video_paint()
        self.clear_item()
        self.my_gif = my_gif
        self.dialog_type = 'gif'
        self.gif_w, self.gif_h = get_ratio(my_gif)
        self.new_gif_h = 200
        self.new_gif_w = self.new_gif_h * self.gif_w / self.gif_h
        self.size_gif_now = QSize(int(self.new_gif_w), self.new_gif_h)
        self.pixmap_gif = QPixmap(my_gif).scaled(self.size_gif_now, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        self.pixmapitem_gif = self.scene.addPixmap(self.pixmap_gif)
        self.pixmapitem_gif.setPos(x, y)
        self.pixmapitem_gif.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.pixmapitem_gif.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.gif_pos = self.pixmapitem_gif.pos()

    def add_pic(self, my_pic="heng.jpg"):
        x, y, video_w, video_h = self.get_video_paint()
        self.clear_item()
        self.my_pic = my_pic
        self.dialog_type = 'pic'
        self.pic_w, self.pic_h = get_ratio(my_pic)
        self.new_h = 30
        self.new_w = self.new_h * self.pic_w / self.pic_h
        self.size_now = QSize(int(self.new_w), self.new_h)
        self.pixmap = QPixmap(my_pic).scaled(self.size_now, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        self.pixmapitem = self.scene.addPixmap(self.pixmap)
        self.pixmapitem.setPos(x, y)
        self.pixmapitem.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.pixmapitem.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.pic_pos = self.pixmapitem.pos()

    def set_smaller(self):
        if self.dialog_type == 'text':
            self.scene.removeItem(self.text_item)
            self.text_size -= 1
            self.text_item.setFont(QFont(self.font_family, self.text_size, weight=QFont.Weight.Bold))
            self.text_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.text_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            self.scene.addItem(self.text_item)
        if self.dialog_type == 'pic':
            self.pic_pos = self.pixmapitem.pos()
            self.scene.removeItem(self.pixmapitem)
            self.new_h -= 1
            self.new_w = self.new_h * self.pic_w / self.pic_h
            self.size_now = QSize(int(self.new_w), self.new_h)
            self.pixmap = QPixmap(self.my_pic).scaled(self.size_now, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            self.pixmapitem = self.scene.addPixmap(self.pixmap)
            self.pixmapitem.setPos(self.pic_pos)
            self.pixmapitem.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.pixmapitem.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        if self.dialog_type == 'gif':
            self.gif_pos = self.pixmapitem_gif.pos()
            self.scene.removeItem(self.pixmapitem_gif)
            self.new_gif_h -= 5
            self.new_gif_w = self.new_gif_h * self.gif_w / self.gif_h
            self.size_gif_now = QSize(int(self.new_gif_w), self.new_gif_h)
            self.pixmap_gif = QPixmap(self.my_gif).scaled(self.size_gif_now,
                                                          aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            self.pixmapitem_gif = self.scene.addPixmap(self.pixmap_gif)
            self.pixmapitem_gif.setPos(self.gif_pos)
            self.pixmapitem_gif.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.pixmapitem_gif.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)

    def set_larger(self):
        if self.dialog_type == 'text':
            self.scene.removeItem(self.text_item)
            self.text_size += 1
            self.text_item.setFont(QFont(self.font_family, self.text_size, weight=QFont.Weight.Bold))
            self.text_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.text_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            self.scene.addItem(self.text_item)
        if self.dialog_type == 'pic':
            self.pic_pos = self.pixmapitem.pos()
            self.scene.removeItem(self.pixmapitem)
            self.new_h += 1
            self.new_w = self.new_h * self.pic_w / self.pic_h
            self.size_now = QSize(int(self.new_w), self.new_h)
            self.pixmap = QPixmap(self.my_pic).scaled(self.size_now, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            self.pixmapitem = self.scene.addPixmap(self.pixmap)
            self.pixmapitem.setPos(self.pic_pos)
            self.pixmapitem.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.pixmapitem.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        if self.dialog_type == 'gif':
            self.gif_pos = self.pixmapitem_gif.pos()
            self.scene.removeItem(self.pixmapitem_gif)
            self.new_gif_h += 5
            self.new_gif_w = self.new_gif_h * self.gif_w / self.gif_h
            self.size_gif_now = QSize(int(self.new_gif_w), self.new_gif_h)
            self.pixmap_gif = QPixmap(self.my_gif).scaled(self.size_gif_now,
                                                          aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            self.pixmapitem_gif = self.scene.addPixmap(self.pixmap_gif)
            self.pixmapitem_gif.setPos(self.gif_pos)
            self.pixmapitem_gif.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.pixmapitem_gif.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)

    def close(self):
        self.ui.close()

    def show(self):
        self.ui.show()

    def bt_ok(self):
        x, y, video_w, video_h = self.get_video_paint()

        def check_temp(a, b):
            return (a - x) < 0 or (b - y) < 0 or (a - x) > video_w or (b - y) > video_h


        if self.dialog_type == 'text':
            # print(self.text_item.x()/700,self.text_item.pos().y()/394,self.text_item.boundingRect().height()/394)
            if check_temp(self.text_item.x(),self.text_item.pos().y()):
                reply = QMessageBox.question(self.ui, '提示框', '数值无效！', QMessageBox.StandardButton.Yes)
            else:
                self.water_dialog_signal.emit('text', (self.text_item.x() - x) / video_w,
                                              (self.text_item.pos().y() - y+self.text_item.boundingRect().height() *0.2)/ video_h,
                                              self.text_item.boundingRect().height() *0.6/ video_h)
                self.close()
        if self.dialog_type == 'pic':
            # print(self.pixmapitem.x()/700,self.pixmapitem.pos().y()/394,self.new_w,self.new_h)
            if check_temp(self.pixmapitem.x(),self.pixmapitem.pos().y()):
                reply = QMessageBox.question(self.ui, '提示框', '数值无效！', QMessageBox.StandardButton.Yes)
            else:
                self.water_dialog_signal.emit('pic', (self.pixmapitem.x() - x) / video_w, (self.pixmapitem.pos().y() - y) / video_h,
                                          self.new_w / video_w)
                self.close()
        if self.dialog_type == 'gif':

            if check_temp(self.pixmapitem_gif.x(),self.pixmapitem_gif.pos().y()):
                reply = QMessageBox.question(self.ui, '提示框', '数值无效！', QMessageBox.StandardButton.Yes)
            else:
                self.water_dialog_signal.emit('gif', (self.pixmapitem_gif.x() - x) / video_w,
                                              (self.pixmapitem_gif.pos().y() - y) / video_h, self.new_gif_w / video_w)
            # print(('gif',self.pixmapitem_gif.x() / 700, self.pixmapitem_gif.pos().y() / 394, self.new_gif_w/700))
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
    window = water_dialog("712.mp4")
    window.show()

    sys.exit(app.exec())
