from functools import partial
from func_xunfei import my_xunfei
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction,  QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow,QMessageBox, QFileDialog, QTableWidgetItem, QMenu, QColorDialog, QFontDialog
from PyQt6 import uic
import threading
from video_dia import video_dialog
from func_conf import *
from func_video import *
from func_os import *
from video_dia_logo import water_dialog
from video_dia_letter import letter_dialog
from func_ass import get_ass
from video_dia_wenan import Wenan_dialog


class mainwindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("data/ui/main_win.ui")
        self.init_table()
        self.ui.show()
        self.ui.setWindowTitle(u'用线科技视频剪辑')
        self.ui.setWindowIcon(QIcon('data/ui/logoa.png'))
        # 将自定义异常处理函数设置为全局异常处理器
        # # aaa
        sys.excepthook = self.handle_exception
        self.ui.in_video.clicked.connect(self.open_video)
        self.ui.in_file.clicked.connect(self.open_dir)
        self.ui.open_mix_video.clicked.connect(self.open_mix_video_func)
        self.video_list = []
        # 表格右键点击事件
        # self.ui.my_table.cellPressed.connect(self.table_item_right)
        #  右键菜单
        self.ui.my_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.my_table.customContextMenuRequested.connect(self.item_menu_event)

        self.ui.clear_table.clicked.connect(self.clear_list)
        self.ui.choose_file.clicked.connect(self.open_out_dir)
        self.dir_out = './out'
        self.ui.label_out_file.setText(self.dir_out)
        self.video_dialog = None
        self.temp_video_dialog = None
        self.choose_dialog_type = ''
        self.ui.open_video.clicked.connect(lambda: self.open_video_dialog('water'))
        self.ui.open_video_2.clicked.connect(lambda: self.open_video_dialog('crop'))

        self.ui.p_edit.clicked.connect(self.clickButton)
        self.ui.p_ending.clicked.connect(self.clickButton)
        self.ui.p_removal.clicked.connect(self.clickButton)
        self.ui.p_watermark.clicked.connect(self.clickButton)
        self.ui.p_setting.clicked.connect(self.clickButton)
        self.ui.p_mix.clicked.connect(self.clickButton)
        self.ui.p_letter.clicked.connect(self.clickButton)
        self.ui.p_tools.clicked.connect(self.clickButton)
        self.cur_button = self.ui.p_edit
        self.cur_button.setStyleSheet("QPushButton {background: #00aaff;}")

        self.ui.choose_color.clicked.connect(self.choose_color)

        self.edit_color = ''

        # self.ui.pb_preview.clicked.connect(lambda: threading.Thread(target=self.preview_fun()).start())  #lambda: threading.Thread(target=self.preview_fun()).start()使用lamda  带括号
        self.ui.pb_preview.clicked.connect(lambda: threading.Thread(
            target=self.preview_fun).start())  # lambda: threading.Thread(target=self.preview_fun()).start()使用lamda  带括号
        self.cur_conf = read_conf('data/conf/temp.toml')
        self.video_w = 0
        self.video_h = 0
        self.is_interrupted = True
        # self.ui.start_p.clicked.connect(threading.Thread(target=self.start_p_func).start())
        self.ui.start_p.clicked.connect(lambda: threading.Thread(target=self.start_p_func).start())
        self.ui.stop_p.clicked.connect(lambda: threading.Thread(target=self.stop_p_func()).start())
        self.ui.opendir_p.clicked.connect(lambda: threading.Thread(target=self.opendir_p_func()).start())

        # 去重 stack page
        self.cube_list = []
        self.init_repeate()
        self.ui.repeate_pre.clicked.connect(lambda: threading.Thread(target=self.preview_repeate).start())
        self.ui.pb_pic_mask.clicked.connect(self.choose_mask_pic)
        # 日志重输出
        # aaa
        sys.stdout = self.ui.textEdit

        self.current_pre_video = ''
        # 后期
        self.ui.pb_preview_ending.clicked.connect(lambda: threading.Thread(target=self.preview_ending).start())
        self.ui.choose_color_ending.clicked.connect(self.choose_color_ending)
        self.ui.pb_padding_pic.clicked.connect(self.choose_padding_pic)
        self.ui.pb_bg_audio.clicked.connect(self.choose_bg_audio)
        self.ui.pb_video_start_file.clicked.connect(self.choose_video_start)
        self.ui.pb_video_end_file.clicked.connect(self.choose_video_end)

        # conf 配置
        self.ui.use_1.clicked.connect(self.use_conf)
        self.ui.use_2.clicked.connect(self.use_conf)
        self.ui.use_3.clicked.connect(self.use_conf)
        self.ui.use_4.clicked.connect(self.use_conf)
        self.ui.use_5.clicked.connect(self.use_conf)
        self.ui.save_1.clicked.connect(self.save_conf)
        self.ui.save_2.clicked.connect(self.save_conf)
        self.ui.save_3.clicked.connect(self.save_conf)
        self.ui.save_4.clicked.connect(self.save_conf)
        self.ui.save_5.clicked.connect(self.save_conf)
        self.init_conf()
        # 配置重命名
        self.ui.lineEdit_name1.editingFinished.connect(self.rename_conf)
        self.ui.lineEdit_name2.editingFinished.connect(self.rename_conf)
        self.ui.lineEdit_name3.editingFinished.connect(self.rename_conf)
        self.ui.lineEdit_name4.editingFinished.connect(self.rename_conf)
        self.ui.lineEdit_name5.editingFinished.connect(self.rename_conf)
        #  自定义配置
        self.ui.use_myconf.clicked.connect(self.open_my_conf)
        self.ui.save_myconf.clicked.connect(self.save_my_conf)
        self.ui.share_myconf.clicked.connect(self.share_my_conf)

        # 水印 stack
        self.water_dialog = None
        self.water_pic = ''
        self.water_gif = ''
        self.ui.pushButton_water_text.clicked.connect(self.water_dialog_show)
        self.ui.pushButton_water_pic.clicked.connect(self.water_dialog_show)
        self.ui.pushButton_water_gif.clicked.connect(self.water_dialog_show)

        self.ui.pb_choose_pic.clicked.connect(self.choose_water_pic)
        self.ui.pb_choose_gif.clicked.connect(self.choose_water_gif)
        self.ui.pb_preview_water.clicked.connect(lambda: threading.Thread(target=self.preview_water).start())

        #     更改gpu加速
        self.ui.gpu_flag.currentTextChanged.connect(self.gpu_changed)
        # 混剪mix
        self.ui.pb_pic_add.clicked.connect(self.choose_mix_pic)
        self.ui.pb_pic_clear.clicked.connect(self.clear_mix_pic)
        self.mix_pic_list = []
        self.ui.start_p_mix.clicked.connect(lambda: threading.Thread(target=self.start_mix).start())

        # 文字
        self.ui.choose_color_l1.clicked.connect(self.letter_color_func)
        self.ui.choose_color_l2.clicked.connect(self.letter_color_func)
        self.ui.choose_color_l3.clicked.connect(self.letter_color_func)
        self.ui.choose_color_l4.clicked.connect(self.letter_color_func)
        self.letter_color_1 = 'white'
        self.letter_color_2 = 'white'
        self.letter_color_3 = 'white'
        self.letter_color_4 = 'white'
        self.ui.choose_font1.clicked.connect(self.letter_font_func)
        self.ui.choose_font2.clicked.connect(self.letter_font_func)
        self.ui.choose_font3.clicked.connect(self.letter_font_func)
        self.ui.choose_font4.clicked.connect(self.letter_font_func)
        self.letter_font_1 = '仿宋'
        self.letter_font_2 = '仿宋'
        self.letter_font_3 = '仿宋'
        self.letter_font_4 = '仿宋'
        self.letter_dia = None

        self.pos_x_1 = 0.5
        self.pos_y_1 = 0.5
        self.font_size_1 = 0.1
        self.pos_x_2 = 0.5
        self.pos_y_2 = 0.5
        self.font_size_2 = 0.1
        self.pos_x_3 = 0.5
        self.pos_y_3 = 0.5
        self.font_size_3 = 0.1
        self.pos_x_4 = 0.5
        self.pos_y_4 = 0.5
        self.font_size_4 = 0.1
        self.ui.choose_pos_size.clicked.connect(self.pos_size_func)
        self.ui.pb_preview_letter.clicked.connect(lambda: threading.Thread(target=self.preview_letter).start())

        # 工具
        self.ui.pb_videotogif_file.clicked.connect(self.pb_videotogif_file_func)
        self.ui.pb_videotogif_out.clicked.connect(self.pb_videotogif_out_fun)
        self.videotogif_file = ''
        self.ui.pb_videotogif_pre.clicked.connect(lambda: threading.Thread(target=self.pb_videotogif_pre_func).start())
        self.ui.pb_videotogif_change.clicked.connect(
            lambda: threading.Thread(target=self.pb_videotogif_change_func).start())

        self.ui.pb_videotomp3.clicked.connect(lambda: threading.Thread(target=self.pb_videotomp3_func).start())
        self.ui.pb_videotomp3_out.clicked.connect(self.pb_videotomp3_out_func)

        self.ui.pb_videototext.clicked.connect(lambda: threading.Thread(target=self.pb_videototext_func).start())
        self.ui.pb_videototext_out.clicked.connect(self.pb_videototext_out_func)
        self.ui.pb_videototext_pre.clicked.connect(
            lambda: threading.Thread(target=self.pb_videototext_pre_func()).start())
        self.out_time_ss = []


    #     self.input_file = "712.mp4"
    #     self.current_time = 0
    #     self.ffplay_process = subprocess.Popen(["ffplay", self.input_file, "-ss", str(self.current_time)],
    #                                            stdin=subprocess.PIPE)
    #     self.ui.ttt.clicked.connect(self.tt_func)
    #
    # def tt_func(self):
    #     self.current_time += 10
    #     self.ffplay_process.stdin.write(f"seek {self.current_time} 2\n".encode())
    #     self.ffplay_process.stdin.flush()

    def opendir_p_func(self):
        video_file, _ = QFileDialog.getOpenFileNames(None, "打开", self.dir_out,
                                                     "全部文件(*.*)")

    def pb_videototext_pre_func(self):
        # self.videotogif_file="C:\\Users\\83853\\Desktop\\py_proj\\ocr\\712.mp4"
        # self.out_time_ss = ['00:00:00.000', '00:00:06.670', '00:00:18.430']
        # self.out_time_to = ['00:00:06.650', '00:00:18.410', '00:00:20.160']
        # self.out_text = ['全球最美的女部长是谁？蒙古国的现代孝庄阿特策策格一定免不了被提名。',
        #                  '在不久前举行的首次女性外长会晤上，巴特斯特格大放异彩，为全球瞩目。这位蒙古国外交部女部长一如法国媒体所褒奖的精通三门语言，富有东方风韵，',
        #                  '秀美而不失英气，']

        if self.out_time_ss == []:
            print('请先提取文案！')
        else:
            self.wenan_dialog = Wenan_dialog(self.videotogif_file, self.out_time_ss, self.out_time_to, self.out_text)
            self.wenan_dialog.show()





    def pb_videototext_func(self):
        if self.videotogif_file == '':
            print('请选定视频/音频文件')
        else:

            videotogif_file = self.videotogif_file
            temp_name = os.path.basename(self.videotogif_file)
            base_name, extension = os.path.splitext(temp_name)

            if extension not in ['wav', 'mp3']:
                print("提取音频中——")
                videotomp3(self.videotogif_file, './temp/temp.wav')
                videotogif_file = './temp/temp.wav'

            txt_name = self.dir_out + '/' + base_name + '.txt'
            print('开始提取文案——')
            try:
                self.out_time_ss, self.out_time_to, self.out_text = my_xunfei(videotogif_file, txt_name)
            except:
                print("提取文案失败！")

    def pb_videototext_out_func(self):
        video_file, _ = QFileDialog.getOpenFileNames(None, "打开", self.dir_out,
                                                     "文本文件(*.txt)")

    def pb_videotomp3_out_func(self):
        video_file, _ = QFileDialog.getOpenFileNames(None, "打开", self.dir_out,
                                                     "音频文件(*.mp3)")

    def pb_videotomp3_func(self):
        if self.videotogif_file == '':
            print('请选定视频文件')
        else:
            temp_name = os.path.basename(self.videotogif_file)
            base_name, extension = os.path.splitext(temp_name)
            mp3_name = self.dir_out + '/' + base_name + '.mp3'
            print('转换中——')
            videotomp3(self.videotogif_file, mp3_name)
            print('提取音频成功')

    def pb_videotogif_out_fun(self):
        video_file, _ = QFileDialog.getOpenFileNames(None, "打开", self.dir_out,
                                                     "动图文件(*.gif)")

    def pb_videotogif_pre_func(self):
        ss = self.ui.lineEdit_videotogif_ss.text()
        to = self.ui.lineEdit_videotogif_to.text()
        if ss == '' or to == '':
            print('请输入生成动图时间')
        elif self.videotogif_file == '':
            print('请选定视频文件')
        else:
            print('生成预览中——')
            videotogif(self.videotogif_file, 'temp/temp.gif', ss, to)
            pre_gif('temp/temp.gif')

    def pb_videotogif_change_func(self):
        ss = self.ui.lineEdit_videotogif_ss.text()
        to = self.ui.lineEdit_videotogif_to.text()
        # new_name=get_new_extension(os.path.basename(self.videotogif_file), '.gif')
        # gif_name=get_unique_filename(self.dir_out+'/'+new_name)

        if ss == '' or to == '':
            print('请输入生成动图时间')
        elif self.videotogif_file == '':
            print('请选定视频文件')
        else:
            temp_name = os.path.basename(self.videotogif_file)
            base_name, extension = os.path.splitext(temp_name)
            gif_name = self.dir_out + '/' + base_name + '_' + ss + '_' + to + '.gif'
            print('转换中——')
            videotogif(self.videotogif_file, gif_name, ss, to)
            print('转换动图成功')

    def pb_videotogif_file_func(self):
        video_file, _ = QFileDialog.getOpenFileName(None, "打开", "./",
                                                    "自定义文件(*.mp4 *.avi *.mkv *.mov *.flv *.mpeg *.mp3 *.wav)")
        if not video_file:
            print("用户未选择文件")
        else:
            # print("选择的文件:", pic_file)
            self.videotogif_file = video_file
            file_name = os.path.basename(video_file)
            self.ui.label_videotogif.setText(file_name)

    def preview_letter(self):
        if self.ui.comboBox_ending_ration.currentIndex() == 0:
            self.video_temp_letter = 'data/pre_video/169.mp4'
            temp_w = 1920
            temp_h = 1080
        if self.ui.comboBox_ending_ration.currentIndex() == 1:
            self.video_temp_letter = 'data/pre_video/916.mp4'
            temp_w = 1080
            temp_h = 1920
        self.ass_list = []
        if self.ui.checkBox_letter1.isChecked():
            self.lineEdit_letter1 = '文本1未选定文字' if self.ui.lineEdit_letter1.text() == '' else self.ui.lineEdit_letter1.text()
            save_ass(ass_content=get_ass(text=self.lineEdit_letter1, font_name=self.ui.lineEdit_font1.text(),
                                         ass_type=self.ui.comboBox_in_form1.currentText(),
                                         font_color=self.ui.lineEdit_color_l1.text(),
                                         font_size=self.font_size_1 * temp_h * 0.7,
                                         posx=(self.pos_x_1 + self.ratio_w_1 / 2) * temp_w,
                                         posy=(self.pos_y_1 + self.font_size_1 / 2) * temp_h, long_time=5,
                                         ratio_w=temp_w, ratio_h=temp_h), output_file_path='data/ass/temp1.ass')
            self.ass_list.append('data/ass/temp1.ass')

        if self.ui.checkBox_letter2.isChecked():
            self.lineEdit_letter2 = '文本2未选定文字' if self.ui.lineEdit_letter2.text() == '' else self.ui.lineEdit_letter2.text()
            save_ass(ass_content=get_ass(text=self.lineEdit_letter2, font_name=self.ui.lineEdit_font2.text(),
                                         ass_type=self.ui.comboBox_in_form2.currentText(),
                                         font_color=self.ui.lineEdit_color_l2.text(),
                                         font_size=self.font_size_2 * temp_h * 0.7,
                                         posx=(self.pos_x_2 + self.ratio_w_2 / 2) * temp_w,
                                         posy=(self.pos_y_2 + self.font_size_2 / 2) * temp_h, long_time=5,
                                         ratio_w=temp_w, ratio_h=temp_h),
                     output_file_path='data/ass/temp2.ass')
            self.ass_list.append('data/ass/temp2.ass')
        if self.ui.checkBox_letter3.isChecked():
            self.lineEdit_letter3 = '文本3未选定文字' if self.ui.lineEdit_letter3.text() == '' else self.ui.lineEdit_letter3.text()
            save_ass(ass_content=get_ass(text=self.lineEdit_letter3, font_name=self.ui.lineEdit_font3.text(),
                                         ass_type=self.ui.comboBox_in_form3.currentText(),
                                         font_color=self.ui.lineEdit_color_l3.text(),
                                         font_size=self.font_size_3 * temp_h * 0.7,
                                         posx=(self.pos_x_3 + self.ratio_w_3 / 2) * temp_w,
                                         posy=(self.pos_y_3 + self.font_size_3 / 2) * temp_h, long_time=5,
                                         ratio_w=temp_w, ratio_h=temp_h),
                     output_file_path='data/ass/temp3.ass')
            self.ass_list.append('data/ass/temp3.ass')
        if self.ui.checkBox_letter4.isChecked():
            self.lineEdit_letter4 = '文本4未选定文字' if self.ui.lineEdit_letter4.text() == '' else self.ui.lineEdit_letter4.text()
            save_ass(ass_content=get_ass(text=self.lineEdit_letter4, font_name=self.ui.lineEdit_font4.text(),
                                         ass_type=self.ui.comboBox_in_form4.currentText(),
                                         font_color=self.ui.lineEdit_color_l4.text(),
                                         font_size=self.font_size_4 * temp_h * 0.7,
                                         posx=(self.pos_x_4 + self.ratio_w_4 / 2) * temp_w,
                                         posy=(self.pos_y_4 + self.font_size_4 / 2) * temp_h, long_time=5,
                                         ratio_w=temp_w, ratio_h=temp_h),
                     output_file_path='data/ass/temp4.ass')
            self.ass_list.append('data/ass/temp4.ass')
        video_merge_ass(video=self.video_temp_letter, ass_list=self.ass_list, out_video='temp/pre.mp4')
        pre_video('temp/pre.mp4')

    def pos_size_func(self):
        if self.ui.comboBox_ending_ration.currentIndex() == 0:
            self.video_temp_letter = 'data/pre_video/169.mp4'
        if self.ui.comboBox_ending_ration.currentIndex() == 1:
            self.video_temp_letter = 'data/pre_video/916.mp4'
        self.letter_dia = letter_dialog(self.video_temp_letter)
        self.letter_dia.letter_dialog_signal.connect(self.letter_dialog_signal_fun)
        self.letter_dia.show()
        if self.ui.checkBox_letter1.isChecked():
            self.lineEdit_letter1 = '文本1未选定文字' if self.ui.lineEdit_letter1.text() == '' else self.ui.lineEdit_letter1.text()
            self.letter_dia.add_Text(text_index='1', mytext=self.lineEdit_letter1,
                                     color=self.ui.lineEdit_color_l1.text(), font_family=self.ui.lineEdit_font1.text())
        if self.ui.checkBox_letter2.isChecked():
            self.lineEdit_letter2 = '文本2未选定文字' if self.ui.lineEdit_letter2.text() == '' else self.ui.lineEdit_letter2.text()
            self.letter_dia.add_Text(text_index='2', mytext=self.lineEdit_letter2,
                                     color=self.ui.lineEdit_color_l2.text(), font_family=self.ui.lineEdit_font2.text())

        if self.ui.checkBox_letter3.isChecked():
            self.lineEdit_letter3 = '文本3未选定文字' if self.ui.lineEdit_letter3.text() == '' else self.ui.lineEdit_letter3.text()
            self.letter_dia.add_Text(text_index='3', mytext=self.lineEdit_letter3,
                                     color=self.ui.lineEdit_color_l3.text(), font_family=self.ui.lineEdit_font3.text())
        if self.ui.checkBox_letter4.isChecked():
            self.lineEdit_letter4 = '文本4未选定文字' if self.ui.lineEdit_letter4.text() == '' else self.ui.lineEdit_letter4.text()
            self.letter_dia.add_Text(text_index='4', mytext=self.lineEdit_letter4,
                                     color=self.ui.lineEdit_color_l4.text(), font_family=self.ui.lineEdit_font4.text())

    def letter_dialog_signal_fun(self, flag, x, y, size, ratio_w):
        # print(self, flag, x, y, size)
        if flag == 'text1':
            self.pos_x_1 = x
            self.pos_y_1 = y
            self.font_size_1 = size
            self.ratio_w_1 = ratio_w
        if flag == 'text2':
            self.pos_x_2 = x
            self.pos_y_2 = y
            self.font_size_2 = size
            self.ratio_w_2 = ratio_w
        if flag == 'text3':
            self.pos_x_3 = x
            self.pos_y_3 = y
            self.font_size_3 = size
            self.ratio_w_3 = ratio_w
        if flag == 'text4':
            self.pos_x_4 = x
            self.pos_y_4 = y
            self.font_size_4 = size
            self.ratio_w_4 = ratio_w

    def letter_color_func(self):
        color = QColorDialog.getColor().name()
        if self.sender() == self.ui.choose_color_l1:
            self.letter_color_1 = color
            self.ui.lineEdit_color_l1.setText(color)
        if self.sender() == self.ui.choose_color_l2:
            self.letter_color_2 = color
            self.ui.lineEdit_color_l2.setText(color)
        if self.sender() == self.ui.choose_color_l3:
            self.letter_color_3 = color
            self.ui.lineEdit_color_l3.setText(color)
        if self.sender() == self.ui.choose_color_l4:
            self.letter_color_4 = color
            self.ui.lineEdit_color_l4.setText(color)

    def letter_font_func(self):
        font, ok = QFontDialog.getFont()
        if ok:
            # print(font.family())
            if self.sender() == self.ui.choose_font1:
                self.letter_font_1 = font.family()
                self.ui.lineEdit_font1.setText(font.family())
            if self.sender() == self.ui.choose_font2:
                self.letter_font_2 = font.family()
                self.ui.lineEdit_font2.setText(font.family())
            if self.sender() == self.ui.choose_font3:
                self.letter_font_3 = font.family()
                self.ui.lineEdit_font3.setText(font.family())
            if self.sender() == self.ui.choose_font4:
                self.letter_font_4 = font.family()
                self.ui.lineEdit_font4.setText(font.family())

    def choose_mix_pic(self):
        pic_file, _ = QFileDialog.getOpenFileNames(None, "打开", "./",
                                                   "图片文件(*.png *.jpg *.jpeg *.bmp *.gif *.tiff)")
        if not pic_file:
            print("用户未选择文件")
        else:
            # print("选择的文件:", pic_file)
            self.mix_pic_list.extend(pic_file)

        self.ui.mix_pic_table.setRowCount(len(self.mix_pic_list))  # 设置表格的行数
        for index, video_item in enumerate(self.mix_pic_list):
            file_name = os.path.basename(video_item)
            self.ui.mix_pic_table.setItem(index, 0, QTableWidgetItem(file_name))

    def clear_mix_pic(self):
        for index, video_item in enumerate(self.mix_pic_list):
            self.ui.mix_pic_table.setItem(index, 0, QTableWidgetItem(''))
        self.mix_pic_list=[]

        # for i in self.mix_pic_list:
        #     file_name = os.path.basename(i)
        #     self.ui.label_water_pic.setText(file_name)

    def start_mix(self):
        # print(self.video_list)
        temp_list = []
        temp_list.extend(self.video_list)
        temp_ratio_pic = '16/9'
        if self.ui.checkBox_mix_pic.isChecked():
            temp_list.extend(self.mix_pic_list)
            if self.ui.comboBox_mix_pic.currentIndex() == 0:
                temp_ratio_pic = '16/9'
            if self.ui.comboBox_mix_pic.currentIndex() == 1:
                temp_ratio_pic = '9/16'

        temp_ratio_w = '1920'
        temp_ratio_h = '1080'
        if self.ui.checkBox_mix_ration.isChecked():

            if self.ui.comboBox_mix_ration.currentIndex() == 0:
                temp_ratio_w = '1920'
                temp_ratio_h = '1080'
            elif self.ui.comboBox_mix_ration.currentIndex() == 1:
                temp_ratio_w = '1080'
                temp_ratio_h = '1920'

        temp_min_time = float(self.ui.lineEdit_mix_min.text())
        temp_max_time = float(self.ui.lineEdit_mix_max.text())

        temp_out_time = float(self.ui.lineEdit_mix_outtime.text())
        if self.ui.mix_trans_time.isChecked():
            temp_trans_time = self.ui.lineEdit_mix_trans.text()
        else:
            temp_trans_time = '0'
        if self.ui.mix_audio_able.isChecked():
            temp_audio_able = '0'
        else:
            temp_audio_able = '1'

        out_video_count = int(self.ui.lineEdit_mix_count.text())
        print("开始混剪！")
        # print('all_balls=',temp_list, 'pic_ratio=',temp_ratio_pic, 'ratio_w=',temp_ratio_w, 'ratio_h=',temp_ratio_h,
        #               'video_long_time=',temp_out_time, 'video_min_time=',temp_min_time,
        #               'video_max_time=',temp_max_time,'transitions_value=',temp_trans_time,'audio_able=',temp_audio_able,'out_count=',out_video_count)
        try:
            mix_video_api(all_balls=temp_list, pic_ratio=temp_ratio_pic, ratio_w=temp_ratio_w, ratio_h=temp_ratio_h,
                          video_long_time=temp_out_time, video_min_time=temp_min_time,
                          video_max_time=temp_max_time, transitions_value=temp_trans_time, audio_able=temp_audio_able,
                          out_count=out_video_count)
            print('混剪完成！')
        except:
            print('混剪过程异常')

    def gpu_changed(self):
        # print(self.ui.gpu_flag.currentIndex(),type(self.ui.gpu_flag.currentIndex()))
        change_gpu(self.ui.gpu_flag.currentIndex())
        print('切换成功')

    def init_conf(self):
        self.temp_conf_1 = read_conf('data/conf/conf1.toml')
        self.temp_conf_2 = read_conf('data/conf/conf2.toml')
        self.temp_conf_3 = read_conf('data/conf/conf3.toml')
        self.temp_conf_4 = read_conf('data/conf/conf4.toml')
        self.temp_conf_5 = read_conf('data/conf/conf5.toml')
        self.ui.lineEdit_name1.setText(self.temp_conf_1["alias"]["name"])
        self.ui.lineEdit_name2.setText(self.temp_conf_2["alias"]["name"])
        self.ui.lineEdit_name3.setText(self.temp_conf_3["alias"]["name"])
        self.ui.lineEdit_name4.setText(self.temp_conf_4["alias"]["name"])
        self.ui.lineEdit_name5.setText(self.temp_conf_5["alias"]["name"])

    def choose_water_pic(self):
        pic_file, _ = QFileDialog.getOpenFileName(None, "打开", "./", "图片文件(*.png *.jpg *.jpeg *.bmp *.gif *.tiff)")
        if not pic_file:
            print("用户未选择文件")
        else:
            # print("选择的文件:", conf_file)
            file_name = os.path.basename(pic_file)
            self.ui.label_water_pic.setText(file_name)
            self.water_pic = pic_file

    def choose_water_gif(self):
        pic_file, _ = QFileDialog.getOpenFileName(None, "打开", "./data/pic",
                                                  "图片文件(*.png *.jpg *.jpeg *.bmp *.gif *.tiff)")
        if not pic_file:
            print("用户未选择文件")
        else:
            # print("选择的文件:", conf_file)
            file_name = os.path.basename(pic_file)
            self.ui.label_water_gif.setText(file_name)
            self.water_gif = pic_file

    def water_dialog_show(self):
        if len(self.video_list) == 0:
            print("请选择视频")
        else:
            self.water_dialog = water_dialog(self.current_pre_video)
            self.water_dialog.water_dialog_signal.connect(self.water_dialog_signal)
            self.water_dialog.show()
            if self.sender() == self.ui.pushButton_water_text:
                text_temp = self.ui.lineEdit_water_text.text()
                text_temp = '测试文字水印' if text_temp == '' else text_temp
                self.water_dialog.add_Text(text_temp)
            if self.sender() == self.ui.pushButton_water_pic:
                if self.water_pic != '':
                    self.water_dialog.add_pic(self.water_pic)
                else:
                    print("请先导入图片")
            if self.sender() == self.ui.pushButton_water_gif:
                if self.water_gif != '':
                    self.water_dialog.add_gif(self.water_gif)
                else:
                    print("请先导入贴纸")

    def open_my_conf(self):
        conf_file, _ = QFileDialog.getOpenFileName(None, "打开", "./data/conf", "配置文件(*.toml)")
        if not conf_file:
            print("用户未确定保存文件名")
        else:
            self.cur_conf = read_conf(conf_file)
            base_name = os.path.basename(conf_file)
            self.ui.label_current_conf.setText(f'当前配置：配置{base_name}')
            print(f'配置{base_name}加载成功')

    def save_my_conf(self):
        conf_file, _ = QFileDialog.getSaveFileName(None, "保存配置文件", "./data/conf", "配置文件(*.toml)")
        if not conf_file:
            print("用户未选择文件")
        else:
            save_conf(self.cur_conf, conf_file)
            base_name = os.path.basename(conf_file)
            print(f'配置{base_name}保存成功')

    def share_my_conf(self):
        conf_file, _ = QFileDialog.getSaveFileName(None, "打开", "./data/conf", "配置文件(*.toml)")

    def use_conf(self):
        conf_file = f'data/conf/conf{self.sender().text()[-1]}.toml'
        self.cur_conf = read_conf(conf_file)
        base_name = os.path.basename(conf_file)
        self.ui.label_current_conf.setText(f'当前配置：配置{self.sender().text()[-1]}')
        self.get_conf_ui()
        print(f'配置{base_name}加载成功')

    def get_conf_ui(self):
        # print("更新ui")
        # edit
        if self.cur_conf['edit']['accurate_cut_flag'] == '1':
            self.ui.checkBox_accurate_cut.setChecked(True)
        else:
            self.ui.checkBox_accurate_cut.setChecked(False)
        if self.cur_conf['edit']['start_cut_flag'] == '1':
            self.ui.checkBox_start.setChecked(True)
            self.ui.lineEdit_start.setText(self.cur_conf['edit']['start_cut_time'])
        else:
            self.ui.checkBox_start.setChecked(False)

        if self.cur_conf['edit']['end_cut_flag'] == '1':
            self.ui.checkBox_end.setChecked(True)
            self.ui.lineEdit_end.setText(self.cur_conf['edit']['end_cut_time'])
        else:
            self.ui.checkBox_end.setChecked(False)

        if self.cur_conf['edit']['end_cut_time_1'] != '0':
            self.ui.checkBox_cut.setChecked(True)
            self.ui.lineEdit_cut_end.setText(self.cur_conf['edit']['end_cut_time_1'])
        else:
            self.ui.checkBox_cut.setChecked(False)

        if self.cur_conf['edit']['delogo_flag'] == '1':
            self.ui.checkBox_water.setChecked(True)
            self.ui.lineEdit_water_x.setText(self.cur_conf['edit']['delog_x'])
            self.ui.lineEdit_water_y.setText(self.cur_conf['edit']['delog_y'])
            self.ui.lineEdit_water_w.setText(self.cur_conf['edit']['delog_w'])
            self.ui.lineEdit_water_h.setText(self.cur_conf['edit']['delog_h'])
        else:
            self.ui.checkBox_water.setChecked(False)

        if self.cur_conf['edit']['crop_flag'] == '1':
            self.ui.checkBox_crop.setChecked(True)
            self.ui.lineEdit_crop_left.setText(self.cur_conf['edit']['crop_x'])
            self.ui.lineEdit_crop_top.setText(self.cur_conf['edit']['crop_y'])
            self.ui.lineEdit_crop_right.setText(str(self.video_w - float(self.cur_conf['edit']['crop_w'])))
            self.ui.lineEdit_crop_buttom.setText(str(self.video_h - float(self.cur_conf['edit']['crop_h'])))
        else:
            self.ui.checkBox_crop.setChecked(False)

        if self.cur_conf['edit']['ration_flag'] == '1':
            self.ui.checkBox_ratio.setChecked(True)
            self.ui.lineEdit_ratio_w.setText(self.cur_conf['edit']['ratio_w'])
            self.ui.lineEdit_ratio_h.setText(self.cur_conf['edit']['ratio_h'])
            if self.cur_conf['edit']['padding_color'] != '':
                self.ui.checkBox_color.setChecked(True)
                self.ui.lineEdit_color.setText(self.cur_conf['edit']['padding_color'])
            else:
                self.ui.checkBox_color.setChecked(False)
        else:
            self.ui.checkBox_ratio.setChecked(False)
            self.ui.checkBox_color.setChecked(False)

        # 消重
        if self.cur_conf['repeate']['cut_fps'] != '':
            self.ui.checkBox_cut_fps.setChecked(True)
            self.ui.lineEdit_cut_fps.setText(self.cur_conf['repeate']['cut_fps'])
        else:
            self.ui.checkBox_cut_fps.setChecked(False)

        if self.cur_conf['repeate']['fps'] != '':
            self.ui.checkBox_fps.setChecked(True)
            self.ui.lineEdit_fps.setText(self.cur_conf['repeate']['fps'])
        else:
            self.ui.checkBox_fps.setChecked(False)
        self.ui.checkBox_multiplay.setChecked(True)
        self.ui.lineEdit_multiplay.setText(str(self.cur_conf['repeate']['multi_play_value']))

        if self.cur_conf['repeate']['mata_flag'] == '1':
            self.ui.checkBox_mate.setChecked(True)
            self.ui.lineEdit_title.setText(self.cur_conf['repeate']['title'])
            self.ui.lineEdit_des.setText(self.cur_conf['repeate']['description'])
            self.ui.lineEdit_author.setText(self.cur_conf['repeate']['author'])
            self.ui.lineEdit_copyright.setText(self.cur_conf['repeate']['copyright'])
        else:
            self.ui.checkBox_mate.setChecked(False)

        if self.cur_conf['repeate']['cube_flag'] == '1':
            self.ui.checkBox_filter.setChecked(True)
            self.ui.comboBox_filter.setCurrentIndex(self.cube_list.index(self.cur_conf['repeate']['cube_value'][9:]))
        else:
            self.ui.checkBox_filter.setChecked(False)
        if self.cur_conf['repeate']['mask_flag'] == '1':
            self.ui.checkBox_mask.setChecked(True)
            self.ui.lineEdit_trans.setText(self.cur_conf['repeate']['mask_trans'])
            file_name = os.path.basename(self.cur_conf['repeate']['mask_pic_url'])
            self.ui.label_pic_mask.setText(file_name)

        else:
            self.ui.checkBox_mask.setChecked(False)

        if self.cur_conf['repeate']['gamma'] == '1' and self.cur_conf['repeate']['brightness'] == '0' and \
                self.cur_conf['repeate']['contrast'] == '1' and self.cur_conf['repeate']['saturation'] == '1':
            self.ui.checkBox_color_video.setChecked(False)
        else:
            self.ui.checkBox_color_video.setChecked(True)
            self.ui.lineEdit_gamma.setText(self.cur_conf['repeate']['gamma'])
            self.ui.lineEdit_brightness.setText(self.cur_conf['repeate']['brightness'])
            self.ui.lineEdit_contrast.setText(self.cur_conf['repeate']['contrast'])
            self.ui.lineEdit_saturation.setText(self.cur_conf['repeate']['saturation'])

        #     水印
        if self.cur_conf['watermark']['text_flag'] == '1':
            self.ui.checkBox_water_text.setChecked(True)
            self.ui.lineEdit_water_text.setText(self.cur_conf['watermark']['text'])
            if self.cur_conf['watermark']['text_time_flag'] == '0':
                self.ui.radioButton_text_all.setChecked(True)
            if self.cur_conf['watermark']['text_time_flag'] == '1':
                self.ui.radioButton_text_start.setChecked(True)
                self.ui.radioButton_text_start.setText(self.cur_conf['watermark']['text_time'])
            if self.cur_conf['watermark']['text_time_flag'] == '2':
                self.ui.radioButton_text_end.setChecked(True)
                self.ui.radioButton_text_end.setText(self.cur_conf['watermark']['text_time'])
        else:
            self.ui.checkBox_water_text.setChecked(False)

        if self.cur_conf['watermark']['pic_flag'] == '1':
            self.ui.checkBox_water_pic.setChecked(True)
            file_name = os.path.basename(self.cur_conf['watermark']['pic_file'])
            self.ui.label_water_pic.setText(file_name)
            self.water_pic = self.cur_conf['watermark']['pic_file']

            if self.cur_conf['watermark']['pic_time_flag'] == '0':
                self.ui.radioButton_pic_all.setChecked(True)
            if self.cur_conf['watermark']['pic_time_flag'] == '1':
                self.ui.radioButton_pic_start.setChecked(True)
                self.ui.radioButton_pic_start.setText(self.cur_conf['watermark']['pic_time'])
            if self.cur_conf['watermark']['pic_time_flag'] == '2':
                self.ui.radioButton_pic_end.setChecked(True)
                self.ui.radioButton_pic_end.setText(self.cur_conf['watermark']['pic_time'])
        else:
            self.ui.checkBox_water_pic.setChecked(False)

        if self.cur_conf['watermark']['gif_flag'] == '1':
            self.ui.checkBox_water_gif.setChecked(True)
            file_name = os.path.basename(self.cur_conf['watermark']['gif_file'])
            self.ui.label_water_gif.setText(file_name)
            self.water_gif = self.cur_conf['watermark']['gif_file']

            if self.cur_conf['watermark']['gif_time_flag'] == '0':
                self.ui.radioButton_gif_all.setChecked(True)
            if self.cur_conf['watermark']['gif_time_flag'] == '1':
                self.ui.radioButton_gif_start.setChecked(True)
                self.ui.radioButton_gif_start.setText(self.cur_conf['watermark']['gif_time'])
            if self.cur_conf['watermark']['gif_time_flag'] == '2':
                self.ui.radioButton_gif_end.setChecked(True)
                self.ui.radioButton_gif_end.setText(self.cur_conf['watermark']['gif_time'])
        else:
            self.ui.checkBox_water_gif.setChecked(False)

        #         后期
        self.ui.checkBox_extension.setChecked(True)
        temp_list = ['.mp4', '.flv', '.avi', '.mov']
        self.ui.comboBox_extension.setCurrentIndex(temp_list.index(self.cur_conf['ending']['extension']))
        if self.cur_conf['ending']['ration_flag'] != '0':
            self.ui.checkBox_ending_ration.setChecked(True)
            if self.cur_conf['ending']['ratio_w'] == '1920' and self.cur_conf['ending']['ratio_h'] == '1080':
                self.ui.comboBox_ending_ration.setCurrentIndex(0)
            if self.cur_conf['ending']['ratio_w'] == '1080' and self.cur_conf['ending']['ratio_h'] == '1920':
                self.ui.comboBox_ending_ration.setCurrentIndex(1)

            if self.cur_conf['ending']['ration_flag'] == '1' and self.cur_conf['ending']['padding_color'] == '':
                self.ui.radioButton_4.setChecked(True)
            if self.cur_conf['ending']['ration_flag'] == '1' and self.cur_conf['ending']['padding_color'] != '':
                self.ui.radioButton.setChecked(True)
                self.ui.lineEdit_color_ending.setText(self.cur_conf['ending']['padding_color'])

            if self.cur_conf['ending']['ration_flag'] == '4':
                self.ui.radioButton_2.setChecked(True)  # 图片
                file_name = os.path.basename(self.cur_conf['ending']['padding_pic'])
                self.ui.label_padding_pic.setText(file_name)
            if self.cur_conf['ending']['ration_flag'] in ['2', '3']:
                self.ui.radioButton_3.setChecked(True)  # 图片
                self.ui.lineEdit_blur.setText(self.cur_conf['ending']['blur_level'])
        else:
            self.ui.checkBox_ending_ration.setChecked(False)

        if self.cur_conf['ending']['audio_able'] == '1':
            self.ui.checkBox_audio_able.setChecked(False)
        else:
            self.ui.checkBox_audio_able.setChecked(True)

        if self.cur_conf['ending']['bg_audio_flag'] == '1':
            self.ui.checkBox_bg_audio_flag.setChecked(True)
            file_name = os.path.basename(self.cur_conf['ending']['bg_audio_file'])
            self.ui.label_bg_audio.setText(file_name)
            self.ui.lineEdit_bg_audio_volume.setText(self.cur_conf['ending']['bg_audio_volume'])
        else:
            self.ui.checkBox_bg_audio_flag.setChecked(False)

        if self.cur_conf['ending']['video_start_file'] != '':
            self.ui.checkBox_video_start_file.setChecked(True)
            file_name = os.path.basename(self.cur_conf['ending']['video_start_file'])
            self.ui.label_bg_audio.setText(file_name)
        else:
            self.ui.checkBox_video_start_file.setChecked(False)

        if self.cur_conf['ending']['video_end_file'] != '':
            self.ui.checkBox_video_end_file.setChecked(True)
            file_name = os.path.basename(self.cur_conf['ending']['video_end_file'])
            self.ui.label_bg_audio.setText(file_name)
        else:
            self.ui.checkBox_video_end_file.setChecked(False)

        if self.cur_conf['ending']['title_start'] != '' or self.cur_conf['ending']['title_end'] != '':
            self.ui.checkBox_new_title.setChecked(True)
            self.ui.lineEdit_title_start.setText(self.cur_conf['ending']['title_start'])
            self.ui.lineEdit_title_end.setText(self.cur_conf['ending']['title_end'])
        else:
            self.ui.checkBox_new_title.setChecked(False)

        if self.cur_conf['ending']['quality'] != '23':
            self.ui.checkBox_quality.setChecked(True)
            self.ui.lineEdit_quality.setText(self.cur_conf['ending']['quality'])
        else:
            self.ui.checkBox_quality.setChecked(False)

    def save_conf(self):
        self.get_edit_conf()
        conf_file = f'data/conf/conf{self.sender().text()[-1]}.toml'
        save_conf(self.cur_conf, conf_file)
        base_name = os.path.basename(conf_file)
        print(f'配置{base_name}保存成功')

    def rename_conf(self):
        conf_file = f'data/conf/conf{self.sender().objectName()[-1]}.toml'
        temp_conf = read_conf()
        temp_conf['alias']['name'] = self.sender().text()
        save_conf(temp_conf, conf_file)
        print(f'配置{self.sender().objectName()[-1]}重命名-{self.sender().text()}成功！')

    def init_repeate(self):
        self.cube_list.extend(find_cube_files('./data/lut'))
        for cube in self.cube_list:
            self.ui.comboBox_filter.addItem(cube[:-5])

    def start_p_func(self):
        self.is_interrupted = True
        if len(self.video_list) == 0:
            print("请选择视频")
        else:
            self.get_edit_conf()
            for index, video in enumerate(self.video_list):
                try:
                    base_name = os.path.basename(video)
                    video_out_file = f"{self.dir_out}/{base_name}"
                    video_out_file = get_unique_filename(video_out_file)
                    if self.is_interrupted:
                        print(f"第{index}处理中————{base_name}")
                        myedit(input_video=video, output_video='temp/edit.mp4',
                               accurate_cut_flag=self.cur_conf['edit']['accurate_cut_flag'],
                               start_cut_flag=self.cur_conf['edit']['start_cut_flag'],
                               start_cut_time=self.cur_conf['edit']['start_cut_time'],
                               end_cut_flag=self.cur_conf['edit']['end_cut_flag'],
                               end_cut_time=self.cur_conf['edit']['end_cut_time'],
                               end_cut_time_1=self.cur_conf['edit']['end_cut_time_1'],
                               delogo_flag=self.cur_conf['edit']['delogo_flag'],
                               delog_x=self.cur_conf['edit']['delog_x'],
                               delog_y=self.cur_conf['edit']['delog_y'], delog_w=self.cur_conf['edit']['delog_w'],
                               delog_h=self.cur_conf['edit']['delog_h'],
                               crop_flag=self.cur_conf['edit']['crop_flag'], crop_x=self.cur_conf['edit']['crop_x'],
                               crop_y=self.cur_conf['edit']['crop_y'], crop_w=self.cur_conf['edit']['crop_w'],
                               crop_h=self.cur_conf['edit']['crop_h'],
                               ration_flag=self.cur_conf['edit']['ration_flag'],
                               ratio_w=self.cur_conf['edit']['ratio_w'],
                               ratio_h=self.cur_conf['edit']['ratio_h'],
                               padding_color=self.cur_conf['edit']['padding_color'])
                        if self.is_interrupted:
                            remove_duplicate_api(input_file="temp/edit.mp4", out_file="temp/repeate.mp4",
                                                 cut_fps=self.cur_conf['repeate']['cut_fps'],
                                                 fps=self.cur_conf['repeate']['fps'],
                                                 multi_play_value=self.cur_conf['repeate']['multi_play_value'],
                                                 mate_flag=self.cur_conf['repeate']['mata_flag'],
                                                 title=self.cur_conf['repeate']['title'],
                                                 author=self.cur_conf['repeate']['author'],
                                                 description=self.cur_conf['repeate']['description'],
                                                 copyright=self.cur_conf['repeate']['copyright'],
                                                 cube_flag=self.cur_conf['repeate']['cube_flag'],
                                                 cube_value=self.cur_conf['repeate']['cube_value'],
                                                 gamma=self.cur_conf['repeate']['gamma'],
                                                 brightness=self.cur_conf['repeate']['brightness'],
                                                 contrast=self.cur_conf['repeate']['contrast'],
                                                 saturation=self.cur_conf['repeate']['saturation'],
                                                 mask_flag=self.cur_conf['repeate']['mask_flag'],
                                                 mask_pic_url=self.cur_conf['repeate']['mask_pic_url'],
                                                 mask_trans=self.cur_conf['repeate']['mask_trans'],
                                                 type='long')
                        if self.is_interrupted:
                            water_api(input_file="temp/repeate.mp4", out_file="temp/water.mp4",
                                      text_flag=self.cur_conf['watermark']['text_flag'],
                                      text=self.cur_conf['watermark']['text'],
                                      font_size=self.cur_conf['watermark']['font_size'],
                                      text_time_flag=self.cur_conf['watermark']['text_time_flag'],
                                      text_time=self.cur_conf['watermark']['text_time'],
                                      text_x=self.cur_conf['watermark']['text_x'],
                                      text_y=self.cur_conf['watermark']['text_y'],
                                      pic_flag=self.cur_conf['watermark']['pic_flag'],
                                      pic_file=self.cur_conf['watermark']['pic_file'],
                                      pic_size_w=self.cur_conf['watermark']['pic_size_w'],
                                      pic_time_flag=self.cur_conf['watermark']['pic_time_flag'],
                                      pic_time=self.cur_conf['watermark']['pic_time'],
                                      pic_x=self.cur_conf['watermark']['pic_x'],
                                      pic_y=self.cur_conf['watermark']['pic_y'],
                                      gif_flag=self.cur_conf['watermark']['gif_flag'],
                                      gif_file=self.cur_conf['watermark']['gif_file'],
                                      gif_size_w=self.cur_conf['watermark']['gif_size_w'],
                                      gif_time_flag=self.cur_conf['watermark']['gif_time_flag'],
                                      gif_time=self.cur_conf['watermark']['gif_time'],
                                      gif_x=self.cur_conf['watermark']['gif_x'],
                                      gif_y=self.cur_conf['watermark']['gif_y'],
                                      )
                        if self.is_interrupted:
                            # 文字放在后期之前
                            if self.ui.comboBox_ending_ration.currentIndex() == 0:
                                temp_w = 1920
                                temp_h = 1080
                            if self.ui.comboBox_ending_ration.currentIndex() == 1:
                                temp_w = 1080
                                temp_h = 1920
                            self.ass_list = []
                            self.ass_type_list = []
                            self.ass_time_list = []
                            if self.ui.checkBox_letter1.isChecked():
                                self.lineEdit_letter1 = '文本1未选定文字' if self.ui.lineEdit_letter1.text() == '' else self.ui.lineEdit_letter1.text()
                                save_ass(
                                    ass_content=get_ass(text=self.lineEdit_letter1, long_time='time_not_defined',
                                                        font_name=self.ui.lineEdit_font1.text(),
                                                        ass_type=self.ui.comboBox_in_form1.currentText(),
                                                        font_color=self.ui.lineEdit_color_l1.text(),
                                                        font_size=self.font_size_1 * temp_h * 0.7,
                                                        posx=(self.pos_x_1 + self.ratio_w_1 / 2) * temp_w,
                                                        posy=(self.pos_y_1 + self.font_size_1 / 2) * temp_h,
                                                        ratio_w=temp_w, ratio_h=temp_h,
                                                        start_time1='time_start1_not_defined',
                                                        start_time2='time_start2_not_defined'),
                                    output_file_path='data/ass/temp1.ass')
                                self.ass_list.append('data/ass/temp1.ass')
                                self.ass_type_list.append(self.ui.comboBox_in_form1.currentText())
                                self.ass_time_list.append({'start': self.ui.lineEdit_letter_s1.text(),
                                                           'end': self.ui.lineEdit_letter_e1.text()})
                        if self.is_interrupted:
                            if self.ui.checkBox_letter2.isChecked():
                                self.lineEdit_letter2 = '文本2未选定文字' if self.ui.lineEdit_letter2.text() == '' else self.ui.lineEdit_letter2.text()
                                save_ass(
                                    ass_content=get_ass(text=self.lineEdit_letter2, long_time='time_not_defined',
                                                        font_name=self.ui.lineEdit_font2.text(),
                                                        ass_type=self.ui.comboBox_in_form2.currentText(),
                                                        font_color=self.ui.lineEdit_color_l2.text(),
                                                        font_size=self.font_size_2 * temp_h * 0.7,
                                                        posx=(self.pos_x_2 + self.ratio_w_2 / 2) * temp_w,
                                                        posy=(self.pos_y_2 + self.font_size_2 / 2) * temp_h,
                                                        ratio_w=temp_w, ratio_h=temp_h,
                                                        start_time1='time_start1_not_defined',
                                                        start_time2='time_start2_not_defined'),
                                    output_file_path='data/ass/temp2.ass')
                                self.ass_list.append('data/ass/temp2.ass')
                                self.ass_type_list.append(self.ui.comboBox_in_form2.currentText())
                                self.ass_time_list.append({'start': self.ui.lineEdit_letter_s2.text(),
                                                           'end': self.ui.lineEdit_letter_e2.text()})
                        if self.is_interrupted:
                            if self.ui.checkBox_letter3.isChecked():
                                self.lineEdit_letter3 = '文本3未选定文字' if self.ui.lineEdit_letter3.text() == '' else self.ui.lineEdit_letter3.text()
                                save_ass(
                                    ass_content=get_ass(text=self.lineEdit_letter3, long_time='time_not_defined',
                                                        font_name=self.ui.lineEdit_font3.text(),
                                                        ass_type=self.ui.comboBox_in_form3.currentText(),
                                                        font_color=self.ui.lineEdit_color_l3.text(),
                                                        font_size=self.font_size_3 * temp_h * 0.7,
                                                        posx=(self.pos_x_3 + self.ratio_w_3 / 2) * temp_w,
                                                        posy=(self.pos_y_3 + self.font_size_3 / 2) * temp_h,
                                                        ratio_w=temp_w, ratio_h=temp_h,
                                                        start_time1='time_start1_not_defined',
                                                        start_time2='time_start2_not_defined'),
                                    output_file_path='data/ass/temp3.ass')
                                self.ass_list.append('data/ass/temp3.ass')
                                self.ass_type_list.append(self.ui.comboBox_in_form3.currentText())
                                self.ass_time_list.append({'start': self.ui.lineEdit_letter_s3.text(),
                                                           'end': self.ui.lineEdit_letter_e3.text()})
                        if self.is_interrupted:
                            if self.ui.checkBox_letter4.isChecked():
                                self.lineEdit_letter4 = '文本4未选定文字' if self.ui.lineEdit_letter4.text() == '' else self.ui.lineEdit_letter4.text()
                                save_ass(
                                    ass_content=get_ass(text=self.lineEdit_letter4, long_time='time_not_defined',
                                                        font_name=self.ui.lineEdit_font4.text(),
                                                        ass_type=self.ui.comboBox_in_form4.currentText(),
                                                        font_color=self.ui.lineEdit_color_l4.text(),
                                                        font_size=self.font_size_4 * temp_h * 0.7,
                                                        posx=(self.pos_x_4 + self.ratio_w_4 / 2) * temp_w,
                                                        posy=(self.pos_y_4 + self.font_size_4 / 2) * temp_h,
                                                        ratio_w=temp_w, ratio_h=temp_h,
                                                        start_time1='time_start1_not_defined',
                                                        start_time2='time_start2_not_defined'),
                                    output_file_path='data/ass/temp4.ass')
                                self.ass_list.append('data/ass/temp4.ass')
                                self.ass_type_list.append(self.ui.comboBox_in_form1.currentText())
                                self.ass_time_list.append({'start': self.ui.lineEdit_letter_s4.text(),
                                                           'end': self.ui.lineEdit_letter_e4.text()})
                        # print(self.ass_type_list,self.ass_time_list)
                        if self.is_interrupted:
                            ending_api(input_file="temp/water.mp4", out_file=video_out_file,
                                       extension=self.cur_conf['ending']['extension'],
                                       ratio_h=self.cur_conf['ending']['ratio_h'],
                                       ratio_w=self.cur_conf['ending']['ratio_w'],
                                       ration_flag=self.cur_conf['ending']['ration_flag'],
                                       padding_color=self.cur_conf['ending']['padding_color'],
                                       blur_level=self.cur_conf['ending']['blur_level'],
                                       audio_able=self.cur_conf['ending']['audio_able'],
                                       bg_audio_flag=self.cur_conf['ending']['bg_audio_flag'],
                                       bg_audio_file=self.cur_conf['ending']['bg_audio_file'],
                                       bg_audio_volume=self.cur_conf['ending']['bg_audio_volume'],
                                       title_start=self.cur_conf['ending']['title_start'],
                                       title_end=self.cur_conf['ending']['title_end'],
                                       video_start_file=self.cur_conf['ending']['video_start_file'],
                                       video_end_file=self.cur_conf['ending']['video_end_file'],
                                       padding_pic=self.cur_conf['ending']['padding_pic'],
                                       quality=self.cur_conf['ending']['quality'],
                                       quality_flag=self.cur_conf['ending']['quality_flag'], ass_list=self.ass_list,
                                       ass_type_list=self.ass_type_list, ass_time_list=self.ass_time_list
                                       )
                            print(f"处理完成")
                    else:
                        break
                except:
                    continue

    def stop_p_func(self):
        self.is_interrupted = False
        print('——处理终止——')

    def get_edit_conf(self):
        #  edit
        self.cur_conf['edit']['accurate_cut_flag'] = '1' if self.ui.checkBox_accurate_cut.isChecked() else '0'

        if self.ui.checkBox_start.isChecked():
            self.cur_conf['edit']['start_cut_flag'] = '1'
            # self.cur_conf['edit']['start_cut_time'] = self.ui.lineEdit_start.text()
            self.cur_conf['edit'][
                'start_cut_time'] = self.ui.lineEdit_start.text() if self.ui.lineEdit_start.text() != '' else '0'
        else:
            self.cur_conf['edit']['start_cut_flag'] = '0'

        if self.ui.checkBox_end.isChecked():
            self.cur_conf['edit']['end_cut_flag'] = '1'
            # self.cur_conf['edit']['end_cut_time'] = self.ui.lineEdit_end.text()
            self.cur_conf['edit'][
                'end_cut_time'] = self.ui.lineEdit_end.text() if self.ui.lineEdit_end.text() != '' else '0'
        else:
            self.cur_conf['edit']['end_cut_flag'] = '0'

        if self.ui.checkBox_cut.isChecked():
            if self.ui.lineEdit_cut_start.text() != '':
                self.cur_conf['edit']['start_cut_flag'] = '1'
                self.cur_conf['edit']['start_cut_time'] = self.ui.lineEdit_cut_start.text()
            else:
                self.cur_conf['edit']['start_cut_flag'] = '0'
            if self.ui.lineEdit_cut_end.text() != '':
                self.cur_conf['edit']['end_cut_flag'] = '2'
                self.cur_conf['edit']['end_cut_time_1'] = self.ui.lineEdit_cut_end.text()
            else:
                self.cur_conf['edit']['end_cut_flag'] = '0'
                self.cur_conf['edit']['end_cut_time_1'] = ''

        if self.ui.checkBox_water.isChecked():
            self.cur_conf['edit']['delogo_flag'] = '1'
            self.cur_conf['edit']['delog_x'] = self.ui.lineEdit_water_x.text()
            self.cur_conf['edit']['delog_y'] = self.ui.lineEdit_water_y.text()
            self.cur_conf['edit']['delog_w'] = self.ui.lineEdit_water_w.text()
            self.cur_conf['edit']['delog_h'] = self.ui.lineEdit_water_h.text()
        else:
            self.cur_conf['edit']['delogo_flag'] = '0'

        if self.ui.checkBox_crop.isChecked():
            self.cur_conf['edit']['crop_flag'] = '1'
            self.cur_conf['edit']['crop_x'] = self.ui.lineEdit_crop_left.text()
            self.cur_conf['edit']['crop_y'] = self.ui.lineEdit_crop_top.text()
            self.cur_conf['edit']['crop_w'] = self.video_w - float(self.ui.lineEdit_crop_right.text())
            self.cur_conf['edit']['crop_h'] = self.video_h - float(self.ui.lineEdit_crop_buttom.text())
        else:
            self.cur_conf['edit']['crop_flag'] = '0'

        if self.ui.checkBox_ratio.isChecked():
            self.cur_conf['edit']['ration_flag'] = '1'
            self.cur_conf['edit']['ratio_w'] = self.ui.lineEdit_ratio_w.text()
            self.cur_conf['edit']['ratio_h'] = self.ui.lineEdit_ratio_h.text()
        else:
            self.cur_conf['edit']['checkBox_ratio'] = '0'
        # 颜色填充
        self.cur_conf['edit'][
            'padding_color'] = self.ui.lineEdit_color.text() if self.ui.checkBox_color.isChecked() else ''
        # print(self.cur_conf['edit'])

        # repeat

        self.cur_conf['repeate'][
            'cut_fps'] = self.ui.lineEdit_cut_fps.text() if self.ui.checkBox_cut_fps.isChecked() else ''
        self.cur_conf['repeate']['fps'] = self.ui.lineEdit_fps.text() if self.ui.checkBox_fps.isChecked() else ''
        self.cur_conf['repeate'][
            'multi_play_value'] = self.ui.lineEdit_multiplay.text() if self.ui.checkBox_multiplay.isChecked() else '1'
        if self.ui.checkBox_filter.isChecked():
            self.cur_conf['repeate']['cube_flag'] = '1'
            self.cur_conf['repeate']['cube_value'] = 'data/lut/' + self.ui.comboBox_filter.currentText() + '.cube'
        else:
            self.cur_conf['repeate']['cube_flag'] = '0'

        if self.ui.checkBox_mate.isChecked():
            self.cur_conf['repeate']['mata_flag'] = '1'
            self.cur_conf['repeate']['title'] = self.ui.lineEdit_title.text()
            self.cur_conf['repeate']['author'] = self.ui.lineEdit_author.text()
            self.cur_conf['repeate']['description'] = self.ui.lineEdit_des.text()
            self.cur_conf['repeate']['copyright'] = self.ui.lineEdit_copyright.text()
        else:
            self.cur_conf['repeate']['mata_flag'] = '0'

        if self.ui.checkBox_color_video.isChecked():
            self.cur_conf['repeate']['gamma'] = self.ui.lineEdit_gamma.text()
            self.cur_conf['repeate']['brightness'] = self.ui.lineEdit_brightness.text()
            self.cur_conf['repeate']['contrast'] = self.ui.lineEdit_contrast.text()
            self.cur_conf['repeate']['saturation'] = self.ui.lineEdit_saturation.text()
        else:
            self.cur_conf['repeate']['gamma'] = '1'
            self.cur_conf['repeate']['brightness'] = '0'
            self.cur_conf['repeate']['contrast'] = '1'
            self.cur_conf['repeate']['saturation'] = '1'
        if self.ui.checkBox_mask.isChecked():
            self.cur_conf['repeate']['mask_flag'] = '1'
            self.cur_conf['repeate']['mask_trans'] = self.ui.lineEdit_trans.text()
        else:
            self.cur_conf['repeate']['mask_flag'] = '0'
        # print(self.cur_conf['repeate'])

        # ending配置
        if self.ui.checkBox_extension.isChecked():
            self.cur_conf['ending']['extension'] = self.ui.comboBox_extension.currentText()
        else:
            self.cur_conf['ending']['extension'] = '.mp4'

        if self.ui.checkBox_ending_ration.isChecked():
            if self.ui.comboBox_ending_ration.currentIndex() == 0:
                self.cur_conf['ending']['ratio_w'] = '1920'
                self.cur_conf['ending']['ratio_h'] = '1080'
            elif self.ui.comboBox_ending_ration.currentIndex() == 1:
                self.cur_conf['ending']['ratio_w'] = '1080'
                self.cur_conf['ending']['ratio_h'] = '1920'

            if self.ui.radioButton_4.isChecked():  # 改变尺寸  不填充  也就是填充颜色为空
                self.cur_conf['ending']['ration_flag'] = '1'
                self.cur_conf['ending']['padding_color'] = ''
            if self.ui.radioButton.isChecked():  # 颜色填充
                self.cur_conf['ending']['ration_flag'] = '1'
                self.cur_conf['ending']['padding_color'] = self.ui.lineEdit_color_ending.text()
            if self.ui.radioButton_2.isChecked():  # 图片
                self.cur_conf['ending']['ration_flag'] = '4'

            if self.ui.radioButton_3.isChecked():  # 模糊填充
                self.cur_conf['ending']['blur_level'] = self.ui.lineEdit_blur.text()
                if int(self.cur_conf['ending']['ratio_w']) >= int(self.cur_conf['ending']['ratio_h']):
                    self.cur_conf['ending']['ration_flag'] = '2'
                if int(self.cur_conf['ending']['ratio_w']) < int(self.cur_conf['ending']['ratio_h']):
                    self.cur_conf['ending']['ration_flag'] = '3'
        else:
            self.cur_conf['ending']['ration_flag'] = '0'  # 不改变尺寸

        self.cur_conf['ending']['audio_able'] = '0' if self.ui.checkBox_audio_able.isChecked() else '1'
        self.cur_conf['ending']['video_start_file'] = self.cur_conf['ending'][
            'video_start_file'] if self.ui.checkBox_video_start_file.isChecked() else ''
        self.cur_conf['ending']['video_end_file'] = self.cur_conf['ending'][
            'video_end_file'] if self.ui.checkBox_video_end_file.isChecked() else ''

        if self.ui.checkBox_new_title.isChecked():
            self.cur_conf['ending']['title_start'] = self.ui.lineEdit_title_start.text()
            self.cur_conf['ending']['title_end'] = self.ui.lineEdit_title_end.text()
        else:
            self.cur_conf['ending']['title_start'] = ''
            self.cur_conf['ending']['title_end'] = ''

        if self.ui.checkBox_bg_audio_flag.isChecked():
            self.cur_conf['ending']['bg_audio_flag'] = '1'
            self.cur_conf['ending']['bg_audio_volume'] = self.ui.lineEdit_bg_audio_volume.text()

        else:
            self.cur_conf['ending']['bg_audio_flag'] = '0'

        self.cur_conf['ending']['quality_flag'] = '1' if self.ui.checkBox_audio_able.isChecked() else '0'
        self.cur_conf['ending']['quality'] = self.ui.lineEdit_quality.text()

        # water
        if self.ui.checkBox_water_text.isChecked():
            self.cur_conf['watermark']['text_flag'] = '1'
            self.cur_conf['watermark']['text'] = self.ui.lineEdit_water_text.text()
            if self.ui.radioButton_text_all.isChecked():
                self.cur_conf['watermark']['text_time_flag'] = '0'
            if self.ui.radioButton_text_start.isChecked():
                self.cur_conf['watermark']['text_time_flag'] = '1'
                self.cur_conf['watermark'][
                    'text_time'] = self.ui.lineEdit_text_start.text() if self.ui.lineEdit_text_start.text() != '' else '0'
            if self.ui.radioButton_text_end.isChecked():
                self.cur_conf['watermark']['text_time_flag'] = '2'
                self.cur_conf['watermark'][
                    'text_time'] = self.ui.lineEdit_text_end.text() if self.ui.lineEdit_text_end.text() != '' else '0'
        else:
            self.cur_conf['watermark']['text_flag'] = '0'
        #         TODO
        if self.ui.checkBox_water_pic.isChecked():
            self.cur_conf['watermark']['pic_flag'] = '1'
            self.cur_conf['watermark']['pic_file'] = self.water_pic
            if self.ui.radioButton_pic_all.isChecked():
                self.cur_conf['watermark']['pic_time_flag'] = '0'
            if self.ui.radioButton_pic_start.isChecked():
                self.cur_conf['watermark']['pic_time_flag'] = '1'
                self.cur_conf['watermark'][
                    'pic_time'] = self.ui.lineEdit_pic_start.text() if self.ui.lineEdit_pic_start.text() != '' else '0'
            if self.ui.radioButton_pic_end.isChecked():
                self.cur_conf['watermark']['pic_time_flag'] = '2'
                self.cur_conf['watermark'][
                    'pic_time'] = self.ui.lineEdit_pic_end.text() if self.ui.lineEdit_pic_end.text() != '' else '0'
        else:
            self.cur_conf['watermark']['pic_flag'] = '0'
        if self.ui.checkBox_water_gif.isChecked():
            self.cur_conf['watermark']['gif_flag'] = '1'
            self.cur_conf['watermark']['gif_file'] = self.water_gif
            if self.ui.radioButton_gif_all.isChecked():
                self.cur_conf['watermark']['gif_time_flag'] = '0'
            if self.ui.radioButton_gif_start.isChecked():
                self.cur_conf['watermark']['gif_time_flag'] = '1'
                self.cur_conf['watermark'][
                    'gif_time'] = self.ui.lineEdit_gif_start.text() if self.ui.lineEdit_gif_start.text() != '' else '0'
            if self.ui.radioButton_gif_end.isChecked():
                self.cur_conf['watermark']['gif_time_flag'] = '2'
                self.cur_conf['watermark'][
                    'gif_time'] = self.ui.lineEdit_gif_end.text() if self.ui.lineEdit_gif_end.text() != '' else '0'
        else:
            self.cur_conf['watermark']['gif_flag'] = '0'

    # 选取蒙版图片
    def choose_mask_pic(self):
        pic_file, _ = QFileDialog.getOpenFileName(None, "打开", "./", "图片文件(*.png *.jpg *.jpeg *.bmp *.gif *.tiff)")
        if not pic_file:
            print("用户未选择文件")
        else:
            # print("选择的文件:", conf_file)
            file_name = os.path.basename(pic_file)
            self.ui.label_pic_mask.setText(file_name)
            self.cur_conf['repeate']['mask_pic_url'] = pic_file

    def preview_water(self):
        if len(self.video_list) == 0:
            print("请导入视频")
        else:
            try:
                self.get_edit_conf()
                print("预览准备中")
                # print(self.cur_conf['watermark']['text_flag'],self.cur_conf['watermark']['pic_flag'],self.cur_conf['watermark']['gif_flag'])
                water_api(input_file=self.current_pre_video, out_file='temp/pre.mp4',
                          text_flag=self.cur_conf['watermark']['text_flag'], text=self.cur_conf['watermark']['text'],
                          font_size=self.cur_conf['watermark']['font_size'],
                          text_time_flag=self.cur_conf['watermark']['text_time_flag'],
                          text_time=self.cur_conf['watermark']['text_time'],
                          text_x=self.cur_conf['watermark']['text_x'],
                          text_y=self.cur_conf['watermark']['text_y'],
                          pic_flag=self.cur_conf['watermark']['pic_flag'],
                          pic_file=self.cur_conf['watermark']['pic_file'],
                          pic_size_w=self.cur_conf['watermark']['pic_size_w'],
                          pic_time_flag=self.cur_conf['watermark']['pic_time_flag'],
                          pic_time=self.cur_conf['watermark']['pic_time'],
                          pic_x=self.cur_conf['watermark']['pic_x'],
                          pic_y=self.cur_conf['watermark']['pic_y'],
                          gif_flag=self.cur_conf['watermark']['gif_flag'],
                          gif_file=self.cur_conf['watermark']['gif_file'],
                          gif_size_w=self.cur_conf['watermark']['gif_size_w'],
                          gif_time_flag=self.cur_conf['watermark']['gif_time_flag'],
                          gif_time=self.cur_conf['watermark']['gif_time'],
                          gif_x=self.cur_conf['watermark']['gif_x'],
                          gif_y=self.cur_conf['watermark']['gif_y'],
                          )

                pre_video('temp/pre.mp4')
            except:
                print("配置错误，预览失败")

    def preview_ending(self):
        if len(self.video_list) == 0:
            print("请导入视频")
        else:
            try:
                self.get_edit_conf()
                print("预览准备中")
                ending_api(input_file=self.current_pre_video, out_file='temp/pre.mp4',
                           extension=self.cur_conf['ending']['extension'],
                           ratio_h=self.cur_conf['ending']['ratio_h'], ratio_w=self.cur_conf['ending']['ratio_w'],
                           ration_flag=self.cur_conf['ending']['ration_flag'],
                           padding_color=self.cur_conf['ending']['padding_color'],
                           blur_level=self.cur_conf['ending']['blur_level'],
                           audio_able=self.cur_conf['ending']['audio_able'],
                           bg_audio_flag=self.cur_conf['ending']['bg_audio_flag'],
                           bg_audio_file=self.cur_conf['ending']['bg_audio_file'],
                           bg_audio_volume=self.cur_conf['ending']['bg_audio_volume'],
                           title_start='', title_end='',
                           video_start_file=self.cur_conf['ending']['video_start_file'],
                           video_end_file=self.cur_conf['ending']['video_end_file'],
                           padding_pic=self.cur_conf['ending']['padding_pic'],
                           quality=self.cur_conf['ending']['quality'],
                           quality_flag=self.cur_conf['ending']['quality_flag']
                           )
                pre_video('temp/pre.mp4')
            except:
                print("配置错误，预览失败")

    def preview_repeate(self):
        if len(self.video_list) == 0:
            print("请导入视频")
        else:
            try:
                self.get_edit_conf()
                print("预览准备中")
                remove_duplicate_api(input_file=self.current_pre_video, out_file='temp/pre.mp4',
                                     cut_fps=self.cur_conf['repeate']['cut_fps'], fps=self.cur_conf['repeate']['fps'],
                                     multi_play_value=self.cur_conf['repeate']['multi_play_value'],
                                     mate_flag=self.cur_conf['repeate']['mata_flag'],
                                     title=self.cur_conf['repeate']['title'], author=self.cur_conf['repeate']['author'],
                                     description=self.cur_conf['repeate']['description'],
                                     copyright=self.cur_conf['repeate']['copyright'],
                                     cube_flag=self.cur_conf['repeate']['cube_flag'],
                                     cube_value=self.cur_conf['repeate']['cube_value'],
                                     gamma=self.cur_conf['repeate']['gamma'],
                                     brightness=self.cur_conf['repeate']['brightness'],
                                     contrast=self.cur_conf['repeate']['contrast'],
                                     saturation=self.cur_conf['repeate']['saturation'],
                                     mask_flag=self.cur_conf['repeate']['mask_flag'],
                                     mask_pic_url=self.cur_conf['repeate']['mask_pic_url'],
                                     mask_trans=self.cur_conf['repeate']['mask_trans'],
                                     type='temp')
                pre_video('temp/pre.mp4')
            except:
                print("配置错误，预览失败")

    def preview_fun(self):
        if len(self.video_list) == 0:
            print("请导入视频")
        else:
            try:
                self.get_edit_conf()
                print("预览准备中")
                myedit(input_video=self.current_pre_video, output_video='temp/temp.mp4',
                       accurate_cut_flag=self.cur_conf['edit']['accurate_cut_flag'],
                       start_cut_flag=self.cur_conf['edit']['start_cut_flag'],
                       start_cut_time=self.cur_conf['edit']['start_cut_time'],
                       end_cut_flag='2', end_cut_time='0',
                       end_cut_time_1=str(float(self.cur_conf['edit']['start_cut_time']) + 3),
                       delogo_flag=self.cur_conf['edit']['delogo_flag'], delog_x=self.cur_conf['edit']['delog_x'],
                       delog_y=self.cur_conf['edit']['delog_y'], delog_w=self.cur_conf['edit']['delog_w'],
                       delog_h=self.cur_conf['edit']['delog_h'],
                       crop_flag=self.cur_conf['edit']['crop_flag'], crop_x=self.cur_conf['edit']['crop_x'],
                       crop_y=self.cur_conf['edit']['crop_y'], crop_w=self.cur_conf['edit']['crop_w'],
                       crop_h=self.cur_conf['edit']['crop_h'],
                       ration_flag=self.cur_conf['edit']['ration_flag'], ratio_w=self.cur_conf['edit']['ratio_w'],
                       ratio_h=self.cur_conf['edit']['ratio_h'], padding_color=self.cur_conf['edit']['padding_color'])
                # self.temp_video_dialog=temp_video_dialog('temp/temp.mp4')
                # self.temp_video_dialog.show()

                pre_video('temp/temp.mp4')
            except:
                print("配置错误，预览失败")

        # 颜色选择

    def choose_color(self):
        self.edit_color = QColorDialog.getColor().name()
        self.ui.lineEdit_color.setText(self.edit_color)

    def choose_color_ending(self):
        self.edit_color = QColorDialog.getColor().name()
        self.ui.lineEdit_color_ending.setText(self.edit_color)

    #  选择填充图片
    def choose_padding_pic(self):
        pic_file, _ = QFileDialog.getOpenFileName(None, "打开", "./", "图片文件(*.png *.jpg *.jpeg *.bmp *.gif *.tiff)")
        if not pic_file:
            print("用户未选择文件")
        else:
            # print("选择的文件:", conf_file)
            file_name = os.path.basename(pic_file)
            self.ui.label_padding_pic.setText(file_name)
            self.cur_conf['ending']['padding_pic'] = pic_file

    #  选择背景音乐
    def choose_bg_audio(self):
        audio_file, _ = QFileDialog.getOpenFileName(None, "打开", "./",
                                                    "音频文件(*.mp3 *.aac *.WAV *.WMA)")
        if not audio_file:
            print("用户未选择文件")
        else:
            # print("选择的文件:", conf_file)
            file_name = os.path.basename(audio_file)
            self.ui.label_bg_audio.setText(file_name)
            self.cur_conf['ending']['bg_audio_file'] = audio_file

    #  选择片头
    def choose_video_start(self):
        video_file, _ = QFileDialog.getOpenFileName(None, "打开", "./",
                                                    "视频文件(*.mp4 *.avi *.mkv *.mov *.flv *.mpeg)")
        if not video_file:
            print("用户未选择文件")
        else:
            # print("选择的文件:", conf_file)
            file_name = os.path.basename(video_file)
            self.ui.label_video_start_file.setText(file_name)
            self.cur_conf['ending']['video_start_file'] = video_file

    #  选择片尾
    def choose_video_end(self):
        video_file, _ = QFileDialog.getOpenFileName(None, "打开", "./",
                                                    "视频文件(*.mp4 *.avi *.mkv *.mov *.flv *.mpeg)")
        if not video_file:
            print("用户未选择文件")
        else:
            # print("选择的文件:", conf_file)
            file_name = os.path.basename(video_file)
            self.ui.label_video_end_file.setText(file_name)
            self.cur_conf['ending']['video_end_file'] = video_file

    def init_table(self):
        row_count = 200
        self.ui.my_table.setRowCount(row_count)  # 设置表格的行数
        # 设置固定行高
        row_height = 25  # 设置行高度为30像素
        for row in range(self.ui.my_table.rowCount()):
            self.ui.my_table.setRowHeight(row, row_height)

        row_name = []
        for i in range(row_count):
            row_name.append(str(i))
        self.ui.my_table.setVerticalHeaderLabels(row_name)
        line_count = 2
        self.ui.my_table.setColumnCount(line_count)  # 设置表格的行数
        line_name = ['名称', '视频时长']
        self.ui.my_table.setHorizontalHeaderLabels(line_name)
        # 列宽度
        self.ui.my_table.setColumnWidth(0, 120)
        self.ui.my_table.setColumnWidth(1, 90)

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """
        自定义异常处理函数
        """
        # 在这里添加你希望执行的异常处理逻辑
        # 例如，显示一个错误对话框或将异常信息记录到日志文件中
        QMessageBox.critical(None, "Error", str(exc_value))
        print('error')
        # 如果你希望终止应用程序，可以在这里调用 sys.exit()
        # sys.exit(1)

    # 多选视频文件
    def open_video(self):
        history_file_conf = read_conf('data/history_floder/folder.toml')
        if not os.path.exists(history_file_conf['folder']['file1']):
            history_file_conf['folder']['file1'] = './'

        files, _ = QFileDialog.getOpenFileNames(None, "打开", history_file_conf['folder']['file1'],
                                                "视频文件(*.mp4 *.avi *.mkv *.mov *.flv *.mpeg)")
        if not files:
            print("用户未选择文件")
        else:
            # print("选择的文件:", conf_file)
            history_file_conf['folder']['file1'] = os.path.dirname(files[0])
            save_conf(history_file_conf, 'data/history_floder/folder.toml')
            self.video_list.extend(files)
            self.current_pre_video = self.video_list[0]
            self.updata_table()

        # 切换槽布局

    def clickButton(self):
        self.cur_button.setStyleSheet("QPushButton {}")
        self.sender().setStyleSheet("QPushButton {background: #00aaff;}")
        self.cur_button = self.sender()
        sender = self.sender()
        if sender.text() == '剪辑':
            self.ui.stackedWidget.setCurrentIndex(0)
        if sender.text() == '消重':
            self.ui.stackedWidget.setCurrentIndex(1)
        if sender.text() == '后期':
            self.ui.stackedWidget.setCurrentIndex(3)
        if sender.text() == '配置':
            self.ui.stackedWidget.setCurrentIndex(2)
        if sender.text() == '混剪':
            self.ui.stackedWidget.setCurrentIndex(4)
        if sender.text() == '水印':
            self.ui.stackedWidget.setCurrentIndex(5)
        if sender.text() == '文字':
            self.ui.stackedWidget.setCurrentIndex(6)
        if sender.text() == '工具':
            self.ui.stackedWidget.setCurrentIndex(7)
        # 打开视频文件夹

    def open_mix_video_func(self):
        conf_file, _ = QFileDialog.getOpenFileNames(None, "打开", "./out", "全部文件(*)")

    def open_dir(self):
        history_file_conf = read_conf('data/history_floder/folder.toml')
        if not os.path.exists(history_file_conf['folder']['file2']):
            history_file_conf['folder']['file2'] = './'
        dir = QFileDialog.getExistingDirectory(None, "选择文件夹路径", history_file_conf['folder']['file2'])
        if not dir:
            print("用户未选择文件")
        else:
            history_file_conf['folder']['file2'] = dir
            save_conf(history_file_conf, 'data/history_floder/folder.toml')
            self.video_list.extend(find_video_files(dir))
            self.current_pre_video = self.video_list[0]
            self.updata_table()
        # 打开视频输出文件夹

    def open_out_dir(self):
        out = QFileDialog.getExistingDirectory(None, "选择文件夹路径", os.getcwd())
        if not self.dir_out:
            print("用户未选择文件")
        else:
            self.dir_out = out
            self.ui.label_out_file.setText(self.dir_out)

        # 重新绘制表格元素

    def updata_table(self):

        try:

            for index, video_item in enumerate(self.video_list):
                self.ui.my_table.setItem(index, 0, QTableWidgetItem('..' + video_item[-10:]))
                self.ui.my_table.setItem(index, 1, QTableWidgetItem(seconds_to_hhmmss(get_video_length(video_item))))
            for i in range(len(self.video_list), 200):
                if self.ui.my_table.item(i, 0) is not None and self.ui.my_table.item(i, 0).text() != '':
                    self.ui.my_table.setItem(i, 0, QTableWidgetItem(''))
                    self.ui.my_table.setItem(i, 1, QTableWidgetItem(''))
                else:
                    break
            self.video_w, self.video_h = get_ratio(self.current_pre_video)
        except:
            print("")  # 超过200，显示问题，但是不影响处理

    def open_video_dialog(self, type):

        if len(self.video_list) == 0:
            print('请导入视频')
        else:
            self.choose_dialog_type = type
            self.video_dialog = video_dialog(self.current_pre_video)
            self.video_dialog.close_dialog.connect(self.video_dialog_signal)
            self.video_dialog.show()

    def video_dialog_signal(self, flag, x, y, w, h):
        if flag == 1 and self.choose_dialog_type == 'water':
            self.ui.lineEdit_water_x.setText(str(x))
            self.ui.lineEdit_water_y.setText(str(y))
            self.ui.lineEdit_water_w.setText(str(w))
            self.ui.lineEdit_water_h.setText(str(h))

        if flag == 1 and self.choose_dialog_type == 'crop':
            self.ui.lineEdit_crop_left.setText(str(x))
            self.ui.lineEdit_crop_top.setText(str(y))
            self.ui.lineEdit_crop_right.setText(str(round(self.video_w - w, 2)))
            self.ui.lineEdit_crop_buttom.setText(str(round(self.video_h - h, 2)))

    def water_dialog_signal(self, flag, x, y, size):
        if flag == 'text':
            self.cur_conf['watermark']['text_x'] = x
            self.cur_conf['watermark']['text_y'] = y
            self.cur_conf['watermark']['font_size'] = size

        if flag == 'pic':
            self.cur_conf['watermark']['pic_x'] = x
            self.cur_conf['watermark']['pic_y'] = y
            self.cur_conf['watermark']['pic_size_w'] = size
        if flag == 'gif':
            self.cur_conf['watermark']['gif_x'] = x
            self.cur_conf['watermark']['gif_y'] = y
            self.cur_conf['watermark']['gif_size_w'] = size
        print("添加成功")

    def item_menu_event(self, pos):
        menu = QMenu(self)
        action1 = QAction("删除本视频", self)
        action2 = QAction("设置当前视频为预览视频", self)
        action3 = QAction("查看视频", self)
        # 获取点击的表格元素的行和列索引
        item = self.ui.my_table.indexAt(pos)

        if item is not None:
            action1.triggered.connect(partial(self.delete_item, item.row()))
            menu.addAction(action1)
            action2.triggered.connect(partial(self.set_current_pre_video, item.row()))
            menu.addAction(action2)
            action3.triggered.connect(partial(self._current_pre_video, item.row()))
            menu.addAction(action3)
        menu.exec(self.ui.my_table.mapToGlobal(pos))

    def delete_item(self, row):
        if int(row) < len(self.video_list):
            del self.video_list[int(row)]
        self.updata_table()

    def set_current_pre_video(self, row):
        if int(row) < len(self.video_list):
            self.current_pre_video = self.video_list[int(row)]

    def _current_pre_video(self, row):
        if int(row) < len(self.video_list):
            pre_video(self.video_list[int(row)])

    def clear_list(self):
        self.video_list = []
        self.updata_table()


# # aaa
def excepthook(exc_type, exc_value, exc_traceback):
    # 异常处理函数
    # 在这里你可以做一些处理，如记录错误日志、显示错误信息等

    print("Exception occurred:", exc_value)

    # 可以阻止程序崩溃，但这取决于你如何处理异常
    # sys.exit(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 将 excepthook 函数设置为全局异常处理函数
    window = mainwindow()
    # aaa
    sys.excepthook = excepthook
    sys.exit(app.exec())
