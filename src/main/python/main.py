from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os

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
#global_points_list=[[(0,0),(50,50)],[(0,50),(50,50)]]

def start_openpose():
    os.system("start /min cmd /k C:\\Users\\Hp\\Desktop\\standardmotion\\standardmotion\\src\\main\\python\\start.bat")


folder = 'C:\\Users\\Hp\\Desktop\\standardmotion\\standardmotion\\src\\main\\python\\json'

#清除原有json文件
def clear_cache():
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        os.remove(file_path)




def qualified(x,y):
    if( 0.12<x<0.88 and 0.12<y<0.88):
        return True
    else:
        return False

reader=pyttsx3.init()


def no():
    try:
        reader.say("姿势不标准")
        reader.runAndWait()
    except RuntimeError as rt:
        reader.endLoop()
        reader.say("不标准")
        reader.runAndWait()



class DrawCircle(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setFixedSize(800,450)
        self.frame_path=QPainterPath()
        self.frame_path.addRoundedRect(QRectF(800*0.12,450*0.12,600,350),50,50)

    def paintEvent(self,event):
        qp = QPainter(self)
        qp.setPen(QPen(Qt.blue,5,Qt.SolidLine))
        qp.begin(self)
        self.paint(qp)
        qp.end()

    def paint(self,qp):
        qp.setRenderHint(qp.Antialiasing)
        qp.fillPath(self.frame_path,QColor(204,204,255))
        qp.drawPath(self.frame_path)
        if(global_points_list==None):
            cover=QPixmap('./image/sitting_ico.png')
            qp.drawPixmap(120,0,cover)
        elif(global_points_list==[]):
            cover=QPixmap('./image/danger.png')
            cover=cover.scaled(QSize(200,200))
            qp.drawPixmap(300,135,cover)
        else:
            qp.setPen(QPen(Qt.black,10,Qt.DashDotLine))
            for i,j in global_points_list:
                qp.drawLine(i[0]*800,i[1]*450,j[0]*800,j[1]*450)



class gui(QDialog):
    def __init__(self, parent=None):
        super(gui, self).__init__(parent)
        #self.resize(1200, 800)
        self.setFixedSize(1500, 800)
        self.tabs=QTabWidget()
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.palette = QPalette()
        #self.palette.setBrush(QPalette.Background, QBrush(QPixmap('background1.jpg')))
        #self.setPalette(self.palette)#初始化窗口并设置背景图片
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap('./image/background3.jpg')))
        self.setPalette(self.palette)
        self.tabs.setFont(QFont("楷体", 20, QFont.Bold) )
        self.crFTab()
        self.tabs.addTab(self.FTab,'功能')
        mainlayout=QGridLayout()
        mainlayout.addWidget(self.tabs,0,0)
        self.setLayout(mainlayout)
        self.setWindowTitle("标准坐姿检测")

        self.voice_cache=None
        self.current_status=0
        clear_cache()
        cache_timer = QTimer(self)
        cache_timer.timeout.connect(clear_cache)
        cache_timer.start(10000)
        t = threading.Thread(target=self.prepare)
        t.setDaemon(True)
        t.start()

    def prepare(self):
        start_openpose()
        wndtitle = 'OpenPose 1.5.1'
        wndclass = None
        while True:
            wnd=win32gui.FindWindow(wndclass, wndtitle)
            if(wnd!=0):
                win32gui.ShowWindow(win32gui.FindWindow(wndclass, wndtitle), win32con.SW_MINIMIZE)

                break
        while(True):
            if(len(os.listdir(folder))==0):
                global initialed
                initialed=True
                self.status.setText("程序未运行")
                break

    def crFTab(self):
        self.FTab=QWidget()
        Tablayout=QGridLayout()
        self.start_botton=QPushButton("开始检测")
        self.start_botton.setCheckable(True)
        self.start_botton.clicked.connect(self.start)
        #self.start_botton.clicked.connect(self.repaint)
        self.quit_button=QPushButton("退出程序")
        self.quit_button.setFlat(True)
        self.quit_button.clicked.connect(self._quit)
        self.start_botton.setFixedSize(200,80)
        self.start_botton.setFont(QFont("华文新魏",20))
        self.quit_button.setFixedSize(100,40)

        self.quit_button.setFont(QFont("华文新魏",15))
        self.coverlabel=QLabel()
        cover_pixmap = QPixmap('./image/cov.png')
        self.coverlabel.setPixmap(cover_pixmap)
        self.status=QLabel("正在初始化")##################################################
        self.status.setAlignment(Qt.AlignCenter)

        self.status.setStyleSheet("QLabel { background-color : white;border-radius: 30px;border-style: outset;\
    border-width: 2px;\
    border-color: bule;}")
        self.status.setFixedSize(700,160)
        self.status.setFont(QFont("隶书",35, QFont.Bold) )
        
        button_layout=QVBoxLayout()
    
        button_layout.addWidget(self.start_botton)
        button_layout.addWidget(self.quit_button,0,Qt.AlignCenter)
        self.pose_drawing=DrawCircle()
        #self.pose_drawing.setStyleSheet("background-color : white;")

        Tablayout.addLayout(button_layout,0,0,1,1,Qt.AlignCenter)
        Tablayout.addWidget(self.coverlabel,1,0,Qt.AlignCenter)
        Tablayout.addWidget(self.status,0,1,Qt.AlignCenter)
        Tablayout.addWidget(self.pose_drawing,1,1,Qt.AlignCenter)


        self.FTab.setLayout(Tablayout)
        palette=QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.FTab.setPalette(palette)

    def repaint(self):
        self.pose_drawing.setColor('green')

    def start(self):
        if(not initialed):
            self.start_botton.setChecked(False)
            warnning_message=QMessageBox()
            warnning_message.setText("程序尚未初始化")
            warnning_message.setIcon(QMessageBox.Warning)
            warnning_message.setWindowTitle("警告")
            warnning_message.setFont(QFont("微软雅黑", 20, QFont.Bold))
            warnning_message.exec()

        elif(self.start_botton.isChecked()):
            #self.CTab.setDisabled(True)
            self.CTabG_1.setDisabled(True)
            self.CTabG_2.setDisabled(True)
            self.start_botton.setText("停止检测")
            self.running_timer = QTimer(self)
            self.running_timer.timeout.connect(self.running)
            self.running_timer.start(30)
        else:
            #self.CTab.setEnabled(True)
            self.CTabG_1.setEnabled(True)
            self.CTabG_2.setEnabled(True)
            self.start_botton.setText("开始检测")
            self.running_timer.stop()
            self.current_status=0
            self.voice_cache=None
            self.status.setText("程序未运行")
            global global_points_list
            global_points_list=None
            self.pose_drawing.update()


    def running(self):

        self.status.setText(self.out())

        if(self.voice_on.isChecked()):
            if(self.status.text()=="不标准"):
                if(self.current_status==0):
                    self.voice_cache=time.time()
                    self.current_status=1
            else:
                if(self.current_status==1):
                    self.current_status=0
                    self.voice_cache=None
            
            if(self.voice_cache!=None and time.time()-self.voice_cache>=3.0):
                threading.Thread(target=no, daemon=True).start()
                self.voice_cache=time.time()

        if(self.scene_on.isChecked()):
            self.pose_drawing.update()
        
                    



    def _quit(self):
        os.system('TASKKILL /F /T /FI "WINDOWTITLE eq running_openpose*"')
        clear_cache()
        self.close()


    #def crFTabG(self):
    #    self.CTabG_4=QGroupBox("关于")
    #    self.CTabG_4.setFont(QFont("Times", 25, QFont.Bold) )
    #    temp_layout=QGridLayout()
    #
    #    self.CTabG_4.setLayout(temp_layout)      
    def _changebg(self):
        #self.changebg(self.bgcontroler.value())
        #print(self.bgcontroler.value())

        if(self.bgcontroler.value()>=344):
            self.changebg(4)
        else:
            for i,j in enumerate([(130,230),(230,266),(266,308),(308,344),(1,19),(19,53),(53,93),(93,130)]):
                if(self.bgcontroler.value()>=j[0] and self.bgcontroler.value()<j[1]):
                    self.changebg(i)
                    break

        

    def changebg(self,value):
        if(value==0):
            self.setPalette(QPalette())
        else:
            self.palette.setBrush(QPalette.Background, QBrush(QPixmap('./image/'+'background'+str(value)+'.jpg')))
            self.setPalette(self.palette)


    def out(self):
        if(self.scene_on.isChecked()):
            global global_points_list
            global_points_list=[]
            jsonlist=os.listdir(folder)
            if(len(jsonlist)==0):
                return ("开始监测")

            chosedfile=max(jsonlist)
            with open(folder+'\\'+chosedfile,'r') as jsonfile:
                    data = json.load(jsonfile)
            if(len(data['people'])==0):
                return("未检测到人体")


            key_point_array=data['people'][0]['pose_keypoints_2d']
            middlex,middley=key_point_array[3],key_point_array[4]
            leftx,lefty=key_point_array[6],key_point_array[7]
            rightx,righty=key_point_array[15],key_point_array[16]
            nosex,nosey=key_point_array[0],key_point_array[1]

            needed_points=[middlex,middley,leftx,lefty,rightx,righty,nosex,nosey]


            for i in range(0,7,2):
                if(not qualified(needed_points[i],needed_points[i+1])):
                    return("图像不完整")


            for i,j in [(0,1),(0,15),(0,16),(15,17),(16,18),(1,2),(1,5),(2,3),(3,4),(5,6),(6,7)]:
                    if(qualified(key_point_array[3*i],key_point_array[3*i+1]) and qualified(key_point_array[3*j],key_point_array[3*j+1])):
                        #global_points_list.append([( key_point_array[3*i]  ,  key_point_array[3*j]  ),(key_point_array[3*i+1],key_point_array[3*j+1])])
                        global_points_list.append([( key_point_array[3*i]  ,  key_point_array[3*i+1]  ),(key_point_array[3*j],key_point_array[3*j+1])])

            heady=nosey-middley
            headx=nosex-middlex
            if(headx!=0):
                if(abs(headx/heady)>0.13):
                    return("不标准")


            lsy,lsx=middley-lefty,middlex-leftx
            rsy,rsx=middley-righty,rightx-middlex
            lk=lsy/lsx
            rk=rsy/rsx


            if(not ((abs(lk)<0.25 and abs(rk)<0.25 and lk*rk>0) or (abs(lk)<0.1 and abs(rk)<0.1)) ):
                return("不标准")


            if(1.2>abs(lsx/rsx)>0.8 and abs(heady)>1.3*(abs(lsx)+abs(rsx))/2):
                return("标准")
            else:
                return("不标准")

        else:
            jsonlist=os.listdir(folder)
            if(len(jsonlist)==0):
                return ("开始监测")

            chosedfile=max(jsonlist)
            with open(folder+'\\'+chosedfile,'r') as jsonfile:
                    data = json.load(jsonfile)
            if(len(data['people'])==0):
                return("未检测到人体")


            key_point_array=data['people'][0]['pose_keypoints_2d']
            middlex,middley=key_point_array[3],key_point_array[4]
            leftx,lefty=key_point_array[6],key_point_array[7]
            rightx,righty=key_point_array[15],key_point_array[16]
            nosex,nosey=key_point_array[0],key_point_array[1]

            needed_points=[middlex,middley,leftx,lefty,rightx,righty,nosex,nosey]


            for i in range(0,7,2):
                if(not qualified(needed_points[i],needed_points[i+1])):
                    return("图像不完整")

            heady=nosey-middley
            headx=nosex-middlex
            if(headx!=0):
                if(abs(headx/heady)>0.13):
                    return("不标准")


            lsy,lsx=middley-lefty,middlex-leftx
            rsy,rsx=middley-righty,rightx-middlex
            lk=lsy/lsx
            rk=rsy/rsx


            if(not ((abs(lk)<0.25 and abs(rk)<0.25 and lk*rk>0) or (abs(lk)<0.1 and abs(rk)<0.1)) ):
                return("不标准")


            if(1.2>abs(lsx/rsx)>0.8 and abs(heady)>1.3*(abs(lsx)+abs(rsx))/2):
                return("标准")
            else:
                return("不标准")
    










appctxt = ApplicationContext()
appctxt.app.setStyle('Fusion')
gui_example= gui()
gui_example.show()
sys.exit(appctxt.app.exec_())
    