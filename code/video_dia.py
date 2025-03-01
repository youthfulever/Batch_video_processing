import sys
import time

from PyQt6.QtCore import QUrl, Qt, QSizeF, QRectF, pyqtSignal
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QDialogButtonBox, QGraphicsScene, QGraphicsRectItem
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from func_ffprobe import *
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

class video_dialog(QMainWindow):
    close_dialog = pyqtSignal(int,float,float,float,float)
    def __init__(self,video_url='8月8日.mp4'):
        super().__init__()
        self.ui=uic.loadUi("data/ui/video.ui")

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

        self.ui.ok.clicked.connect(self.bt_ok)  # play
        self.ui.cancel.clicked.connect(self.bt_cancel)
        self.ui.btn_play.clicked.connect(self.play_tog)  # play
        self.media_player.positionChanged.connect(self.changeSlide)  # change Slide
        self.ui.sld_video.setTracking(False)
        self.ui.sld_video.sliderReleased.connect(self.releaseSlider)
        self.ui.sld_video.sliderPressed.connect(self.pressSlider)
        self.ui.sld_video.sliderMoved.connect(self.moveSlider)  # 进度条拖拽跳转
        self.media_player.play()

        self.start_flag = 0
        self.start_pos=None
        self.ui.graphicsView.pressValue.connect(self.set_start_pos)
        self.ui.graphicsView.moveValue.connect(self.pic_rect)
        self.ui.graphicsView.releaseValue.connect(self.set_end_pos)
        self.brush_color=QColor("blue")
        self.brush_color.setAlpha(int(255*0.5))
        self.brush = QBrush(self.brush_color)  # 矩形的填充颜色
        rect = QRectF(10, 10, 0, 0)  # 根据左上角点和右下角点计算矩形的位置和大小
        self.rect_item = QGraphicsRectItem(rect)
        # self.rect_item.setFlags(QGraphicsItem.ItemIsMovable)
        # self.rect_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.rect_item.setBrush(self.brush)
        self.scene.addItem(self.rect_item)
        self.flag=0
        self.watermark_x=0
        self.watermark_y=0
        self.watermark_w=0
        self.watermark_h=0
    def close(self):
        if self.flag==1:
            reply = QMessageBox.question(self.ui, '提示框', '你没有确定！是否依然退出',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.ui.close()

    def pic_rect(self,pos):
        if self.start_flag==1:
            try:
                self.scene.removeItem(self.rect_item)
                self.watermark_x=self.start_pos.x()
                self.watermark_y=self.start_pos.y()
                self.watermark_w =pos.x()-self.start_pos.x()
                self.watermark_h = pos.y()-self.start_pos.y()
                rect = QRectF(self.watermark_x,self.watermark_y ,self.watermark_w ,self.watermark_h )  # 根据左上角点和右下角点计算矩形的位置和大小
                self.rect_item = QGraphicsRectItem(rect)
                self.rect_item.setBrush(self.brush)
                # self.rect_item.setFlag(QGraphicsItem.ItemIsSelectable)
                # self.rect_item.setFlag(QGraphicsItem.ItemIsMovable)
                # self.rect_item.setFlag(QGraphicsRectItem.ItemIsSelectable)  # Allow the rectangle to be selected
                # self.rect_item.setFlag(QGraphicsRectItem.ItemIsMovable)  # Allow the rectangle to be moved
                self.scene.addItem(self.rect_item)
                # self.rect_item.setFlag(QGraphicsItem.ItemIsSelectable, True)
                # self.rect_item.setFlag(QGraphicsItem.ItemIsMovable,True)
                self.flag = 1
            except:
                print('绘画错误，往右下画矩形')

    def pos_mappe(self):
        video_w,video_h=get_ratio(self.video_url)
        if video_w / video_h == 16 / 9:
            self.watermark_x = self.watermark_x*video_w/700
            self.watermark_y = self.watermark_y*video_w/700
            self.watermark_w = self.watermark_w*video_w/700
            self.watermark_h = self.watermark_h*video_w/700
        elif video_w / video_h > 16 / 9:
            temp_h=700/video_w*video_h
            self.watermark_x = self.watermark_x * video_w / 700
            self.watermark_y = (self.watermark_y-(394-temp_h)/2) * video_w / 700
            self.watermark_w = self.watermark_w * video_w / 700
            self.watermark_h = self.watermark_h * video_w / 700
        elif video_w / video_h < 16 / 9:
            temp_w = 394 / video_h * video_w
            self.watermark_x = (self.watermark_x-(700-temp_w)/2) * video_h / 394
            self.watermark_y = self.watermark_y * video_h / 394
            self.watermark_w = self.watermark_w * video_h / 394
            self.watermark_h = self.watermark_h * video_h / 394
        return video_w,video_h
    # 设置水印起始点坐标
    def set_start_pos(self,pos):
        self.start_flag=1
        self.start_pos=pos
    def set_end_pos(self,pos):
        self.start_flag = 0
        self.end_pos=pos

    def show(self):
        self.ui.show()


    def bt_cancel(self):
        self.flag=0
        # self.close_dialog.emit('取消前',self.flag, self.watermark_x, self.watermark_y, self.watermark_w, self.watermark_h)
        self.ui.close()

    def bt_ok(self):
        video_w,video_h=self.pos_mappe()
        if self.watermark_x<0 or self.watermark_y<0 or self.watermark_x+self.watermark_w>video_w or self.watermark_y+self.watermark_h>video_h:
            print(self.watermark_x<0,self.watermark_y<0,self.watermark_x+self.watermark_w>video_w,self.watermark_y+self.watermark_h>video_h)
            reply = QMessageBox.question(self.ui, '提示框', '数值无效！',
                                         QMessageBox.StandardButton.Yes)
        else:
            self.watermark_x=round(self.watermark_x,2)
            self.watermark_y=round(self.watermark_y,2)
            self.watermark_w=round(self.watermark_w,2)
            self.watermark_h=round(self.watermark_h,2)
            self.close_dialog.emit(self.flag, self.watermark_x, self.watermark_y, self.watermark_w, self.watermark_h)
            self.ui.close()
            # reply = QMessageBox.question(self.ui, '提示框', '数值无效！',
            #                              QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            # if reply == QMessageBox.StandardButton.Yes:
            #     self.ui.close()

        # self.ui.close()
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
    window=video_dialog()
    window.show()

    sys.exit(app.exec())

