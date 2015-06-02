#!/usr/bin/python
#-*- coding: utf-8 -*-

__author__ = 'mario'

from cv2 import *
import Tkinter
import tkFileDialog
import numpy
from MyGlobals import MyImgGlobals as mg
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
        mg.img = copy.copy(mg.backup)
        setPoints()
        imshow(mg.imgWindowName, mg.img)
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
        mg.img = copy.copy(mg.backup)
        setPoints()
        imshow(mg.imgWindowName, mg.img)


def setPoints(start = False):
    if start:
        y,x,ret = mg.img.shape
        mg.p1 = (x*1/3, y*1/3)
        mg.p2 = (x*2/3, y*1/3)
        mg.p3 = (x*1/3, y*2/3)
        mg.p4 = (x*2/3, y*2/3)
    line(mg.img, mg.p1, mg.p2, (0, 255, 0), 2)
    line(mg.img, mg.p2, mg.p4, (0, 255, 0), 2)
    line(mg.img, mg.p4, mg.p3, (0, 255, 0), 2)
    line(mg.img, mg.p3, mg.p1, (0, 255, 0), 2)
    circle(mg.img, mg.p1, mg.circleRadius, (255,0,0), thickness=-1)
    circle(mg.img, mg.p2, mg.circleRadius, (255,0,0), thickness=-1)
    circle(mg.img, mg.p3, mg.circleRadius, (255,0,0), thickness=-1)
    circle(mg.img, mg.p4, mg.circleRadius, (255,0,0), thickness=-1)


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
                               (mg.img.shape[1], mg.img.shape[0]))
    return ret_img


def go():
    window = Tkinter.Tk()
    window.withdraw()
    window.wm_title("tk-okienko")

    mg.img = imread(tkFileDialog.askopenfilename(title="Wybierz obraz zewnętrzny", filetypes=mg.imageTypes))
    mg.vid = VideoCapture(tkFileDialog.askopenfilename(title="Wybierz wideo wewnętrzne", filetypes=mg.videoTypes))
    mg.backup = copy.copy(mg.img)

    namedWindow(mg.imgWindowName)
    setPoints(True)
    setMouseCallback(mg.imgWindowName, onMouseClick)
    imshow(mg.imgWindowName, mg.img)
    waitKey(0)
    setMouseCallback(mg.imgWindowName, lambda: None)

    while True:
        innerFrame = mg.vid.read()[1]
        mg.img = copy.copy(mg.backup)
        fillPoly(mg.img, numpy.array([[mg.p1, mg.p2, mg.p4, mg.p3]]), (0,0,0))
        imshow("video", mg.img+getTransformed(innerFrame))
        key = waitKey(30)
        if key%256 == 27:
            break





