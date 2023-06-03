import os
import sys
import traceback
import qdarkstyle
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox

import detect
from utils.myutil import file_is_pic, Globals
from glob import glob
from PyQt5 import QtCore, QtGui, QtWidgets
from time import time

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.timer_detect = QtCore.QTimer()
        self.setupUi(self)
        self.init_logo()  # 初始化logo
        self.init_slots()  # 初始化槽函数
        self.file_path = None  # 数据路径
        self.model_path = ['./weights/best.pt']  # 模型路径
        self.file_suffix = None  # 文件后缀
        self.result_path = "result"  # 检测图片保存路径
        self.init_file()  # 初始化必要的文件夹
        self.ui()
        self.old_hook = sys.excepthook
        sys.excepthook = self.catch_exceptions

    def catch_exceptions(self, ty, value, tback):

        traceback_format = traceback.format_exception(ty, value, tback)
        traceback_string = "".join(traceback_format)
        QtWidgets.QMessageBox.critical(None, "An exception was raised", "{}".format(traceback_string))
        self.old_hook(ty, value, tback)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1820, 1020)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0,1700, 900))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, -1, 300)
        self.verticalLayout.setObjectName("verticalLayout")

        self.pushButton_img = QtWidgets.QPushButton(self.widget)
        self.pushButton_img.setObjectName("pushButton_img")
        self.verticalLayout.addWidget(self.pushButton_img)
        self.pushButton_model = QtWidgets.QPushButton(self.widget)
        self.pushButton_model.setObjectName("pushButton_model")
        self.verticalLayout.addWidget(self.pushButton_model)
        # self.pushButton_flash = QtWidgets.QPushButton(self.widget)
        # self.pushButton_flash.setObjectName("flash")
        # self.verticalLayout.addWidget(self.pushButton_flash)
        self.pushButton_camera_detect = QtWidgets.QPushButton(self.widget)
        self.pushButton_camera_detect.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_camera_detect)
        self.pushButton_detect = QtWidgets.QPushButton(self.widget)
        self.pushButton_detect.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_detect)
        self.pushButton_flash = QtWidgets.QPushButton(self.widget)
        self.pushButton_flash.setObjectName("flash")
        self.verticalLayout.addWidget(self.pushButton_flash)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.pushButton_showdir = QtWidgets.QPushButton(self.widget)
        self.pushButton_showdir.setObjectName("pushButton_5")
        self.verticalLayout_2.addWidget(self.pushButton_showdir)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.label.setStyleSheet("border: 1px solid white;")
        self.horizontalLayout.addWidget(self.label)

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.v_layout = QtWidgets.QVBoxLayout(self)
        self.v_layout.addWidget(self.scrollArea)
        self.setLayout(self.v_layout)

        self.horizontalLayout.addWidget(self.scrollArea)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "目标检测系统"))
        self.pushButton_img.setText(_translate("MainWindow", "加载本地数据"))
        self.pushButton_model.setText(_translate("MainWindow", "选择模型"))
        self.pushButton_flash.setText(_translate("MainWindow", "查看結果"))
        self.pushButton_camera_detect.setText(_translate("MainWindow", "摄像头检测"))
        self.pushButton_detect.setText(_translate("MainWindow", "本地数据检测"))
        self.pushButton_showdir.setText(_translate("MainWindow", "打开输出文件夹"))
        self.label.setText(_translate("MainWindow", "实时检测情况"))

    def ui(self):

        img_path = glob('./result/camera/*.jpg')
        total = len(img_path)
        col = 0
        row = 0
        self.max_columns = total if total < 5 else 5
        for i in range(total):
            self.max_columns = total if total < 5 else 5

            photo = QPixmap(img_path[i])
            width = photo.width()
            height = photo.height()

            if width == 0 or height == 0:
                continue
            tmp_image = photo.toImage()  # 将QPixmap对象转换为QImage对象
            size = QSize(width, height)
            # photo.convertFromImage(tmp_image.scaled(size, Qt.IgnoreAspectRatio))
            photo = photo.fromImage(tmp_image.scaled(size, Qt.IgnoreAspectRatio))

            # 为每个图片设置QLabel容器
            label = QLabel()
            w = int(self.width() / self.max_columns * 0.8)
            h = int(w * photo.height() / photo.width())
            label.setFixedSize(w, h)
            label.setStyleSheet("border:1px solid gray")
            label.setPixmap(photo)
            label.setScaledContents(True)  # 图像自适应窗口大小

            self.gridLayout.addWidget(label, row, col)
            # 计算下一个label 位置
            if col < self.max_columns - 1:
                col = col + 1
            else:
                col = 0
                row += 1
    def init_slots(self):
        self.pushButton_img.clicked.connect(self.load_source)

        self.pushButton_model.clicked.connect(self.select_model)
        self.pushButton_flash.clicked.connect(self.ui)

        self.pushButton_detect.clicked.connect(self.target_detect)
        self.pushButton_showdir.clicked.connect(self.show_dir)
        self.pushButton_camera_detect.clicked.connect(self.camera_detect)

    # 绘制LOGO
    def init_logo(self):
        pix = QtGui.QPixmap('')
        self.label.setScaledContents(True)
        self.label.setPixmap(pix)

    def load_source(self):
        self.file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "加载数据", "data", "All Files(*)")
        self.suffix = self.file_path.split(".")[-1]  # 读取后缀
        pixmap = QPixmap(self.file_path)
        pixmap = pixmap.scaled(self.label.size(), Qt.IgnoreAspectRatio)
        self.label.setPixmap(pixmap)
        if self.file_path != "":
            self.pushButton_img.setText(self.file_path.split('/')[-1])
        # 清空result文件夹内容
        for i in os.listdir(self.result_path):
            file_data = self.result_path + "/" + i
            if os.path.isfile(file_data):
                os.remove(file_data)
            if os.path.isdir(file_data):
                for j in os.listdir(file_data):
                    os.remove(os.path.join(file_data,j))

    def init_file(self):
        if not os.path.exists(self.result_path):
            os.mkdir(self.result_path)
        if not os.path.exists('./result/camera'):
            os.mkdir('./result/camera')
        for i in os.listdir('./result/camera'):
            file_data = './result/camera' + "/" + i
            if os.path.isfile(file_data):
                os.remove(file_data)
            if os.path.isdir(file_data):
                for j in os.listdir(file_data):
                    os.remove(os.path.join(file_data,j))


    def select_model(self):
        model_path = QtWidgets.QFileDialog.getOpenFileName(self, "选择模型", "weights", "Model files(*.pt)")
        self.model_path = model_path
        if model_path[0] != "":
            self.pushButton_model.setText(self.model_path[0].split('/')[-1])

    # 目标检测
    def target_detect(self):
        if self.check_file():
            # 点击之后防止误触，禁用按钮
            self.pushButton_img.setEnabled(False)
            self.pushButton_model.setEnabled(False)
            self.pushButton_detect.setEnabled(False)
            self.pushButton_camera_detect.setEnabled(False)
            self.thread = DetectionThread(self.file_path, self.model_path, self.label)
            self.thread.start()
            # 子线程运行结束之后signal_done，主线程执行UI更新操作
            QtWidgets.QApplication.processEvents()
            self.thread.signal_done.connect(self.flash_target)

    # 目标检测之前检查是否选择了数据和模型
    def check_file(self):
        if self.file_path is None or self.file_path == "":
            QMessageBox.information(self, '提示', '请先导入数据')
            return False
        if self.model_path is None or self.model_path[0] == "":
            QMessageBox.information(self, '提示', '请先选择模型')
            return False
        return True

    # 摄像头检测之前检查是否选择了模型
    def check_model(self):
        if self.model_path is None or self.model_path[0] == "":
            QMessageBox.information(self, '提示', '请先选择模型')
            return False
        return True

    # 刷新
    def flash_target(self):
        if file_is_pic(self.suffix):
            img_path = os.getcwd() + '/result/' + [f for f in os.listdir('result')][0]
            pixmap = QPixmap(img_path)
            pixmap = pixmap.scaled(self.label.size(), Qt.IgnoreAspectRatio)
            self.label.setPixmap(pixmap)
        # 刷新完之后恢复按钮状态
        self.pushButton_img.setEnabled(True)
        self.pushButton_model.setEnabled(True)
        self.pushButton_detect.setEnabled(True)
        self.pushButton_camera_detect.setEnabled(True)

    # 显示输出文件夹
    def show_dir(self):
        path = os.path.join(os.getcwd(), 'result')
        os.system(f"start explorer {path}")

    # 摄像头检测
    def camera_detect(self):
        if Globals.camera_running:
            Globals.camera_running = False
            self.pushButton_camera_detect.setText("摄像头检测")
            self.pushButton_img.setEnabled(True)
            self.pushButton_model.setEnabled(True)
            self.pushButton_detect.setEnabled(True)
            self.label.clear()
        else:
            if self.check_model():
                Globals.camera_running = True
                self.pushButton_img.setEnabled(False)
                self.pushButton_model.setEnabled(False)
                self.pushButton_detect.setEnabled(False)
                self.pushButton_camera_detect.setText("关闭摄像头")
                self.camera_thread = CameraDetectionThread(self.model_path, self.label,res=self.gridLayout)
                self.camera_thread.start()

# DetectionThread子线程用来执行导入资源的目标检测
class DetectionThread(QThread):
    signal_done = pyqtSignal(int)  # 是否结束信号

    def __init__(self, file_path, model_path, label):
        super(DetectionThread, self).__init__()
        self.file_path = file_path
        self.model_path = model_path[0]
        self.label = label

    def run(self):
        detect.run(source=self.file_path, weights=self.model_path, show_label=self.label, save_img=True)
        self.signal_done.emit(1)  # 发送结束信号

# CameraDetectionThread子线程用来执行摄像头实时检测
class CameraDetectionThread(QThread):
    def __init__(self, model_path, label,res):
        super(CameraDetectionThread, self).__init__()
        self.model_path = model_path[0]
        self.label = label
        self.res = res
    def run(self):
        detect.run(source="HKcamera", weights=self.model_path, show_label=self.label, save_img=False, use_camera=True,res_label=self.res)





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ui = Ui_MainWindow()
    ui.show()

    sys.exit(app.exec_())