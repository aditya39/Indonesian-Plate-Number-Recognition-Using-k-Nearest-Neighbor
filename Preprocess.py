# Preprocess.py

import cv2
import numpy as np
import math

# module level variables ##########################################################################
CAL_VAL = np.loadtxt("calibrated_value.txt")
(w ,h, rotationx, rotationy, rotationz, panX, panY, stretchX, dist, G_S_F_W, G_S_F_H, A_T_B, A_T_W, T_V, Xtrans, Ytrans) = np.loadtxt("calibrated_value.txt")
GAUSSIAN_SMOOTH_FILTER_SIZE = (5,5) #(int(G_S_F_W), int(G_S_F_H)) # last best = 3,3
ADAPTIVE_THRESH_BLOCK_SIZE = 19 #int(A_T_B) #19 , last best = 19
ADAPTIVE_THRESH_WEIGHT = 11   #int(A_T_W) #9, last best = 11
THRESHOLD_VALUE = int(T_V)
kernel = np.ones((2,2),np.uint8)
##
###################################################################################################
def preprocess(imgOriginal):

    imgGrayscale = extractValue(imgOriginal)
    #imgGrayscale = np.invert(imgGrayscale)

    imgMaxContrastGrayscale = maximizeContrast(imgGrayscale)
    #cv2.imshow("maxcontras", imgMaxContrastGrayscale)
    height, width = imgGrayscale.shape

    imgBlurred = np.zeros((height, width, 1), np.uint8)
    imgBlurred = cv2.GaussianBlur(imgMaxContrastGrayscale, GAUSSIAN_SMOOTH_FILTER_SIZE, 0)
    #cv2.imshow("Blur", imgBlurred)
    imgThresh = cv2.adaptiveThreshold(imgBlurred, THRESHOLD_VALUE , cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)
    #_,imgThresh = cv2.threshold(imgBlurred,0,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    #cv2.imshow("imgThresh",imgThresh)
    imgThresh = cv2.morphologyEx(imgThresh,cv2.MORPH_OPEN,kernel,iterations=1)
    #imgThresh = cv2.morphologyEx(imgThresh,cv2.MORPH_OPEN,kernel)
    return imgGrayscale, imgThresh
# end function

###################################################################################################
def extractValue(imgOriginal):
    height, width, numChannels = imgOriginal.shape

    imgHSV = np.zeros((height, width, 3), np.uint8)

    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

    imgHue, imgSaturation, imgValue = cv2.split(imgHSV)

    return imgValue
# end function

###################################################################################################
def maximizeContrast(imgGrayscale):

    height, width = imgGrayscale.shape

    imgTopHat = np.zeros((height, width, 1), np.uint8)
    imgBlackHat = np.zeros((height, width, 1), np.uint8)

    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    imgTopHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_TOPHAT, structuringElement)
    imgBlackHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_BLACKHAT, structuringElement)

    imgGrayscalePlusTopHat = cv2.add(imgGrayscale, imgTopHat)
    imgGrayscalePlusTopHatMinusBlackHat = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

    return imgGrayscalePlusTopHatMinusBlackHat
# end function
