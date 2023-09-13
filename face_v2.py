from imutils import face_utils
import numpy as np
import cv2 as cv
import dlib


cam = cv.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
scale = 3
fname = input("имя файла")
scl = int(input("масштаб (натурально число)"))


def draw_mask(fname, scl,  yl, xl):
    mask = cv.imread(fname)
    c = mask.copy()
    c = cv.resize(c, (c.shape[1]//scl, c.shape[0]//scl))
    maskHSV = cv.cvtColor(c, cv.COLOR_BGR2HSV)
    pattern = cv.inRange(maskHSV, (0, 0, 252), (255, 255, 255))
    maskInvoke = cv.bitwise_and(c, c, mask=cv.bitwise_not(pattern))
    # выше - генерация маски изображения в maskInvoke с помощью побитовых масок

    tmp = frame[yl-c.shape[0]//2:yl-c.shape[0]//2+c.shape[0],
                xl-c.shape[1]//2:xl-c.shape[1]//2+c.shape[1]]  # заменяемый фрагмент

    res = cv.add(tmp, maskInvoke)  # наложение
    frame[yl-c.shape[0]//2:yl-c.shape[0]//2+c.shape[0],
          xl-c.shape[1]//2:xl-c.shape[1]//2+c.shape[1]] = res  # замена на потоке

    # cv.circle(frame,(xl, yl),2,(0,0,0),-1) # точка


key = 0
while key != 32:
    frame = cam.read()[1]
    frame = cv.flip(frame, 2)
    frameCopy = cv.resize(
        frame, (frame.shape[1]//scale, frame.shape[0]//scale))
    frameGray = cv.cvtColor(frameCopy, cv.COLOR_BGR2GRAY)
    faces = detector(frameGray, 1)
    for (i, rect) in enumerate(faces):
        shape = predictor(frameGray, rect)
        shape = face_utils.shape_to_np(shape)
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        try:
            draw_mask(fname, scl, shape[51][1]*scale, shape[51][0]*scale)
        except Exception:
            pass

    cv.imshow('camera', frame)
    key = cv.waitKey(1)
cam.release()
cv.destroyAllWindows()
