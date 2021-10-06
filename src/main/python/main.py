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
import cv2
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
import random
import numpy as np

initialed=False
global global_points_list
global_points_list = []
global if_drawing
if_drawing=0
engine=pyttsx3.init()

def degree_count(x, y):
    # 分别计算两个向量的模：
    l_x = np.sqrt(x.dot(x))
    l_y = np.sqrt(y.dot(y))
    # 计算两个向量的点积
    dian = x.dot(y)
    # 计算夹角的cos值：
    cos_=dian/(l_x*l_y)
    # 求得夹角（弧度制）：
    angle_hu=np.arccos(cos_)
    # 转换为角度值：
    angle_d=angle_hu*180/np.pi
    return angle_d

class DrawCircle(QWidget):
    def __init__(self,parent=None):
        super(DrawCircle,self).__init__(parent)
        self.resize(700,500)
        self.setWindowTitle('在窗口画直线')
        self.setFixedSize(700,500)
        self.frame_path=QPainterPath()
        self.frame_path.addRoundedRect(QRectF(0,0,700,500),50,50)

    def paintEvent(self,event):
        #初始化绘图工具
        qp=QPainter()
        #开始在窗口绘制
        qp.begin(self)
        #自定义绘制方法
        self.drawCircle(qp)
        #结束在窗口的绘制
        qp.end()

    def drawCircle(self,qp):
        global if_drawing
        qp.setRenderHint(qp.Antialiasing)
        qp.fillPath(self.frame_path,QColor(231,234,251))
        qp.drawPath(self.frame_path)
        if(global_points_list==None):
            cover=QPixmap('./src/main/python/1.png')
            qp.drawPixmap(275,125,cover)
        elif(global_points_list==[]):
            cover=QPixmap('./src/main/python/1.png')
            cover=cover.scaled(QSize(200,200))
            qp.drawPixmap(275,125,cover)
        else:
        # qp.setPen(QPen(QColor(0, 160, 230), 10));
        # QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # qp.setPen(QPen(QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 2, Qt.DashDotLine))
        # qp.setPen(QPen(Qt.black, 2, Qt.DashDotLine))
        # qp.setPen(pen)
           if(if_drawing==1):
                for i, j in global_points_list:
                    qp.setPen(QPen(QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 10, Qt.DashDotLine))
                    qp.drawLine(i[0] * 800, i[1] * 450, j[0] * 800, j[1] * 450)


def qualified(x,y):
    if( 0.05<x<0.95 and 0.05<y<0.95):
        return True
    else:
        return False

def start_openpose():
    os.system("start /min cmd /k start1.bat")

def start_openpose_upload():
    os.system("start /min cmd /k start2.bat")

folder1 = './json1'
folder2 = './json2'

#清除json文件
def clear_cache():
    for the_file in os.listdir(folder1):
        file_path = os.path.join(folder1, the_file)
        os.remove(file_path)
    for the_file in os.listdir(folder2):
        file_path = os.path.join(folder2, the_file)
        os.remove(file_path)

