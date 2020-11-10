from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import *
import sys
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
#global_points_list=[[(0,0),(50,50)],[(0,50),(50,50)]]

def start_openpose():
    os.system("start /min cmd /k C:\\Users\\Hp\\Desktop\\standardmotion\\standardmotion\\src\\main\\python\\start.bat")


folder = 'C:\\Users\\Hp\\Desktop\\standardmotion\\standardmotion\\src\\main\\python\\json'

#清除原有json文件
def clear_cache():
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        os.remove(file_path)



#判断点是否被拍摄
def qualified(x,y):
    if( 0.12<x<0.88 and 0.12<y<0.88):
        return True
    else:
        return False

reader=pyttsx3.init()

#语音输出
def no():
    try:
        reader.say("姿势不标准")
        reader.runAndWait()
    except RuntimeError as rt:
        reader.endLoop()
        reader.say("不标准")
        reader.runAndWait()

#画小人
class DrawCircle(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setFixedSize(600,800)
        self.frame_path=QPainterPath()
        self.frame_path.addRoundedRect(QRectF(50,100,400,650),50,50)
    
    def paintEvent(self,event):
        qp = QPainter(self)
        qp.setPen(QPen(Qt.white,5,Qt.SolidLine))
        qp.begin(self)
        self.paint(qp)
        qp.end()

    def paint(self,qp):
        qp.setRenderHint(qp.Antialiasing)
        qp.fillPath(self.frame_path,QColor(140,77,167))
        qp.drawPath(self.frame_path)
        #根据global_points_list画图

# 样式  
StyleSheet = """  
TitleBar {  
background-color: red;  
}  
/*最小化最大化关闭按钮通用默认背景*/  
#buttonMinimum,#buttonMaximum,#buttonClose {  
border: none;  
background-color: red;  
}  
/*悬停*/  
#buttonMinimum:hover,#buttonMaximum:hover {  
background-color: red;  
color: white;  
}  
#buttonClose:hover {  
color: white;  
}  
/*鼠标按下不放*/  
#buttonMinimum:pressed,#buttonMaximum:pressed {  
background-color: Firebrick;  
}  
#buttonClose:pressed {  
color: white;  
background-color: Firebrick;  
}  
"""  
class TitleBar(QWidget):
     
     # 窗口最小化信号
    windowMinimumed = pyqtSignal()
     # 窗口最大化信号
    windowMaximumed = pyqtSignal()
     # 窗口还原信号
    windowNormaled = pyqtSignal()
     # 窗口关闭信号
    windowClosed = pyqtSignal()
     # 窗口移动
    windowMoved = pyqtSignal(QPoint)
 
    def __init__(self, *args, **kwargs):
         super(TitleBar, self).__init__(*args, **kwargs)
         # 支持qss设置背景
         self.setAttribute(Qt.WA_StyledBackground, True)
         self.mPos = None
         self.iconSize = 5  # 图标的默认大小
         # 设置默认背景颜色,否则由于受到父窗口的影响导致透明
         self.setAutoFillBackground(True)
         palette = self.palette()
         palette.setColor(palette.Window, QColor(240, 240, 240))
         self.setPalette(palette)
         # 布局
         layout = QHBoxLayout(self, spacing=0)
         layout.setContentsMargins(0, 0, 0, 0)
         # 窗口图标
         self.iconLabel = QLabel(self)
         self.iconLabel.setFixedSize(38,38)
         self.iconLabel.setPixmap(QPixmap('./src/main/python/1.png'))
         self.iconLabel.setScaledContents(True)
         layout.addWidget(self.iconLabel)
         
         # 窗口标题
         self.titleLabel = QLabel(self)
         self.titleLabel.setMargin(2)
         self.setTitle("standardmotion")
         layout.addWidget(self.titleLabel)
         # 中间伸缩条
         layout.addSpacerItem(QSpacerItem(
             40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
         # 利用Webdings字体来显示图标
         font = self.font() or QFont()
         font.setFamily('Webdings')
        
         # 最小化按钮
         self.buttonMinimum = QPushButton(
             '', self, clicked=self.windowMinimumed.emit, font=font, objectName='buttonMinimum')
         layout.addWidget(self.buttonMinimum)
         # 最大化/还原按钮
         self.buttonMaximum = QPushButton(
             '', self, clicked=self.showMaximized, font=font, objectName='buttonMaximum')
         layout.addWidget(self.buttonMaximum)
         # 关闭按钮
         self.buttonClose = QPushButton(
             'r', self, clicked=self.windowClosed.emit, font=font, objectName='buttonClose')
         layout.addWidget(self.buttonClose)
         # 初始高度
         self.setHeight()
    def showMaximized(self):
         if self.buttonMaximum.text() == '':
             # 最大化
             self.buttonMaximum.setText('')
             self.windowMaximumed.emit()
         else:  # 还原
             self.buttonMaximum.setText('')
             self.windowNormaled.emit()
 
    def setHeight(self, height=38):
         """设置标题栏高度"""
         self.setMinimumHeight(height)
         self.setMaximumHeight(height)
         # 设置右边按钮的大小
         self.buttonMinimum.setMinimumSize(height, height)
         self.buttonMinimum.setMaximumSize(height, height)
         self.buttonMaximum.setMinimumSize(height, height)
         self.buttonMaximum.setMaximumSize(height, height)
         self.buttonClose.setMinimumSize(height, height)
         self.buttonClose.setMaximumSize(height, height)
 
    def setTitle(self, title):
         """设置标题"""
         self.titleLabel.setText(title)
 
    def setIcon(self, icon):
         """设置图标"""
         self.iconLabel.setPixmap(icon.pixmap(self.iconSize, self.iconSize))
 
    def setIconSize(self, size):
         """设置图标大小"""
         self.iconSize = size
 
    def enterEvent(self, event):
         self.setCursor(Qt.ArrowCursor)
         super(TitleBar, self).enterEvent(event)
 
    def mouseDoubleClickEvent(self, event):
         super(TitleBar, self).mouseDoubleClickEvent(event)
         self.showMaximized()
 
    def mousePressEvent(self, event):
         """鼠标点击事件"""
         if event.button() == Qt.LeftButton:
             self.mPos = event.pos()
         event.accept()
 
    def mouseReleaseEvent(self, event):
         '''鼠标弹起事件'''
         self.mPos = None
         event.accept()
 
    def mouseMoveEvent(self, event):
         if event.buttons() == Qt.LeftButton and self.mPos:
             self.windowMoved.emit(self.mapToGlobal(event.pos() - self.mPos))
         event.accept()


class gui(QDialog):
    def __init__(self, parent=None):
        super(gui, self).__init__(parent)
        self.resize(1200, 800)
        self.setWindowOpacity(0.99) # 设置窗口透明度
        #self.center()
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去边框

        #self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # 背景透明（就是ui中黑色背景的那个控件）

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        #effect = QGraphicsDropShadowEffect(self)
        #effect.setBlurRadius(12)
        #effect.setOffset(0, 0)
        #effect.setColor(Qt.gray)
        #self.setGraphicsEffect(effect)
        
        #self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        #self.setWindowFlag(Qt.WindowMaximizeButtonHint, True) #窗口最大化
        #self.setWindowFlag(Qt.WindowCloseButtonHint,True)
        self.tabs=QTabWidget()
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
      
        palette1 = QPalette()
        #self.palette.setBrush(QPalette.Background, QBrush(QPixmap('background1.jpg')))
        #self.setPalette(self.palette)#初始化窗口并设置背景图片
        #self.setPixmap(QPixmap('C:\\Users\\Hp\\Desktop\\solved.png'))
        palette1.setBrush(QPalette.Background, QBrush(QPixmap('C:\\Users\\Hp\\Desktop\\solved.jpg')))
        self.setPalette(palette1)
        #QDialog.setStylSheet("QDialog{background-image:url(C:\\Users\\Hp\\Desktop\\solve1d.jpg);}")
        

        self.titleBar=TitleBar()

        self.tabs.setFont(QFont("楷体", 20, QFont.Bold) )
        self.crFTab()
        self.crTTab()
        self.tabs.addTab(self.FTab,'Main')
        self.tabs.addTab(self.TTab,'Setting')
        #self.tabs.setTabPosition(QtGui.QTabWidget.East)
        
        mainlayout=QGridLayout(spacing=0)
        mainlayout.addWidget(self.tabs,1,0)
        mainlayout.addWidget(self.titleBar,0,0)
        self.setLayout(mainlayout)
        self.setWindowTitle("standardmotion")
        
        self.titleBar.windowMinimumed.connect(self.showMinimized)  
        self.titleBar.windowMaximumed.connect(self.showMaximized)  
        self.titleBar.windowNormaled.connect(self.showNormal)  
        self.titleBar.windowClosed.connect(self.close)  
        self.titleBar.windowMoved.connect(self.move)  
        self.windowTitleChanged.connect(self.titleBar.setTitle)  
        self.windowIconChanged.connect(self.titleBar.setIcon)   


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
         #按钮的生成与大小状态的设置
        self.start_button=QPushButton("开始运行")
        self.start_button.setCheckable(True)
        self.start_button.clicked.connect(self.start)
        #self.start_button.clicked.connect(self.repaint)
       
        self.quit_button=QPushButton("退出程序")
        self.quit_button.setFlat(True) #去除按钮边框
        self.quit_button.clicked.connect(self._quit)
 
        self.upload_button=QPushButton("上传文件")
        self.upload_button.setCheckable(True)
        self.upload_button.clicked.connect(self._upload)
        
        self.about_button=QPushButton("关于")
        self.about_button.setCheckable(True)
        self.about_button.clicked.connect(self._about)

        self.start_button.setFixedSize(200,50)
        self.start_button.setFont(QFont("仿宋",20))
        self.quit_button.setFixedSize(200,40)
        self.quit_button.setFont(QFont("仿宋",20))
        self.upload_button.setFixedSize(200,50)
        self.upload_button.setFont(QFont("仿宋",20))
        self.about_button.setFixedSize(200,50)
        self.about_button.setFont(QFont("仿宋",20))

        self.start_button.setStyleSheet( 
                                 "QPushButton{background-color:rgb(0,90,171)}"  #按键背景色
                                 "QPushButton:hover{color:red}" #光标移动到上面后的前景色
                                 "QPushButton{border-radius:6px}"  #圆角半径
                                 "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}" #按下时的样式
                                 )
        self.quit_button.setStyleSheet(
                                 "QPushButton{color:rgb(101,153,26)}" #按键前景色
                                 "QPushButton{background-color:rgb(255,255,255)}"  #按键背景色
                                 "QPushButton:hover{color:red}" #光标移动到上面后的前景色
                                 "QPushButton{border-radius:6px}"  #圆角半径
                                 "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}" #按下时的样式
                                 )
        self.upload_button.setStyleSheet(
                                 "QPushButton{color:rgb(101,153,26)}" #按键前景色
                                 "QPushButton{background-color:rgb(255,222,0)}"  #按键背景色
                                 "QPushButton:hover{color:red}" #光标移动到上面后的前景色
                                 "QPushButton{border-radius:6px}"  #圆角半径
                                 "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}" #按下时的样式
                                 )
        self.about_button.setStyleSheet(
                               "QPushButton{color:White;border-radius: 7px;font-family:微软雅黑;background:#000000;border:1px;}"
                                "QPushButton:hover{background:#FFFFFF;}"
                                "QPushButton:pressed{background:#6600FF;}"
                                )
        self.upload_button.setStyleSheet(
            "QPushButton{border:0px;width:140px;height:30px;border-radius:15px;background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(255,134,143), stop:1 rgb(247,202,143));}" 
            "QPushButton:hover{background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #ffd2f0, stop:1 #b0cbf8);}"
            "QPushButton:pressed{background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #e1aad2, stop:1 #92adda);}"
        )
        self.about_button.setStyleSheet(
            "QPushButton{border:0px;width:140px;height:30px;border-radius:15px;background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #fbc2eb, stop:1 #a6c1ee);}" 
            "QPushButton:hover{background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #ffd2f0, stop:1 #b0cbf8);}"
            "QPushButton:pressed{background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #e1aad2, stop:1 #92adda);}"
        )
        self.quit_button.setStyleSheet(
            "QPushButton{border:0px;width:140px;height:30px;border-radius:15px;background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #fbc2eb, stop:1 #a6c1ee);}" 
            "QPushButton:hover{background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #ffd2f0, stop:1 #b0cbf8);}"
            "QPushButton:pressed{background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #e1aad2, stop:1 #92adda);}"
        )
        self.start_button.setStyleSheet(
            "QPushButton{border:0px;width:140px;height:30px;border-radius:15px;background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(255,134,143), stop:1 rgb(247,202,143));}" 
            "QPushButton:hover{background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #ffd2f0, stop:1 #b0cbf8);}"
            "QPushButton:pressed{background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #e1aad2, stop:1 #92adda);}"
        )
        
        #s是否增加分块
        #self.coverlabel=QLabel()
        #cover_pixmap = QPixmap('./image/cov.png')
        #self.coverlabel.setPixmap(cover_pixmap)
        self.status=QLabel("正在初始化，请稍等")
        
        self.status.setStyleSheet("QLabel {background-color : white;border-radius: 30px;border-style: outset;border-width: 2px;border-color: bule;}")
        self.status.setFixedSize(500,100)
        self.status.setFont(QFont("仿宋",20, QFont.Bold))
        self.status.setAlignment(Qt.AlignCenter)

        button_layout=QVBoxLayout()#QHBoxLayout()水平布局
        
        button_layout.addStretch(1)
        button_layout.addStretch(1)
        button_layout.addWidget(self.start_button)
        button_layout.addStretch(1)
        button_layout.addWidget(self.upload_button,Qt.AlignCenter)
        button_layout.addStretch(1)
        button_layout.addWidget(self.quit_button,Qt.AlignCenter)
        button_layout.addStretch(1)
        button_layout.addWidget(self.about_button,Qt.AlignCenter)
        button_layout.addStretch(1)
        button_layout.addStretch(1)
        
        
        self.status2=QLabel("Welcome")

        self.status2.setStyleSheet("QLabel {background-color :rgb(125,182,157);border-radius: 30px;border-style: outset;border-width: 2px;border-color: bule;color:white}")
        self.status2.setFixedSize(500,300)
        self.status2.setFont(QFont("仿宋",50, QFont.Bold))
        self.status2.setAlignment(Qt.AlignCenter)
        
        
        stauts_layout=QVBoxLayout()
        stauts_layout.addStretch(1)
        
        stauts_layout.addWidget(self.status,Qt.AlignCenter)
        stauts_layout.addStretch(1)
        stauts_layout.addWidget(self.status2,Qt.AlignCenter)
        self.pose_drawing=DrawCircle()
        self.add_shadow()
        stauts_layout.addStretch(1)
        #self.pose_drawing.setStyleSheet("background-color : white;")

        Tablayout.addLayout(button_layout,0,0,1,1)
        #Tablayout.addWidget(self.coverlabel,1,0,1,1,Qt.AlignCenter)
        Tablayout.addLayout(stauts_layout,0,1,Qt.AlignCenter)
        Tablayout.addWidget(self.pose_drawing,0,2,Qt.AlignCenter)
    

        self.FTab.setLayout(Tablayout)
        palette=QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.FTab.setPalette(palette)
       
    def repaint(self):
        self.pose_drawing.setColor('green')

    def start(self):
        if(not initialed):
            self.start_button.setChecked(False)
            warnning_message=QMessageBox()
            warnning_message.setText("程序尚未初始化")
            warnning_message.setIcon(QMessageBox.Warning)
            warnning_message.setWindowTitle("警告")
            warnning_message.setFont(QFont("仿宋", 20, QFont.Bold))
            warnning_message.exec()

        elif(self.start_button.isChecked()):
            #self.CTab.setDisabled(True)
            self.CTabG_1.setDisabled(True)
            self.CTabG_2.setDisabled(True)
            self.start_button.setText("停止检测")
            self.running_timer = QTimer(self)
            self.running_timer.timeout.connect(self.running)
            self.running_timer.start(30)
        else:
            #self.CTab.setEnabled(True)
            self.CTabG_1.setEnabled(True)
            self.CTabG_2.setEnabled(True)
            self.start_button.setText("开始检测")
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

    def out(self):
        pass
    
    def closeEvent(self,event):#函数名固定不可变
        reply=QtWidgets.QMessageBox.question(self,u'注意',u'您真的要关闭窗口吗？',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        #QtWidgets.QMessageBox.question(self,u'弹窗名',u'弹窗内容',选项1,选项2)
        if reply==QtWidgets.QMessageBox.Yes:
            self._quit()
        else:
            event.ignore()#忽视点击X事件
    def _about(self):
        pass

    def _upload(self):
        pass
    def center(self):
        '''
        获取桌面长宽
        获取窗口长宽
        移动
        '''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
    def add_shadow(self):
        # 添加阴影
        self.effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0,0) # 偏移
        self.effect_shadow.setBlurRadius(10) # 阴影半径
        self.effect_shadow.setColor(QtCore.Qt.gray) # 阴影颜色
        self.setGraphicsEffect(self.effect_shadow) # 将设置套用到widget窗口中
 
    def crTTab(self):
        self.TTab=QWidget()
        pass
    
if __name__ == "__main__":
    appctxt = ApplicationContext()
    appctxt.app.setStyle('Fusion')
    gui_example= gui()
    #win=cure.Windows(gui(),'name',True)##实现对窗口的美化
    gui_example.show()
    sys.exit(appctxt.app.exec_())
