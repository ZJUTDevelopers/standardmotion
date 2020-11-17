from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import *
import sys
import qdarkstyle, datetime, webbrowser
import os
#from QcureUi import cure
import json
import time
import threading
import win32console
import win32gui
import win32con
from math import *
import pyttsx3
from pyttsx3 import driver
from pyttsx3 import drivers
from pyttsx3.drivers import sapi5

initialed=False
global_points_list=None

def start_openpose():
    os.system("start /min cmd /k C:\\Users\\Hp\\Desktop\\standardmotion\\standardmotion\\src\\main\\python\\start.bat")

folder = 'C:\\Users\\Hp\\Desktop\\standardmotion\\standardmotion\\src\\main\\python\\json'

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # 设置窗口名称
        self.setWindowTitle("standardmotion")

        # 设置状态栏
        self.status = self.statusBar()
        self.status.showMessage("ZJUTDevelpoers")

        # 设置初始化的窗口大小
        self.setFixedSize(1200, 800)
        
        self.center()

        #self.setWindowOpacity(0.9) # 设置窗口透明度

        self.setWindowIcon(QIcon("./src/main/python/1.png")) #设置图标

        # 设置窗口样式
        #self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        # 设置整体布局 左右显示
        pagelayout = QGridLayout()
        
        # 创建左侧主窗口
        top_left_frame = QFrame(self)  
        # 绘制矩形面板
        top_left_frame.setFrameShape(QFrame.StyledPanel)
        #　左边按钮为垂直布局
        button_layout = QVBoxLayout(top_left_frame)

        #MEUN 标签
        label1 = QLabel(self)
        label1.setFixedSize(200,60)
        label1.setText("MENU")
        label1.setAlignment( Qt.AlignCenter) #设置居中
        label1.setFont(QFont("Kaushan",20,QFont.Bold))
        button_layout.addWidget(label1)

  
        pe = QPalette()
        pe.setColor(QPalette.WindowText,QColor(139,147, 194, 250))
        label1.setPalette(pe)

        # 输入文件 按钮
        self.upload_btn = QPushButton("输入文件")
        self.upload_btn.setFixedSize(200, 60)
        button_layout.addWidget(self.upload_btn)
        # 声音 按钮
        self.voice_btn = QPushButton("声音")
        self.voice_btn.setFixedSize(200, 60)
        button_layout.addWidget(self.voice_btn)
        # 火柴人显示 按钮
        self.show_btn = QPushButton("火柴人显示")
        self.show_btn.setFixedSize(200, 60)
        button_layout.addWidget(self.show_btn)
        # 计时 按钮
        self.time_btn = QPushButton("计时")
        self.time_btn.setFixedSize(200, 60)
        button_layout.addWidget(self.time_btn)   
        # 退出 按钮
        self.quit_btn = QPushButton(top_left_frame)
        self.quit_btn.setFixedSize(200, 60), self.quit_btn.setText("退出")
        button_layout.addWidget(self.quit_btn)
        # 增加间距，美化界面
        button_layout.addStretch(1)
        
        right_frame = QFrame(self)
        #right_frame.setFrameShape(QFrame.StyledPanel)
        right_frame.setStyleSheet('background-color:rgb(239,242,249);')
        #right_frame.setFrameShadow(QFrame.Sunken) #设置阴影
        right_frame.setLineWidth(1000)
        
        # 右边显示为stack布局 即点击按钮，右侧会加载不同的页面
        self.right_layout = QVBoxLayout(right_frame)
        # 右侧的布局已经传入了 right_frame 参数 所以后续的控件不用加此参数 布局 addwidget 即可
        # 确认身份 界面

        right_button = QHBoxLayout()
        
        self.start_btn = QPushButton("开始检测")
        self.start_btn.setFixedSize(200, 60)
        right_button.addWidget(self.start_btn)  

        self.end_btn = QPushButton("停止检测")
        self.end_btn.setFixedSize(200, 60)
        right_button.addWidget(self.end_btn)  

        right_label=QLabel("Welcome")
        right_label.setFixedSize(700,500)
        
        right_label.setStyleSheet("QLabel {background-color :rgb(231,234,251);border-radius: 30px;border-style: outset;border-width: 2px;border-color: bule;color:white}")
        right_label.setAlignment(Qt.AlignCenter)
        #添加按钮布局和label1布局
        right_btn_widget = QWidget()
        right_btn_widget.setLayout(right_button)
        self.right_layout.addWidget(right_label)
        self.right_layout.setAlignment(Qt.AlignHCenter | Qt.AlignCenter)
        self.right_layout.addWidget(right_btn_widget)

        right_frame.setMinimumWidth(920)


        self.splitter1 = QSplitter(Qt.Vertical)
        top_left_frame.setFixedHeight(1000)
        self.splitter1.addWidget(top_left_frame)
        
        self.splitter1.setMinimumWidth(200)
        self.splitter2 = QSplitter(Qt.Horizontal)
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.addWidget(right_frame)
        
        
        
        widget = QWidget()
        pagelayout.addWidget(self.splitter2)
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)
        

    def center(self):
        """
        获取桌面长宽  获取窗口长宽 计算位置 移动
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


if __name__ == "__main__":
    App= ApplicationContext()
    App.app.setStyle('Fusion')
    my_gui= MainWindow()
    #win=cure.Windows(gui(),'name',True)##实现对窗口的美化
    my_gui.show()
    sys.exit(App.app.exec_())