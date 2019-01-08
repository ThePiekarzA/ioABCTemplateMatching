# This class represents a single solution of an ABC algorithm
import cv2
import utils
import numpy as np
class Solution:
    # <editor-fold desc="Parameter set">
    # Optimised parameters
    x = 0  # row of the image
    y = 0  # column if the image
    angle = 0 # rotation in radians (0, 359)
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
        # Rotate object image to the solution angle

        rotatedObject = utils.rotate_bound(imgObj, self.angle)

        # Calculate size of an object image
        xSize = rotatedObject.shape[1]
        ySize = rotatedObject.shape[0]

        # Cut image from imgRef to compare with imgObj
        imgCmp = imgRef[self.y-ySize//2:self.y+ySize//2, self.x-xSize//2:self.x+xSize//2]

        # Fitness is defined as sum of differences between histograms of each level of RGB
        tempFitness = self.compare2(rotatedObject, imgCmp)

        self.fitness = -tempFitness

    def compare1(self, imgObj, imgCmp):
        tempFitness = 0
        for level in range(3):
            # Calculate histograms
            histCmp = cv2.calcHist([imgCmp], [level], None, [256], [0, 256])
            histObj = cv2.calcHist([imgObj], [level], None, [256], [0, 256])

            # Calculate fitness as absolute difference between histograms
            tempFitness += int(sum(sum(abs(histCmp - histObj))))

        return tempFitness

    def compare2(self, imgObj, imgCmp):
        tempFitness = 0
        for level in range(3):
            # Calculate histograms
            histCmp = cv2.calcHist([imgCmp], [level], None, [256], [0, 256])
            histObj = cv2.calcHist([imgObj], [level], None, [256], [0, 256])

            histDif = abs(histCmp - histObj)

            # Use normal distribution to focus on object in center
            #mask = np.random.normal(0, 1, histDif.shape)
            mask = utils.matlab_style_gauss2D(shape=histDif.shape, sigma=1)
            mask = mask * ( histDif.shape[0] * histDif.shape[1] )

            histFiltered = np.multiply(histDif, mask)

            # Calculate fitness as absolute difference between histograms
            tempFitness += int(sum(sum(histFiltered)))

        return tempFitness

