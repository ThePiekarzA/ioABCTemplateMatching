# This class represents a single solution of an ABC algorithm
import cv2

class Solution:
    # <editor-fold desc="Parameter set">
    # Optimised parameters
    x = 0  # row of the image
    y = 0  # column if the image
    angle = 0 # rotation in radians (0, 360)
    # scale and rotation in future phase

    # Other parameters
    fitness = 0
    probability = 0

    # </editor-fold>

    # Solution constructor
    def __init__(self, _x, _y, _angle):
        self.x = _x
        self.y = _y
        self.angle = _angle

    def calculateFitness(self, imgRef, imgObj):
        # Calculate size of an object image
        xSize = imgObj.shape[1]
        ySize = imgObj.shape[0]

        # Cut image from imgRef to compare with imgObj
        imgCmp = imgRef[self.y-ySize//2:self.y+ySize//2, self.x-xSize//2:self.x+xSize//2]

        # Fitness is defined as sum of differences between histograms of each level of RGB
        tempFitness = 0

        for level in range(3):
            # Calculate histograms
            histCmp = cv2.calcHist([imgCmp], [level], None, [256], [0, 256])
            histObj = cv2.calcHist([imgObj], [level], None, [256], [0, 256])

            # Calculate fitness as absolute difference between histograms
            tempFitness += int(sum(abs(histCmp - histObj)))

        self.fitness = -tempFitness