class MainWindow(QMainWindow):
    #界面设置
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # 设置窗口名称
        self.setWindowTitle("基于openpose的静态健身教练系统")
        
        # 设置状态栏
        # self.status = self.statusBar()
        # self.status.showMessage("ZJUTDevelpoers")

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
        label1.setText("菜单")
        label1.setAlignment( Qt.AlignCenter) #设置居中
        label1.setFont(QFont("Century",40,QFont.Bold))
        button_layout.addWidget(label1)

  
        pe = QPalette()
        pe.setColor(QPalette.WindowText,QColor(139,147, 194, 250))
        label1.setPalette(pe)

        # 声音 按钮
        self.voice_btn = QPushButton("打开声音")
        self.voice_btn.setFixedSize(200, 60)
        self.voice_btn.setStyleSheet('''QPushButton{background:rgb(6,8,200);border-radius:5px;color:white;font-family:AdobeHeitiStd;font-size:25px}
                                        QPushButton:hover{background:rgb(106,118,200);}
                                        QPushButton:pressed{background-color:rgb(106,118,200)}''')
        button_layout.addWidget(self.voice_btn)
        self.voice_btn.clicked.connect(self._voice)
        # 火柴人显示 按钮
        self.show_btn = QPushButton("开启回显")
        self.show_btn.setFixedSize(200, 60)
        self.show_btn.setStyleSheet('''QPushButton{background:rgb(6,8,200);border-radius:5px;color:white;font-family:AdobeHeitiStd;font-size:25px}
                                        QPushButton:hover{background:rgb(106,118,200);}
                                        QPushButton:pressed{background-color:rgb(106,118,200)}''')
        button_layout.addWidget(self.show_btn)
        self.show_btn.clicked.connect(self._show)
        # 计时 按钮
        self.time_btn = QPushButton("设定运动时间")
        self.time_btn.setFixedSize(200, 60)
        self.time_btn.setStyleSheet('''QPushButton{background:rgb(6,8,200);border-radius:5px;color:white;font-family:AdobeHeitiStd;font-size:25px}
                                        QPushButton:hover{background:rgb(106,118,200);}
                                        QPushButton:pressed{background-color:rgb(106,118,200)}''')
        button_layout.addWidget(self.time_btn)
        self.time_btn.clicked.connect(self._set_time)
        # 关于 按钮
        self.about_btn = QPushButton("关于")
        self.about_btn.setFixedSize(200, 60)
        self.about_btn.setStyleSheet('''QPushButton{background:rgb(6,8,200);border-radius:5px;color:white;font-family:AdobeHeitiStd;font-size:25px}
                                        QPushButton:hover{background:rgb(106,118,200);}
                                        QPushButton:pressed{background-color:rgb(106,118,200)}''')
        button_layout.addWidget(self.about_btn)
        self.about_btn.clicked.connect(self._about)
        # 退出 按钮
        self.quit_btn = QPushButton(top_left_frame)
        self.quit_btn.setFixedSize(200, 60), self.quit_btn.setText("退出")
        self.quit_btn.setStyleSheet('''QPushButton{background:rgb(6,8,200);border-radius:5px;color:white;font-family:AdobeHeitiStd;font-size:25px}
                                        QPushButton:hover{background:rgb(106,118,200);}
                                        QPushButton:pressed{background-color:rgb(106,118,200)}''')
        button_layout.addWidget(self.quit_btn)
        self.quit_btn.clicked.connect(self._quit)



        self.chose_action_btn=QComboBox()
        self.chose_action_btn.setEditable(True)
        self.chose_action_btn.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.chose_action_btn.addItem('平板支撑')
        self.chose_action_btn.addItem('俄式挺身')
        self.chose_action_btn.addItem('马步')
        # self.chose_action_btn.addItem('其他动作')
        self.chose_action_btn.setFixedSize(200,60)
        self.chose_action_btn.setStyleSheet('''QComboBox{background:rgb(6,8,200);border-radius:5px;color:white;font-family:AdobeHeitiStd;font-size:25px}
                                        QComboBox:hover{background:rgb(106,118,200);}
                                        QComboBox:pressed{background-color:rgb(106,118,200)}''')
        self.chose_action_btn.currentIndexChanged.connect(self.now_action_is)
        button_layout.addWidget(self.chose_action_btn)
        



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

        right_button = QHBoxLayout()

        #开始检测  按钮
        self.start_btn = QPushButton("开始检测")
        self.start_btn.setStyleSheet('''QPushButton{background:rgb(106,118,200);border-radius:5px;color:white;font-family:AdobeHeitiStd;font-size:25px}
                                        QPushButton:hover{background:rgb(106,118,200);}
                                        QPushButton:pressed{background-color:rgb(106,118,200)}''')
        self.start_btn.setFixedSize(150, 45)
        self.start_btn.clicked.connect(self._start)
        right_button.addWidget(self.start_btn)  

        # 输入文件 按钮
        self.upload_btn = QPushButton("输入文件")
        self.upload_btn.setStyleSheet('''QPushButton{background:rgb(106,118,200);border-radius:5px;color:white;font-family:AdobeHeitiStd;font-size:25px}
                                        QPushButton:hover{background:rgb(106,118,200);}
                                        QPushButton:pressed{background-color:rgb(180,180,180)}''')
        self.upload_btn.setFixedSize(150, 45)
        self.upload_btn.clicked.connect(self._upload)
        right_button.addWidget(self.upload_btn)
        
        #停止检测  按钮
        self.end_btn = QPushButton("停止检测")
        self.end_btn.setStyleSheet('''QPushButton{background:rgb(106,118,200);border-radius:5px;color:white;font-family:AdobeHeitiStd;font-size:25px}
                                        QPushButton:hover{background:rgb(106,118,200);}
                                        QPushButton:pressed{background-color:rgb(106,118,200)}''')
        self.end_btn.setFixedSize(150, 45)
        right_button.addWidget(self.end_btn)
        self.end_btn.clicked.connect(self.end_check)
        

        self.right_label=DrawCircle()
        self.right_label.setFixedSize(700,500)
        
        self.right_label.setStyleSheet("QWidget{background-color :rgb(231,234,251);border-radius: 30px;border-style: outset;border-width: 2px;border-color: bule;color:white}")
        #self.right_label.setAlignment(Qt.AlignCenter)


        
        self.right_label2=QLabel()
        self.right_label2.setText("检测未开始")
        self.right_label2.setFixedSize(500,60)
        self.right_label2.setStyleSheet("QLabel{background-color :rgb(231,234,251);border-radius: 15px;border-style: outset;border-width: 2px;border-color: bule;color:black}")
        #self.right_label2.setAlignment(Qt.AlignCenter)
        self.right_label2.setAlignment(Qt.AlignCenter) 
        self.right_label2.setFont(QFont("隶书",50, QFont.Bold) )

        pe = QPalette()
        #pe.setColor(QPalette.WindowText,Qt.red)
        #self.right_label2.setAutoFillBackground(True)
        pe.setColor(QPalette.Window,Qt.black)
        self.right_label2.setPalette(pe)

        right_top_widget = QHBoxLayout()
        right_top_widget.addWidget(self.right_label2)
        right_top_label2_widget = QWidget()
        right_top_label2_widget.setLayout(right_top_widget)
        


        self.remain_time_label=QLabel()
        self.remain_time_label.setText("距离本次运动结束还有0s")
        self.remain_time_label.setFixedSize(500,40)
        self.remain_time_label.setStyleSheet("QLabel{background-color :rgb(231,234,251);border-radius: 15px;border-style: outset;border-width: 2px;border-color: bule;color:black}")
        #self.right_label2.setAlignment(Qt.AlignCenter)
        self.remain_time_label.setAlignment(Qt.AlignCenter) 
        self.remain_time_label.setFont(QFont("隶书",30, QFont.Bold) )
        
        remain_time_widget = QHBoxLayout()
        remain_time_widget.addWidget(self.remain_time_label)
        remain_time_widget2 = QWidget()
        remain_time_widget2.setLayout(remain_time_widget)

        #添加按钮布局和right_label布局
        right_btn_widget = QWidget()
        right_btn_widget.setLayout(right_button)
        self.right_layout.addWidget(right_top_label2_widget)
        self.right_layout.addWidget(self.right_label)
        self.right_layout.addWidget(remain_time_widget2)   
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
        
        self.show_button_checked=0 #控制show按钮开关的两种状态
        self.voice_button_checked=0 #控制voice按钮开关的两种状态
        self.time_button_checked=0
        self.time_seted=0
        self.first_judge=0  #用于计时时判断是否是第一次遇到标准
        self.now_action="平板支撑"
        clear_cache()

    def judge1(self):
        global global_points_list
        global_points_list=[]
        jsonlist=os.listdir(folder1)
        count1,count2=0.0,0.0
        chosedfile=max(jsonlist)

        with open(folder1 + '\\' + chosedfile, 'r') as jsonfile:
            data = json.load(jsonfile)
        
        if(len(data['people'])==0):
            return("未检测到人体")
        '''
        平板支撑
        '''
        if(self.now_action=='平板支撑'):
            #print('平板支撑')
            key_point_array = data['people'][0]['pose_keypoints_2d']
            midhipx, midhipy = key_point_array[8 * 3], key_point_array[8 * 3 + 1]
            Rkneex, Rkneey = key_point_array[10 * 3], key_point_array[10 * 3 + 1]
            Neckx, Necky = key_point_array[1 * 3], key_point_array[1 * 3 + 1]
            Nosex, Nosey = key_point_array[0], key_point_array[1]
            RHeelx, RHeely = key_point_array[24 * 3], key_point_array[24 * 3 + 1]
            REarx, REary =  key_point_array[17 * 3], key_point_array[17 * 3 + 1]
            
    
            for i, j in [(0,1),(1,8),(8,10),(10,11),(11,22),(2,3),(3,4)]:
                if (qualified(key_point_array[3 * i], key_point_array[3 * i + 1]) and qualified(key_point_array[3 * j],key_point_array[3 * j + 1])):
                    global_points_list.append([(key_point_array[3 * i], key_point_array[3 * i + 1]),(key_point_array[3 * j], key_point_array[3 * j + 1])])
    
            if (((Neckx - Nosex)!=0) and ((midhipx - Rkneex)!=0) and ((midhipx - RHeelx)!=0) and (midhipy - RHeely)!=0):
                # k_1_2 = (Necky - Nosey) / (Neckx - Nosex)
                # k_1_3 = (Nosey - midhipy) / (Nosex - midhipx)
                k_1_2 = (Necky - REary) / (Neckx - REarx)
                k_1_3 = (REary - midhipy) / (REarx - midhipx)
                k_2_3 = (Necky - midhipy) / (Neckx - midhipx)
                k_3_4 = (midhipy - Rkneey) / (midhipx - Rkneex)
                k_3_5 = (midhipy - RHeely) / (midhipx - RHeelx)
                #print(k_2_3, "  ", k_3_4, "    ", abs(k_2_3 / k_3_4))
                if (1.2 > abs(k_2_3 / k_3_4) > 0.4):
                    #print(k,"   ",chosedfile,"标准")
                    return("标准")
                else:
                    #print(k,"   ",chosedfile,"不标准")
                    return("不标准")
            #print(count1,count2,count1/count2)
            else:
                return("图像不完整")
        '''
        马步
        '''
        if(self.now_action=='马步'):
            #print("马步")
            key_point_array = data['people'][0]['pose_keypoints_2d']
            midhipx, midhipy = key_point_array[8 * 3], key_point_array[8 * 3 + 1]
            Lkneex, Lkneey = key_point_array[13 * 3], key_point_array[13 * 3 + 1]
            Neckx, Necky = key_point_array[1 * 3], key_point_array[1 * 3 + 1]
            Nosex, Nosey = key_point_array[0], key_point_array[1]
            Lfootx, Lfooty = key_point_array[21 * 3], key_point_array[21 * 3 + 1]
            Lwristx, Lwristy =  key_point_array[7 * 3], key_point_array[7 * 3 + 1]
            Lshoulderx, Lshouldery =  key_point_array[5 * 3], key_point_array[5 * 3 + 1]
            Lhipx, Lhipy = key_point_array[12 * 3], key_point_array[12 * 3 + 1]
            
            
            for i, j in [(0,1),(1,8),(9,10),(10,11),(11,22),(2,3),(3,4)]:  # [(18,1),(1,8),(12,13),(13,14),(14,19),(5,6),(6,7)]
                if (qualified(key_point_array[3 * i], key_point_array[3 * i + 1]) and qualified(key_point_array[3 * j],key_point_array[3 * j + 1])):
                    global_points_list.append([(key_point_array[3 * i], key_point_array[3 * i + 1]),(key_point_array[3 * j], key_point_array[3 * j + 1])])
            
            if (((Neckx - Nosex)!=0) and ((midhipx - Lkneex)!=0) and ((midhipx - Lfootx)!=0) and (midhipy - Lfooty)!=0):
                v_0_1 = np.array([(Nosex - Neckx), (Nosey - Necky)])
                v_1_8 = np.array([(Neckx - midhipx), (Necky - midhipy)])
                v_5_7 = np.array([(Lshoulderx - Lwristx), (Lshouldery - Lwristy)])
                v_13_12 = np.array([(Lkneex - Lhipx), (Lkneey - Lhipy)])
                v_13_14 = np.array([(Lkneex - Lfootx), (Lkneey - Lfooty)])
            
                degree_1 = degree_count(v_1_8, v_5_7)
                degree_2 = degree_count(v_1_8, v_13_12)
                degree_3 = degree_count(v_13_12, v_13_14)
                print("degree_1=", degree_1)
                print("degree_2=", degree_2)
                print("degree_3=", degree_3)
            
                if (degree_1 > 100 and 115 > degree_2 > 80 and 125 > degree_2 > 90):
                    print("标准")
                else:
                    print("不标准")
            #print(count1,count2,count1/count2)
            else:
                print("图像不完整")
 

        '''
        俄挺
        '''
        if(self.now_action=='俄式挺身'):
            #print("俄挺")
            key_point_array = data['people'][0]['pose_keypoints_2d']
            midhipx, midhipy = key_point_array[8 * 3], key_point_array[8 * 3 + 1]
            Lkneex, Lkneey = key_point_array[13 * 3], key_point_array[13 * 3 + 1]
            Neckx, Necky = key_point_array[1 * 3], key_point_array[1 * 3 + 1]
            Nosex, Nosey = key_point_array[0], key_point_array[1]
            LEarx, LEary = key_point_array[18 * 3], key_point_array[18 * 3]
            Lfootx, Lfooty = key_point_array[21 * 3], key_point_array[21 * 3 + 1]
            Lwristx, Lwristy =  key_point_array[7 * 3], key_point_array[7 * 3 + 1]
            Lshoulderx, Lshouldery =  key_point_array[5 * 3], key_point_array[5 * 3 + 1]
            Lhipx, Lhipy = key_point_array[12 * 3], key_point_array[12 * 3 + 1]
            
            
            for i, j in [(0,1),(1,8),(9,10),(10,11),(11,22),(2,3),(3,4)]:  # [(18,1),(1,8),(12,13),(13,14),(14,19),(5,6),(6,7)]
                if (qualified(key_point_array[3 * i], key_point_array[3 * i + 1]) and qualified(key_point_array[3 * j],key_point_array[3 * j + 1])):
                    global_points_list.append([(key_point_array[3 * i], key_point_array[3 * i + 1]),(key_point_array[3 * j], key_point_array[3 * j + 1])])
            
            if (((Neckx - Nosex)!=0) and ((midhipx - Lkneex)!=0) and ((midhipx - Lfootx)!=0) and (midhipy - Lfooty)!=0):
                v_0_1 = np.array([(Nosex - Neckx), (Nosey - Necky)])
                v_1_8 = np.array([(Neckx - midhipx), (Necky - midhipy)])
                v_5_7 = np.array([(Lshoulderx - Lwristx), (Lshouldery - Lwristy)])
                v_13_12 = np.array([(Lkneex - Lhipx), (Lkneey - Lhipy)])
                v_13_14 = np.array([(Lkneex - Lfootx), (Lkneey - Lfooty)])
            
                degree_1 = degree_count(v_1_8, v_5_7)
                degree_2 = degree_count(v_1_8, v_13_12)
                degree_3 = degree_count(v_13_12, v_13_14)
                print("degree_1=", degree_1)
                print("degree_2=", degree_2)
                print("degree_3=", degree_3)
            
                if (80 > degree_1 > 40 and degree_2 > 160 and degree_2 > 160 and Lwristy > Lshouldery):
                    print("标准")
                else:
                    print("不标准")
            #print(count1,count2,count1/count2)
            else:
                print("图像不完整")       
    
    
    def judge2(self):
        global global_points_list
        global_points_list=[]
        jsonlist=os.listdir(folder2)
        count1,count2=0.0,0.0
        chosedfile=max(jsonlist)


        with open(folder2 + '\\' + chosedfile, 'r') as jsonfile:
            data = json.load(jsonfile)
        
        if(len(data['people'])==0):
            return("未检测到人体")
        '''
        平板支撑
        '''
        if(self.now_action=='平板支撑'):
            #print('平板支撑')
            key_point_array = data['people'][0]['pose_keypoints_2d']
            midhipx, midhipy = key_point_array[8 * 3], key_point_array[8 * 3 + 1]
            Rkneex, Rkneey = key_point_array[10 * 3], key_point_array[10 * 3 + 1]
            Neckx, Necky = key_point_array[1 * 3], key_point_array[1 * 3 + 1]
            Nosex, Nosey = key_point_array[0], key_point_array[1]
            RHeelx, RHeely = key_point_array[24 * 3], key_point_array[24 * 3 + 1]
            REarx, REary =  key_point_array[17 * 3], key_point_array[17 * 3 + 1]
            
    
            for i, j in [(0,1),(1,8),(8,10),(10,11),(11,22),(2,3),(3,4)]:
                if (qualified(key_point_array[3 * i], key_point_array[3 * i + 1]) and qualified(key_point_array[3 * j],key_point_array[3 * j + 1])):
                    global_points_list.append([(key_point_array[3 * i], key_point_array[3 * i + 1]),(key_point_array[3 * j], key_point_array[3 * j + 1])])
    
            if (((Neckx - Nosex)!=0) and ((midhipx - Rkneex)!=0) and ((midhipx - RHeelx)!=0) and (midhipy - RHeely)!=0):
                # k_1_2 = (Necky - Nosey) / (Neckx - Nosex)
                # k_1_3 = (Nosey - midhipy) / (Nosex - midhipx)
                k_1_2 = (Necky - REary) / (Neckx - REarx)
                k_1_3 = (REary - midhipy) / (REarx - midhipx)
                k_2_3 = (Necky - midhipy) / (Neckx - midhipx)
                k_3_4 = (midhipy - Rkneey) / (midhipx - Rkneex)
                k_3_5 = (midhipy - RHeely) / (midhipx - RHeelx)
                #print(k_2_3, "  ", k_3_4, "    ", abs(k_2_3 / k_3_4))
                if (1.2 > abs(k_2_3 / k_3_4) > 0.4):
                    #print(k,"   ",chosedfile,"标准")
                    return("标准")
                else:
                    #print(k,"   ",chosedfile,"不标准")
                    return("不标准")
            #print(count1,count2,count1/count2)
            else:
                return("图像不完整")
        '''
        马步
        '''
        if(self.now_action=='马步'):
            # print("马步")
            key_point_array = data['people'][0]['pose_keypoints_2d']
            midhipx, midhipy = key_point_array[8 * 3], key_point_array[8 * 3 + 1]
            Lkneex, Lkneey = key_point_array[13 * 3], key_point_array[13 * 3 + 1]
            Neckx, Necky = key_point_array[1 * 3], key_point_array[1 * 3 + 1]
            Nosex, Nosey = key_point_array[0], key_point_array[1]
            Lfootx, Lfooty = key_point_array[21 * 3], key_point_array[21 * 3 + 1]
            Lwristx, Lwristy =  key_point_array[7 * 3], key_point_array[7 * 3 + 1]
            Lshoulderx, Lshouldery =  key_point_array[5 * 3], key_point_array[5 * 3 + 1]
            Lhipx, Lhipy = key_point_array[12 * 3], key_point_array[12 * 3 + 1]
            
            
            for i, j in [(0,1),(1,8),(9,10),(10,11),(11,22),(2,3),(3,4)]:  # [(18,1),(1,8),(12,13),(13,14),(14,19),(5,6),(6,7)]
                if (qualified(key_point_array[3 * i], key_point_array[3 * i + 1]) and qualified(key_point_array[3 * j],key_point_array[3 * j + 1])):
                    global_points_list.append([(key_point_array[3 * i], key_point_array[3 * i + 1]),(key_point_array[3 * j], key_point_array[3 * j + 1])])
            
            if (((Neckx - Nosex)!=0) and ((midhipx - Lkneex)!=0) and ((midhipx - Lfootx)!=0) and (midhipy - Lfooty)!=0):
                v_0_1 = np.array([(Nosex - Neckx), (Nosey - Necky)])
                v_1_8 = np.array([(Neckx - midhipx), (Necky - midhipy)])
                v_5_7 = np.array([(Lshoulderx - Lwristx), (Lshouldery - Lwristy)])
                v_13_12 = np.array([(Lkneex - Lhipx), (Lkneey - Lhipy)])
                v_13_14 = np.array([(Lkneex - Lfootx), (Lkneey - Lfooty)])
            
                degree_1 = degree_count(v_1_8, v_5_7)
                degree_2 = degree_count(v_1_8, v_13_12)
                degree_3 = degree_count(v_13_12, v_13_14)
                # print("degree_1=", degree_1)
                # print("degree_2=", degree_2)
                # print("degree_3=", degree_3)
            
                if (degree_1 > 90 and 120 > degree_2 > 80 and 125 > degree_2 > 90):
                    return ("标准")
                else:
                    return("不标准")
            #print(count1,count2,count1/count2)
            else:
                return("图像不完整")
 

        '''
        俄挺
        '''
        if(self.now_action=='俄式挺身'):
            # print("俄挺")
            key_point_array = data['people'][0]['pose_keypoints_2d']
            midhipx, midhipy = key_point_array[8 * 3], key_point_array[8 * 3 + 1]
            Lkneex, Lkneey = key_point_array[13 * 3], key_point_array[13 * 3 + 1]
            Neckx, Necky = key_point_array[1 * 3], key_point_array[1 * 3 + 1]
            Nosex, Nosey = key_point_array[0], key_point_array[1]
            LEarx, LEary = key_point_array[18 * 3], key_point_array[18 * 3]
            Lfootx, Lfooty = key_point_array[21 * 3], key_point_array[21 * 3 + 1]
            Lwristx, Lwristy =  key_point_array[7 * 3], key_point_array[7 * 3 + 1]
            Lshoulderx, Lshouldery =  key_point_array[5 * 3], key_point_array[5 * 3 + 1]
            Lhipx, Lhipy = key_point_array[12 * 3], key_point_array[12 * 3 + 1]
            
            
            for i, j in [(0,1),(1,8),(9,10),(10,11),(11,22),(2,3),(3,4)]:  # [(18,1),(1,8),(12,13),(13,14),(14,19),(5,6),(6,7)]
                if (qualified(key_point_array[3 * i], key_point_array[3 * i + 1]) and qualified(key_point_array[3 * j],key_point_array[3 * j + 1])):
                    global_points_list.append([(key_point_array[3 * i], key_point_array[3 * i + 1]),(key_point_array[3 * j], key_point_array[3 * j + 1])])
            
            if (((Neckx - Nosex)!=0) and ((midhipx - Lkneex)!=0) and ((midhipx - Lfootx)!=0) and (midhipy - Lfooty)!=0):
                v_0_1 = np.array([(Nosex - Neckx), (Nosey - Necky)])
                v_1_8 = np.array([(Neckx - midhipx), (Necky - midhipy)])
                v_5_7 = np.array([(Lshoulderx - Lwristx), (Lshouldery - Lwristy)])
                v_13_12 = np.array([(Lkneex - Lhipx), (Lkneey - Lhipy)])
                v_13_14 = np.array([(Lkneex - Lfootx), (Lkneey - Lfooty)])
            
                degree_1 = degree_count(v_1_8, v_5_7)
                degree_2 = degree_count(v_1_8, v_13_12)
                degree_3 = degree_count(v_13_12, v_13_14)
                # print("degree_1=", degree_1)
                # print("degree_2=", degree_2)
                # print("degree_3=", degree_3)
            
                if (80 > degree_1 > 40 and degree_2 > 160 and degree_2 > 160 and Lwristy > Lshouldery):
                    return ("标准")
                else:
                    return ("不标准")
            #print(count1,count2,count1/count2)
            else:
                return ("图像不完整")
    


    def center(self):
        #获取桌面长宽  获取窗口长宽 计算位置 移动
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


    def running1(self):
        self.right_label2.setText(self.judge1())
        if(self.time_button_checked==1):
            if(self.judge1()=="标准"):
                if(self.first_judge==0):
                    self.time_start = time.time()
                    self.first_judge=1
                else:
                    now_time=time.time()
                    if((self.time_seted-(now_time-self.time_start))<=0):
                        self.remain_time_label.setText("本次运动达标!!!")
                        if(self.voice_button_checked==1):
                            engine.say("本次运动达标")
                            engine.runAndWait()
                        self.time_button_checked=0
                        self.first_judge=0
                        self.time_btn.setText("重新设定时间")
                    elif((self.time_seted-(now_time-self.time_start))==10):
                        if(self.voice_button_checked==1):
                            engine.say("加油！还有十秒钟")
                            engine.runAndWait()           
                    else:
                        #控制输出剩余运动时间
                        self.remain_time_label.setText("距离本次运动结束还有"+str(round((self.time_seted-(now_time-self.time_start)),1))+"s")
            else:
                if(self.first_judge==0):
                    pass
                else:
                    self.first_judge=0
        if(self.show_button_checked==1):
            self.right_label.update()


    def running2(self):
        self.right_label2.setText(self.judge2())
        if(self.time_button_checked==1):
            if(self.judge2()=="标准"):
                if(self.first_judge==0):
                    self.time_start = time.time()
                    self.first_judge=1
                else:
                    now_time=time.time()
                    if((self.time_seted-(now_time-self.time_start))<=0):
                        self.remain_time_label.setText("本次运动达标!!!")
                        if(self.voice_button_checked==1):
                            engine.say("本次运动达标")
                            engine.runAndWait()
                        self.time_button_checked=0
                        self.first_judge=0
                        self.time_btn.setText("重新设定时间")
                    elif((self.time_seted-(now_time-self.time_start))==10):
                        if(self.voice_button_checked==1):
                            engine.say("加油！还有十秒钟")
                            engine.runAndWait()
                    else:
                        #控制输出剩余运动时间
                        self.remain_time_label.setText("距离本次运动结束还有"+str(round((self.time_seted-(now_time-self.time_start)),1))+"s")
            else:
                if(self.first_judge==0):
                    pass
                else:
                    self.first_judge=0
        if(self.show_button_checked==1):
            self.right_label.update()
    

    def now_action_is(self):
        self.now_action=self.chose_action_btn.currentText()
        print(self.now_action)
        

    def _start(self):
        start_openpose()
        wndtitle = 'OpenPose 1.5.1'
        wndclass = None
        time.sleep(3)
        while True:
            wnd=win32gui.FindWindow(wndclass, wndtitle)
            if(wnd!=0):          
                #win32gui.SetParent(wnd, int(self.right_label.winId()))
                #实现将win32gui嵌入right_label_new 将right_label_new嵌入right_label
                #self.right_label_new= QWindow.fromWinId(wnd)
                ##self.right_label_new.setStyleSheet("QWidow{border-radius: 30px;border-style: outset;border-width: 2px;border-color: bule;color:white}")
                #self.right_label_new.createWindowContainer(self.right_label, self)
                #self.right_label_new.setWidth(300)
                #self.right_label_new.setHeight(700)
                #self.right_label_new.show()

                win32gui.ShowWindow(win32gui.FindWindow(wndclass, wndtitle), win32con.SW_MINIMIZE)
                self.running_timer = QTimer(self)
                self.running_timer.timeout.connect(self.running1)
                self.running_timer.start(30)
                break
        

    def _upload(self):
        videoName, _ = QFileDialog.getOpenFileName(self, "Open", "", "*.avi *.mp4 *.gif;;All Files(*)")#限定文件格式
        print(videoName)#返回文件位置

        '''
        #实现播放导入文件功能
        self.right_label.setPixmap(QPixmap(videoName))
        self.right_label.setScaledContents(True)
        movie = QMovie(videoName)
        self.right_label.setMovie(movie)
        movie.start()
        '''
        if videoName != "":  # “”为用户取消

            f = open('start2.bat', mode='w',encoding='utf-8')
            f.write("title running_openpose\n")
            f.write("cd .\openpose\n")
            f.write(".\\bin\OpenPoseDemo.exe --video "+videoName+" --net_resolution 320x176 --number_people_max 1 --tracking 7 --write_json ..\json2 --keypoint_scale 3 --frame_flip true")                         
            f.close()

            start_openpose_upload()
            wndtitle = 'OpenPose 1.5.1'
            wndclass = None
            time.sleep(3)
            while True:
                wnd=win32gui.FindWindow(wndclass, wndtitle)
				
                if(wnd!=0):
                    win32gui.ShowWindow(win32gui.FindWindow(wndclass, wndtitle), win32con.SW_MINIMIZE)
                    self.running_timer = QTimer(self)
                    self.running_timer.timeout.connect(self.running2)
                    self.running_timer.start(30)
                    break
    

    def _set_time(self):
        if(self.time_button_checked==1):
            self.time_btn.setText("重新设定时间")
            self.time_button_checked=0
        else:
            #参考链接 https://www.cnblogs.com/linyfeng/p/11223711.html           
            dialog = QInputDialog(self)
            font = QFont()
            font.setFamily("Arial")
            font.setPointSize(24)
            dialog.setInputMode(QInputDialog.TextInput)
            dialog.setWindowTitle('计时时间设定')
            dialog.setLabelText('请输入运动时间(秒):')
            dialog.setFont(font)
            dialog.setOkButtonText("确定")
            dialog.setCancelButtonText("取消")
            dialog.resize(500,300)
            # num,ok = dialog.getInt(None, "计时时间设定", "请输入运动时间(s)", 10)
            ok = dialog.exec_()                                
            num = float(dialog.textValue())
            if ok and num:
                self.time_seted=num
                self.remain_time_label.setText("距离本次运动结束还有"+str(self.time_seted)+"s")
                self.time_btn.setText("已开始计时")
                self.time_button_checked=1
            else:
                self.time_seted=10
                self.remain_time_label.setText("距离本次运动结束还有"+str(self.time_seted)+"s")
                self.time_btn.setText("已开始计时")
                self.time_button_checked=1

    def _voice(self):
        if(self.voice_button_checked==1):
            self.voice_btn.setText("打开声音")
            self.voice_button_checked=0
        else:
            self.voice_btn.setText("关闭声音")
            self.voice_button_checked=1

    def _show(self):
        global if_drawing
        if (self.show_button_checked==1):
            self.show_btn.setText("回显已关闭")
            #self.drawing=DrawCircle()
            #self.right_label.createWindowContainer(self.drawing, self)
            self.show_button_checked=0
            if_drawing=0
        else:
            self.show_btn.setText("回显已开启")
            self.show_button_checked=1
            if_drawing=1
            


    def _about(self):
        QMessageBox.about(self,"基于openpose的静态健身教练系统","浙江工业大学") 


    def end_check(self):
        #os.system('TASKKILL /F /T /FI "WINDOWTITLE eq running_openpose*"')
        os.system('TASKKILL /F /T /FI "imagename eq OpenPoseDemo.exe"')
        

    def _quit(self):
        os.system('TASKKILL /F /T /FI "imagename eq OpenPoseDemo.exe"') #参考链接 https://blog.csdn.net/qq_36011182/article/details/80252170
        clear_cache()
        self.close()

if __name__ == "__main__":
    App= ApplicationContext()
    App.app.setStyle('Fusion')
    my_gui= MainWindow()
    #win=cure.Windows(gui(),'name',True)##实现对窗口的美化
    my_gui.show()
    sys.exit(App.app.exec_())
