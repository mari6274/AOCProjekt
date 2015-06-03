__author__ = 'mario'

class MyVidGlobals(object):
    vid1LastFrame = None
    vid1LastFrameClean = None
    previousFrameClean = None
    vid1 = None
    imgWindowName = "okno"
    p1 = None
    p2 = None
    p3 = None
    p4 = None
    circleRadius = 4
    vid2 = None
    mask = None
    maskRadius = 16
    videoTypes = [("video files", ("*.m4v", "*.mp4", "*.avi"))]

class MyImgGlobals(object):
    imgWindowName = "okno"
    img = None
    backup = None
    vid = None
    p1 = None
    p2 = None
    p3 = None
    p4 = None
    circleRadius = 4
    imageTypes = [("images", ("*.jpg", "*.jpeg", "*.png"))]
    videoTypes = [("video files", ("*.m4v", "*.mp4", "*.avi"))]

