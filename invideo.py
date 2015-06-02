#!/usr/bin/python
#-*- coding: utf-8 -*-

__author__ = 'mario'

from cv2 import *
import Tkinter
import tkFileDialog
import numpy
from MyGlobals import MyVidGlobals as mg
import copy
from functions import *


def distance(point1, point2):
    return numpy.sqrt(((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2))


def onMouseMove(event, x, y, flags, data):
    if event == EVENT_MOUSEMOVE:
        if data == 1: mg.p1 = (x,y)
        if data == 2: mg.p2 = (x,y)
        if data == 3: mg.p3 = (x,y)
        if data == 4: mg.p4 = (x,y)
        mg.vid1LastFrame = copy.copy(mg.vid1LastFrameClean)
        setPoints()
        imshow(mg.imgWindowName, mg.vid1LastFrame)
    elif event == EVENT_LBUTTONDOWN:
        setMouseCallback(mg.imgWindowName, onMouseClick)


def onMouseClick(event, x, y, flags, data):
    if event == EVENT_LBUTTONDOWN:
        if distance((x,y), mg.p1) < mg.circleRadius:
            setMouseCallback(mg.imgWindowName, onMouseMove, 1)
        if distance((x,y), mg.p2) < mg.circleRadius:
            setMouseCallback(mg.imgWindowName, onMouseMove, 2)
        if distance((x,y), mg.p3) < mg.circleRadius:
            setMouseCallback(mg.imgWindowName, onMouseMove, 3)
        if distance((x,y), mg.p4) < mg.circleRadius:
            setMouseCallback(mg.imgWindowName, onMouseMove, 4)
    if event != EVENT_MOUSEMOVE:
        mg.vid1LastFrame = copy.copy(mg.vid1LastFrameClean)
        setPoints()
        imshow(mg.imgWindowName, mg.vid1LastFrame)


def setPoints(start = False):
    if start:
        y,x,ret = mg.vid1LastFrame.shape
        mg.p1 = (x*1/3, y*1/3)
        mg.p2 = (x*2/3, y*1/3)
        mg.p3 = (x*1/3, y*2/3)
        mg.p4 = (x*2/3, y*2/3)
    line(mg.vid1LastFrame, mg.p1, mg.p2, (0, 255, 0), 2)
    line(mg.vid1LastFrame, mg.p2, mg.p4, (0, 255, 0), 2)
    line(mg.vid1LastFrame, mg.p4, mg.p3, (0, 255, 0), 2)
    line(mg.vid1LastFrame, mg.p3, mg.p1, (0, 255, 0), 2)
    circle(mg.vid1LastFrame, mg.p1, mg.circleRadius, (255,0,0), thickness=-1)
    circle(mg.vid1LastFrame, mg.p2, mg.circleRadius, (255,0,0), thickness=-1)
    circle(mg.vid1LastFrame, mg.p3, mg.circleRadius, (255,0,0), thickness=-1)
    circle(mg.vid1LastFrame, mg.p4, mg.circleRadius, (255,0,0), thickness=-1)


def getTransformed(frame, points = None):
    y,x = frame.shape[:2]
    src = numpy.array([(0,0), (x,0), (0,y), (x,y)], numpy.float32)
    if points == None:
        dst = numpy.array([mg.p1, mg.p2, mg.p3, mg.p4], numpy.float32)
    else:
        dst = numpy.array(points, numpy.float32)
    ret_img =  warpPerspective(frame,
                               getPerspectiveTransform(
                                   src,
                                   dst),
                               (mg.vid1LastFrame.shape[1], mg.vid1LastFrame.shape[0]))
    return ret_img


def refreshMask():
    mg.mask = numpy.zeros(mg.vid1LastFrame.shape[:2], numpy.uint8)
    circle(mg.mask, mg.p1, mg.maskRadius, 255, thickness=-1)
    circle(mg.mask, mg.p2, mg.maskRadius, 255, thickness=-1)
    circle(mg.mask, mg.p3, mg.maskRadius, 255, thickness=-1)
    circle(mg.mask, mg.p4, mg.maskRadius, 255, thickness=-1)


def corners():
    refreshMask()

    goodFeaturesToTrack(cvtColor(mg.previousFrameClean, COLOR_BGR2GRAY), 4, 0.1, 8, mask=mg.mask)
    crns = goodFeaturesToTrack(cvtColor(mg.vid1LastFrameClean, COLOR_BGR2GRAY), 4, 0.1, 8, useHarrisDetector=True)
    crns = numpy.int32(crns)
    mg.p1 = (crns[0][0][0], crns[0][0][1])
    mg.p2 = (crns[1][0][0], crns[1][0][1])
    mg.p3 = (crns[2][0][0], crns[2][0][1])
    mg.p4 = (crns[3][0][0], crns[3][0][1])


    # orb = ORB(4)
    # kp1, des1 = orb.detectAndCompute(cvtColor(mg.previousFrameClean, COLOR_BGR2GRAY), mg.mask)
    # kp2, des2 = orb.detectAndCompute(cvtColor(mg.vid1LastFrameClean, COLOR_BGR2GRAY), None)
    # des1 = numpy.float32(des1)
    # des2 = numpy.float32(des2)
    #
    # index_params = dict(algorithm = 0, trees = 5)
    # search_params = dict(checks=50)
    # flann = FlannBasedMatcher(index_params, search_params)
    # matches = flann.match(des1,des2)




def go():
    window = Tkinter.Tk()
    window.withdraw()
    window.wm_title("tk-okienko")

    mg.vid1 = VideoCapture(tkFileDialog.askopenfilename(title="Wybierz wideo zewnętrzne", filetypes=mg.videoTypes))
    mg.vid1LastFrame = mg.vid1.read()[1]
    mg.vid1LastFrameClean = numpy.copy(mg.vid1LastFrame)
    mg.vid2 = VideoCapture(tkFileDialog.askopenfilename(title="Wybierz wideo wewnętrzne", filetypes=mg.videoTypes))

    namedWindow(mg.imgWindowName)
    setPoints(True)
    setMouseCallback(mg.imgWindowName, onMouseClick)
    imshow(mg.imgWindowName, mg.vid1LastFrame)
    waitKey(0)
    setMouseCallback(mg.imgWindowName, lambda: None)

    while True:
        innerFrame = mg.vid2.read()[1]
        fillPoly(mg.vid1LastFrameClean, numpy.array([[mg.p1, mg.p2, mg.p4, mg.p3]]), (0,0,0))
        imshow("video", mg.vid1LastFrameClean+getTransformed(innerFrame))
        ret, mg.vid1LastFrame = mg.vid1.read()
        mg.vid1LastFrameClean = numpy.copy(mg.vid1LastFrame)
        mg.previousFrameClean = mg.vid1LastFrameClean
        corners()
        if not ret:
            break
        key = waitKey(30)
        if key%256 == 27:
            break





