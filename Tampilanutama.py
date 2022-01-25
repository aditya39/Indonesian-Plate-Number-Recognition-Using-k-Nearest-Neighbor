# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simple.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QDate
from Main import *
from PyQt5.QtGui import QIcon, QPixmap
from DataKendaraan import Ui_DataKendaraan
from insertData import Ui_InsertData
import sqlite3
from Sqlitehelper import SqliteHelper
import cv2
import imutils
import argparse
import numpy as np
import Preprocess as pp
import os
import time
import math
import Calibration as cal
import DetectChars
import DetectPlates
import PossiblePlate


class Ui_MainWindow(object):

    def welcomeWindowShow(self):
        self.welcomeWindow = QtWidgets.QMainWindow()
        self.ui = Ui_DataKendaraan()
        self.ui.setupUi(self.welcomeWindow)
        self.welcomeWindow.show()


    def insertWindow(self):
        self.welcomeWindow2 = QtWidgets.QMainWindow()
        self.ui2 = Ui_DataKendaraan()
        self.ui2.setupUi(self.welcomeWindow2)
        self.ui2.welcomeWindowShow()


    def clear(self):
        self.lineId.setText("")
        self.lineNamapemilik.setText("")
        self.lineNomorpolisi.setText("")
        self.lineKendaraan.setText("")
        self.lineJenis.setText("")
        self.lineTahun.setText("")
        self.lineKota.setText("")
        self.lineStatus.setText("")


    def fetchData(self):
        self.clear()
        helper = SqliteHelper("Kendaraan.db")
        Plat = (self.linePelat.text(),)
        conn = sqlite3.connect("Kendaraan.db")
        c = conn.cursor()
        c.execute("SELECT NO_POLISI FROM datakendaraan")
        ay = c.fetchall()
        for x in enumerate(ay):
            if Plat == x[1]:
                c.execute("SELECT * FROM datakendaraan WHERE NO_POLISI=?",Plat)
                ax = c.fetchall()
                self.lineId.setText(str(ax[0][0]))
                self.lineNamapemilik.setText(str(ax[0][1]))
                self.lineNomorpolisi.setText(str(ax[0][2]))
                self.lineKendaraan.setText(str(ax[0][3]))
                self.lineJenis.setText(str(ax[0][4]))
                self.lineTahun.setText(str(ax[0][5]))
                self.lineKota.setText(str(ax[0][6]))
                self.lineStatus.setText(str(ax[0][7]))

    SCALAR_BLACK = (0.0, 0.0, 0.0)
    SCALAR_WHITE = (255.0, 255.0, 255.0)
    SCALAR_YELLOW = (0.0, 255.0, 255.0)
    SCALAR_GREEN = (0.0, 255.0, 0.0)
    SCALAR_RED = (0.0, 0.0, 255.0)
    VERIF = 8  # number for verification the plate license
    showSteps = False

    def main(self):
        # argument for input video/image/calibration
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video",
                        help="path to video file")

        ap.add_argument("-i", "--image",
                        help="Path to the image")

        ap.add_argument("-c", "--calibration",
                        help="image or video or camera")
        args = vars(ap.parse_args())

        if args.get("calibration", True):
            imgOriginalScene = cv2.imread(args["calibration"])
            if imgOriginalScene is None:
                print("   Please check again the path of image or argument !")

            imgOriginalScene = imutils.resize(imgOriginalScene, width=720)
            cal.calibration(imgOriginalScene)
            return

        if args.get("video", True):
            camera = cv2.VideoCapture(0)
            if camera is None:
                print("   Please check again the path of video or argument !")
            loop = True

        elif args.get("image", True):
            imgOriginalScene = cv2.imread(args["image"])
            if imgOriginalScene is None:
                print("   Please check again the path of image or argument !")
            loop = False
        else:
            camera = cv2.VideoCapture(0)

            loop = True

        # add knn library for detect chars
        blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()  # attempt KNN training

        if blnKNNTrainingSuccessful == False:
            print("\nerror: KNN traning was not successful\n")
            return
        count = 0

        license = []
        VER = np.zeros(VERIF)
        for x in VER:
            license.append("")
        numlicense = ""
        knn = 0

        # Looping for Video
        while (loop):
            # grab the current frame
            (grabbed, frame) = camera.read()

            if args.get("video") and not grabbed:
                break

            # resize frame
            imgOriginalScene = imutils.resize(frame, width=620)
            #cv2.imshow("imageori", imgOriginalScene)

            # Panggil preprocess untuk dapet grayscale dan threshold
            imgGrayscale, imgThresh = pp.preprocess(imgOriginalScene)

            #cv2.imshow("thres", imgThresh)
            # Proses utama deteksi
            # Hasil berupa frame dan nomor polisi
            imgOriginalScene, licenses = searching(imgOriginalScene, loop)

            # only save 5 same license each time
            license[count + 1] = licenses
            if (license[count] == license[count + 1]):
                license[count] = license[count + 1]
                count = count + 1
            elif (license[count] != license[count + 1]):
                coba = license[count + 1]
                count = 0
                license[count] = coba
            if count == (VERIF - 1):
                if (license[VERIF - 1] == ""):
                    print("no characters were detected\n")
                else:
                    # if number license same, not be saved
                    if numlicense == license[VERIF - 1]:
                        print("still = " + numlicense + "\n")
                    else:
                        numlicense = license[VERIF - 1]
                        print("A new license plate read from image = " + license[VERIF - 1] + "\n")
                        self.linePelat.setText(numlicense)
                        self.fetchData()
                        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        img_height, img_width, img_colors = image.shape
                        step = img_colors * img_width
                        qImage = QImage(image.data, img_width, img_height, step, QImage.Format_RGB888)
                        self.labelFoto.setPixmap(QtGui.QPixmap.fromImage(qImage.scaled(400, 400, QtCore.Qt.KeepAspectRatio)))
                        #cv2.imshow(license[VERIF - 1], imgOriginalScene)

                        namefile = "hasil/" + license[VERIF - 1] + ".png"
                        cv2.imwrite(namefile, imgOriginalScene)
                count = 0
            # print(license)
            # re-show scene image
            # imgOriginalScene = cv2.blur(imgOriginalScene,(12,12))
            # cv2.putText(imgOriginalScene,"Press 's' to save frame to be 'save.png', for calibrating",(10,30),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,bottomLeftOrigin = False)
            # drawRedRectangleAroundPlate(imgOriginalScene, imgOriginalScene)

            # cv2.rectangle(imgOriginalScene,((imgOriginalScene.shape[1]/2-230),(imgOriginalScene.shape[0]/2-80)),((imgOriginalScene.shape[1]/2+230),(imgOriginalScene.shape[0]/2+80)),SCALAR_GREEN,3)

            result = imgOriginalScene
            height, width, channel = result.shape
            scale_w = float(390) / float(width)
            scale_h = float(190) / float(height)
            scale = min([scale_w, scale_h])
            image = cv2.resize(result, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            img_height, img_width, img_colors = image.shape
            step = img_colors * img_width
            qImage = QImage(image.data, img_width, img_height, step, QImage.Format_RGB888 )
            self.ImgWidget.setPixmap(QPixmap.fromImage(qImage))

            #cv2.imshow("result", result)
            #cv2.imshow("ori", frame)

            key = cv2.waitKey(5) & 0xFF
            if key == ord('s'):
                knn = str(knn)
                savefileimg = "calib_knn/img_" + knn + ".png"
                savefileThr = "calib_knn/Thr_" + knn + ".png"
                # cv2.saveimage("save.png", imgOriginalScene)
                cv2.imwrite(savefileimg, frame)
                cv2.imwrite(savefileThr, imgThresh)
                print("image save !")
                knn = int(knn)
                knn = knn + 1
            if key == 27:  # if the 'q' key is pressed, stop the loop
                break
                camera.release()  # cleanup the camera and close any open windows

        # For image only
        if (loop == False):
            imgOriginalScene = imutils.resize(imgOriginalScene, width=720)
            #cv2.imshow("original", imgOriginalScene)
            imgGrayscale, imgThresh = pp.preprocess(imgOriginalScene)
            #cv2.imshow("threshold", imgThresh)
            #cv2.imshow("grayscale", imgGrayscale)

            imgOriginalScene, license = searching(imgOriginalScene, loop)
            # imgOriginalScene = imutils.detransform(imgOriginalScene)

            cv2.waitKey(0)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return result

    # end main

    ###################################################################################################
    def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):

        p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)  # get 4 vertices of rotated rect
        cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)  # draw 4 red lines
        cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
        cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
        cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)

    # end function

    ###################################################################################################
    def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
        ptCenterOfTextAreaX = 0  # this will be the center of the area the text will be written to
        ptCenterOfTextAreaY = 0

        ptLowerLeftTextOriginX = 0  # this will be the bottom left of the area that the text will be written to
        ptLowerLeftTextOriginY = 0

        sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
        plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape

        intFontFace = cv2.FONT_HERSHEY_SIMPLEX  # choose a plain jane font
        fltFontScale = float(plateHeight) / 30.0  # base font scale on height of plate area
        intFontThickness = int(round(fltFontScale * 1.5))  # base font thickness on font scale

        textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale,
                                             intFontThickness)  # call getTextSize

        # unpack roatated rect into center point, width and height, and angle
        ((intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight),
         fltCorrectionAngleInDeg) = licPlate.rrLocationOfPlateInScene

        intPlateCenterX = int(intPlateCenterX)  # make sure center is an integer
        intPlateCenterY = int(intPlateCenterY)

        ptCenterOfTextAreaX = int(intPlateCenterX)  # the horizontal location of the text area is the same as the plate

        if intPlateCenterY < (sceneHeight * 0.75):  # if the license plate is in the upper 3/4 of the image
            ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(
                round(plateHeight * 1.6))  # write the chars in below the plate
        else:  # else if the license plate is in the lower 1/4 of the image
            ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(
                round(plateHeight * 1.6))  # write the chars in above the plate
        # end if

        textSizeWidth, textSizeHeight = textSize  # unpack text size width and height

        ptLowerLeftTextOriginX = int(
            ptCenterOfTextAreaX - (textSizeWidth / 2))  # calculate the lower left origin of the text area
        ptLowerLeftTextOriginY = int(
            ptCenterOfTextAreaY + (textSizeHeight / 2))  # based on the text area center, width, and height

        # write the text on the image
        cv2.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace,
                    fltFontScale, SCALAR_YELLOW, intFontThickness)

    # end function

    # Proses utama deteksi pelat nomor
    def searching(self, imgOriginalScene, loop):
        licenses = ""
        if imgOriginalScene is None:  # if image not read successfully
            print("error: image not read from file \n")  # print error message
            os.system("pause")
            return
            # end if
        listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)  # Deteksi kemungkinan plat nomor
        # time.sleep(0.1)
        listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)  # Deteksi karakter pada plat nomor
        # time.sleep(0.1)

        if (loop == False):
            cv2.imshow("imgOriginalScene", imgOriginalScene)

        if len(listOfPossiblePlates) == 0:
            if (loop == False):  # if no plates were found
                print("no license plates were detected\n")  # inform user no plates were found
        else:  # else
            # if we get in here list of possible plates has at leat one plate

            # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
            listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)
            # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
            licPlate = listOfPossiblePlates[0]
            plateThresh = licPlate.imgThresh
            #cv2.imshow("pelatThres", plateThresh)
            pixmap = QtGui.QPixmap('platthres.png')
            self.label_11.setPixmap(pixmap.scaled(130, 220, QtCore.Qt.KeepAspectRatio))

            pixmap2 = QtGui.QPixmap(plateThresh)
            self.label_12.setPixmap(pixmap2.scaled(130, 220, QtCore.Qt.KeepAspectRatio))
            if (loop == False):
                cv2.imshow("imgPlate", licPlate.imgPlate)  # show crop of plate and threshold of plate
                cv2.imshow("imgThresh", licPlate.imgThresh)

            if len(licPlate.strChars) == 0:  # if no chars were found in the plate
                if (loop == False):
                    print("no characters were detected\n")
                    return  # show message
                # end if

            drawRedRectangleAroundPlate(imgOriginalScene, licPlate)
            writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)
            print("ini coy", licPlate.strChars)
            licenses = licPlate.strChars
            # if ((licenses[0] and licenses[len(licenses)-1])  == ('0' or '1' or '2' or '3' or '4' or  '5' or '6' or '7' or '8' or '9')):
            #     licenses = ""
            #     print("license plate False !! \n and ")
            # draw red rectangle around plate
            # print (licenses)
            # print(licPlate)
            if (loop == False):
                print(
                    "license plate read from image = " + licPlate.strChars + "\n")  # write license plate text to std out
                # write license plate text on the image

            if (loop == False):

                cv2.imshow("imgOriginalScene", imgOriginalScene)  # re-show scene image
                cv2.imwrite("imgOriginalScene.png", imgOriginalScene)

        return imgOriginalScene, licenses

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(689, 635)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 351, 351))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.ImgWidget = QtWidgets.QLabel(self.groupBox)
        self.ImgWidget.setGeometry(QtCore.QRect(11, 24, 330, 190))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImgWidget.sizePolicy().hasHeightForWidth())
        self.ImgWidget.setSizePolicy(sizePolicy)
        self.ImgWidget.setMinimumSize(QtCore.QSize(330, 190))
        self.ImgWidget.setMaximumSize(QtCore.QSize(330, 190))
        self.ImgWidget.setObjectName("ImgWidget")
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(10, 251, 321, 81))
        self.widget.setObjectName("widget")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")

        self.label_11 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setMinimumSize(QtCore.QSize(128, 50))
        self.label_11.setMaximumSize(QtCore.QSize(128, 50))
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_13.addWidget(self.label_11)
        self.label_12 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMinimumSize(QtCore.QSize(128, 50))
        self.label_12.setMaximumSize(QtCore.QSize(128, 50))
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_13.addWidget(self.label_12)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(50, 230, 91, 16))
        self.label_5.setObjectName("label_5")
        self.label_16 = QtWidgets.QLabel(self.groupBox)
        self.label_16.setGeometry(QtCore.QRect(180, 230, 141, 16))
        self.label_16.setObjectName("label_16")

        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(370, 10, 301, 581))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName("gridLayout")
        self.labelFoto = QtWidgets.QLabel(self.groupBox_2)
        self.labelFoto.setGeometry(QtCore.QRect(10,23,281,200))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelFoto.sizePolicy().hasHeightForWidth())
        self.labelFoto.setSizePolicy(sizePolicy)
        self.labelFoto.setMaximumSize(QtCore.QSize(300, 200))
        self.labelFoto.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.labelFoto.setFrameShape(QtWidgets.QFrame.Box)
        self.labelFoto.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.labelFoto.setScaledContents(False)
        self.labelFoto.setAlignment(QtCore.Qt.AlignCenter)
        self.labelFoto.setObjectName("labelFoto")
        self.gridLayout.addWidget(self.labelFoto, 1, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.labelId = QtWidgets.QLabel(self.groupBox_2)
        self.labelId.setMinimumSize(QtCore.QSize(70, 0))
        self.labelId.setObjectName("labelId")
        self.horizontalLayout_4.addWidget(self.labelId)
        self.lineId = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineId.setFont(font)
        self.lineId.setReadOnly(True)
        self.lineId.setObjectName("lineId")
        self.horizontalLayout_4.addWidget(self.lineId)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.labelNamapemilik = QtWidgets.QLabel(self.groupBox_2)
        self.labelNamapemilik.setMinimumSize(QtCore.QSize(70, 0))
        self.labelNamapemilik.setObjectName("labelNamapemilik")
        self.horizontalLayout_5.addWidget(self.labelNamapemilik)
        self.lineNamapemilik = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineNamapemilik.setFont(font)
        self.lineNamapemilik.setReadOnly(True)
        self.lineNamapemilik.setObjectName("lineNamapemilik")
        self.horizontalLayout_5.addWidget(self.lineNamapemilik)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.labelNomorpolisi = QtWidgets.QLabel(self.groupBox_2)
        self.labelNomorpolisi.setMinimumSize(QtCore.QSize(70, 0))
        self.labelNomorpolisi.setObjectName("labelNomorpolisi")
        self.horizontalLayout_6.addWidget(self.labelNomorpolisi)
        self.lineNomorpolisi = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineNomorpolisi.setFont(font)
        self.lineNomorpolisi.setReadOnly(True)
        self.lineNomorpolisi.setObjectName("lineNomorpolisi")
        self.horizontalLayout_6.addWidget(self.lineNomorpolisi)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.labelKendaraan = QtWidgets.QLabel(self.groupBox_2)
        self.labelKendaraan.setMinimumSize(QtCore.QSize(70, 0))
        self.labelKendaraan.setObjectName("labelKendaraan")
        self.horizontalLayout_7.addWidget(self.labelKendaraan)
        self.lineKendaraan = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineKendaraan.setFont(font)
        self.lineKendaraan.setReadOnly(True)
        self.lineKendaraan.setObjectName("lineKendaraan")
        self.horizontalLayout_7.addWidget(self.lineKendaraan)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.labelJenis = QtWidgets.QLabel(self.groupBox_2)
        self.labelJenis.setMinimumSize(QtCore.QSize(70, 0))
        self.labelJenis.setObjectName("labelJenis")
        self.horizontalLayout_11.addWidget(self.labelJenis)
        self.lineJenis = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineJenis.setFont(font)
        self.lineJenis.setObjectName("lineJenis")
        self.horizontalLayout_11.addWidget(self.lineJenis)
        self.verticalLayout_2.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.labelTahun = QtWidgets.QLabel(self.groupBox_2)
        self.labelTahun.setMinimumSize(QtCore.QSize(70, 0))
        self.labelTahun.setObjectName("labelTahun")
        self.horizontalLayout_8.addWidget(self.labelTahun)
        self.lineTahun = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineTahun.setFont(font)
        self.lineTahun.setReadOnly(True)
        self.lineTahun.setObjectName("lineTahun")
        self.horizontalLayout_8.addWidget(self.lineTahun)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.labelKota = QtWidgets.QLabel(self.groupBox_2)
        self.labelKota.setMinimumSize(QtCore.QSize(70, 0))
        self.labelKota.setObjectName("labelKota")
        self.horizontalLayout_12.addWidget(self.labelKota)
        self.lineKota = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineKota.setFont(font)
        self.lineKota.setObjectName("lineKota")
        self.horizontalLayout_12.addWidget(self.lineKota)
        self.verticalLayout_2.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.labelStatus = QtWidgets.QLabel(self.groupBox_2)
        self.labelStatus.setMinimumSize(QtCore.QSize(70, 0))
        self.labelStatus.setObjectName("labelStatus")
        self.horizontalLayout_10.addWidget(self.labelStatus)
        self.lineStatus = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(12)

        self.lineStatus.setFont(font)
        self.lineStatus.setObjectName("lineStatus")
        self.horizontalLayout_10.addWidget(self.lineStatus)
        self.verticalLayout_2.addLayout(self.horizontalLayout_10)
        self.gridLayout.addLayout(self.verticalLayout_2, 2, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 370, 351, 221))
        self.groupBox_3.setObjectName("groupBox_3")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setGeometry(QtCore.QRect(90, 20, 181, 16))
        self.label.setObjectName("label")
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox_3)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 50, 311, 157))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelTanggal = QtWidgets.QLabel(self.layoutWidget1)
        self.labelTanggal.setMinimumSize(QtCore.QSize(60, 0))
        self.labelTanggal.setObjectName("labelTanggal")
        self.horizontalLayout.addWidget(self.labelTanggal)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget1)

        font = QtGui.QFont()
        font.setPointSize(12)

        self.lineEdit.setFont(font)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setMinimumSize(QtCore.QSize(60, 0))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.linePelat = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(12)

        self.linePelat.setFont(font)
        self.linePelat.setObjectName("linePelat")
        self.horizontalLayout_2.addWidget(self.linePelat)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.verticalLayout_3.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 689, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        date = QDate.currentDate()
        date_show = (date.toString(QtCore.Qt.DefaultLocaleLongDate))
        self.lineEdit.setText(date_show)

        self.linePelat.returnPressed.connect(self.fetchData)
        self.pushButton_3.clicked.connect(self.welcomeWindowShow)


        self.timer = QTimer()
        # set timer timeout callback function

        # set control_bt callback clicked  function





        #==========Crop Plat=========
       # pixmap = QtGui.QPixmap('platthres.png')
        #self.label_11.setPixmap(pixmap.scaled(130, 220, QtCore.Qt.KeepAspectRatio))

       # pixmap2 = QtGui.QPixmap('platthres.png')
        #self.label_12.setPixmap(pixmap2.scaled(130, 220, QtCore.Qt.KeepAspectRatio))

        # ==========Foto Muka Sementara=========
        #pixmap = QtGui.QPixmap('wajah.jpg')
        #self.labelFoto.setPixmap(pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio))



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Webcam"))
        self.label_11.setText(_translate("MainWindow", "CROP PELAT ORIGINAL"))
        self.label_12.setText(_translate("MainWindow", "CROP PLAT THRESHOLD"))
        self.label_5.setText(_translate("MainWindow", "Crop Pelat Nomor"))
        self.label_16.setText(_translate("MainWindow", "Crop Pelat Nomor Threshold"))

        self.groupBox_2.setTitle(_translate("MainWindow", "Data Kendaraan"))
        self.labelId.setText(_translate("MainWindow", "Id "))
        self.labelNamapemilik.setText(_translate("MainWindow", "Nama Pemilik "))
        self.labelNomorpolisi.setText(_translate("MainWindow", "Nomor Polisi"))
        self.labelKendaraan.setText(_translate("MainWindow", "Kendaraan"))
        self.labelJenis.setText(_translate("MainWindow", "Jenis"))
        self.labelTahun.setText(_translate("MainWindow", "Tahun"))
        self.labelKota.setText(_translate("MainWindow", "Kota"))
        self.labelStatus.setText(_translate("MainWindow", "Status"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Hasil"))
        self.label.setText(_translate("MainWindow", "DETEKSI PELAT NOMOR KENDARAAN"))
        self.labelTanggal.setText(_translate("MainWindow", "Tanggal "))
        self.label_3.setText(_translate("MainWindow", "Pelat Nomor "))


        self.pushButton_3.setText(_translate("MainWindow", "Database"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.main()
    sys.exit(app.exec_())

