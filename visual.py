# This class implements algorithm data visualizer

import cv2
import numpy as np

class Visualize:
    def __init__(self, _img):
        self.img = _img

        self.drawnImg = self.img.copy()

        self.arrowLength = 40

        self.thickness = 2
        self.color = (0,0,255)

        self.scale = 8

        # Shrink image if too big
        if self.img.shape[1] > 1000 or self.img.shape[0] > 800:
            proportion = self.img.shape[0] / self.img.shape[1]
            self.drawnImg = cv2.resize(self.drawnImg, (1000, int(1000*proportion)))
        cv2.imshow("ABC", self.drawnImg)
        cv2.waitKey(0)


    # Refresh image with drawn points
    def refresh(self):
        if self.img.shape[1] > 800 or self.img.shape[0] > 600:
            proportion = self.img.shape[0] / self.img.shape[1]
            self.drawnImg = cv2.resize(self.drawnImg, (1000, int(1000 * proportion)))
            #self.drawnImg = cv2.resize(self.drawnImg, (1000, 600))
        cv2.imshow("ABC", self.drawnImg)
        cv2.waitKey(100)
        #cv2.destroyAllWindows()

    # Draw point on image
    def drawPoint(self, x, y, angle, _color=(255,0,0)):
        angle = 360 - angle + 90
        radAngle = angle*np.pi/180

        xEnd = int(np.cos(radAngle) * self.arrowLength) + x
        yEnd = -int(np.sin(radAngle) * self.arrowLength) + y

        cv2.arrowedLine(self.drawnImg, (x,y), (xEnd,yEnd), _color, thickness=self.thickness)


    def clear(self):
        self.drawnImg = self.img.copy()

    def wait(self):
        cv2.waitKey(0)
