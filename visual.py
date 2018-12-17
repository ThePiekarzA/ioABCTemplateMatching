# This class implements algorithm visualizer

import cv2
import numpy as np

class Visualize:
    def __init__(self, _img):
        self.img = _img

        self.drawnImg = self.img.copy()

        self.fontFace = cv2.FONT_HERSHEY_SIMPLEX
        self.fontScale = 0.2
        self.thickness = 2
        self.marker = 'o'
        self.color = (0,0,255)

        self.scale = 8

        if self.img.shape[1] > 800 or self.img.shape[0] > 600:
            self.drawnImg = cv2.resize(self.drawnImg, (1000, 600))
        cv2.imshow("ABC", self.drawnImg)
        cv2.waitKey(0)


    def refresh(self):
        if self.img.shape[1] > 800 or self.img.shape[0] > 600:
            self.drawnImg = cv2.resize(self.drawnImg, (1000, 600))
        cv2.imshow("ABC", self.drawnImg)
        cv2.waitKey(100)
        #cv2.destroyAllWindows()

    def drawPoint(self, x, y):
        textSize = cv2.getTextSize(self.marker, self.fontFace, self.fontScale, self.thickness)

        cv2.putText(self.drawnImg,
                    self.marker,
                    (x - textSize[0][0]//2, y - textSize[0][1]//2),
                    self.fontFace*self.scale,
                    self.fontScale*self.scale,
                    self.color,
                    self.thickness*self.scale)

    def clear(self):
        self.drawnImg = self.img.copy()
