# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Bogdan\Documents\Licenta\app_user_interface.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PIL import Image
from PIL.ImageQt import ImageQt
            
from keras.models import Sequential, load_model
from keras.applications import vgg16

from skimage.color import rgb2lab, lab2rgb, gray2rgb, rgb2gray
from skimage.io import imsave

import numpy as np
import os

class Predictor(object):
    def __init__(self, model_path, size):
        self.size = size
        self.model = load_model(model_path)

    def predict(self, image_path):
        
        im = Image.open(image_path)
        old_size = im.size
           
        ratio = float(self.size) / max(old_size)
        new_size = tuple([int(x * ratio) for x in old_size])
        im = im.resize(new_size, Image.ANTIALIAS)
           
        new_im = Image.new("RGB", (self.size, self.size))
        new_im.paste(im, ((self.size - new_size[0]) // 2, (self.size - new_size[1]) // 2))
           
        im_arr = np.array(new_im, dtype="float")
        im_arr *= 1.0 / 255
           
        lab = rgb2lab(im_arr)
        l = lab[:,:,0]
        l = np.expand_dims(l, axis = 0)
        l = np.expand_dims(l, axis = 3)    
               
        ab = self.model.predict(l)
        ab *= 128
           
        l = np.squeeze(l, axis = 3)
        result = np.zeros((self.size, self.size, 3))
        result[:,:,0] = l
        result[:,:,1:] = ab
        result = lab2rgb(result)
        # imsave('./data/results/image_2/model4_15_' + str(idx) + '.png', result)
        
        return np.array(result)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(934, 418)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 931, 371))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.chooseImageBtn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.chooseImageBtn.setObjectName("chooseImageBtn")
        self.gridLayout.addWidget(self.chooseImageBtn, 0, 0, 1, 1)
        self.originalImage = QtWidgets.QLabel(self.gridLayoutWidget)
        self.originalImage.setFrameShape(QtWidgets.QFrame.Box)
        self.originalImage.setText("")
        self.originalImage.setAlignment(QtCore.Qt.AlignCenter)
        self.originalImage.setObjectName("originalImage")
        self.gridLayout.addWidget(self.originalImage, 1, 0, 1, 1)
        self.grayscaleImage = QtWidgets.QLabel(self.gridLayoutWidget)
        self.grayscaleImage.setFrameShape(QtWidgets.QFrame.Box)
        self.grayscaleImage.setText("")
        self.grayscaleImage.setAlignment(QtCore.Qt.AlignCenter)
        self.grayscaleImage.setObjectName("grayscaleImage")
        self.gridLayout.addWidget(self.grayscaleImage, 1, 1, 1, 1)
        self.predictedImage = QtWidgets.QLabel(self.gridLayoutWidget)
        self.predictedImage.setFrameShape(QtWidgets.QFrame.Box)
        self.predictedImage.setText("")
        self.predictedImage.setAlignment(QtCore.Qt.AlignCenter)
        self.predictedImage.setObjectName("predictedImage")
        self.gridLayout.addWidget(self.predictedImage, 1, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 934, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.chooseImageBtn.clicked.connect(self.chooseImage)
        
        self.size = 150
        model_path = 'model.h5' 
        if '_MEIPASS2' in os.environ:
            model_path = os.path.join(os.environ['_MEIPASS2'], model_path)
        self.predictor = Predictor(model_path, self.size)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Colorization"))
        self.label_3.setText(_translate("MainWindow", "Predicted"))
        self.label_2.setText(_translate("MainWindow", "Grayscale"))
        self.chooseImageBtn.setText(_translate("MainWindow", "Choose image..."))

    def chooseImage(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Choose Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
        
        if filename:
            predicted_im = self.predictor.predict(filename)
            predicted_im = Image.fromarray((predicted_im * 255).astype(np.uint8))
            predicted_im = np.array(predicted_im)
            
            original_im = QPixmap(filename)
            original_im = original_im.scaled(self.size, self.size, QtCore.Qt.KeepAspectRatio)
            self.originalImage.setPixmap(original_im)
            
            grayscale_im = original_im.copy()
            grayscale_im = QtGui.QPixmap.toImage(grayscale_im)
            grayscale_im = grayscale_im.convertToFormat(QImage.Format_Grayscale8)
            self.grayscaleImage.setPixmap(QtGui.QPixmap.fromImage(grayscale_im))
            
            height, width, channel = predicted_im.shape
            bytesPerLine = 3 * width
            predicted_im = QImage(predicted_im.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.predictedImage.setPixmap(QtGui.QPixmap.fromImage(predicted_im))
            
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

