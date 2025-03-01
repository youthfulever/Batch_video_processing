from PyQt6.QtGui import QBrush, QMouseEvent
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QWidget, QSlider, QGraphicsRectItem, QTextEdit, \
    QGraphicsTextItem
from PyQt6.QtCore import Qt, pyqtSignal, QPoint, QRectF


class CustomGraphicsView(QGraphicsView):
    pressValue = pyqtSignal(QPoint)
    moveValue = pyqtSignal(QPoint)
    releaseValue = pyqtSignal(QPoint)

    def __init__(self, parent=None):
        super(CustomGraphicsView, self).__init__(parent)
        self.start_flag = 0

    def mousePressEvent(self, event):
        self.start_flag = 1
        # 捕获鼠标点击事件
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            self.pressValue.emit(pos)
    def mouseMoveEvent(self, event):
        if self.start_flag ==1:
            pos = event.pos()
            self.moveValue.emit(pos)

    def mouseReleaseEvent(self, event):
        self.start_flag = 0
        # 捕获鼠标点击事件
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            self.releaseValue.emit(pos)

class CustomTextEdit(QTextEdit):
    def write(self, text):
        self.insertPlainText(text)
        self.ensureCursorVisible()


# class myVideoSlider(QSlider):
#     ClickedValue = Signal(int)
#
#     def __init__(self, father):
#         super().__init__(Qt.Horizontal, father)
#
#     def mousePressEvent(self, QMouseEvent):     #单击事件
#         super().mousePressEvent(QMouseEvent)
#         value = QMouseEvent.localPos().x()
#         # self.setValue(int(value)/9)
#         value = round(value/self.width()*self.maximum())  # 根据鼠标点击的位置和slider的长度算出百分比
#         self.ClickedValue.emit(value)
class myVideoSlider(QSlider):
    ClickedValue = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(Qt.Orientation.Horizontal, parent)

    # def mousePressEvent(self, event):
        # super().mousePressEvent(event)
        # value = event.localPos().x()
        # value = round(value / self.width() * self.maximum())  # 根据鼠标点击的位置和slider的长度算出百分比
        # print(value)
        # self.ClickedValue.emit(value)




class letter_scence(QGraphicsScene):
    def __init__(self):
        super().__init__()

    def onSelectionChanged(self):
        selected_items = self.selectedItems()
        if selected_items:
            print("Selected items:", selected_items)
        else:
            print("No items selected.")

