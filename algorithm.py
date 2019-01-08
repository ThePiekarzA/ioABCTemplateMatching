# ABC class implements Artificial Bee Colony algorithm for image template matching
from __future__ import division

from solution import Solution
from random import randint
import numpy as np
from visual import Visualize
from plot import Plot

class ABC:
    # <editor-fold desc="Parameter set">
    # Algorithm parameters
    SN = 0  # number of solutions (size of colony)
    MCN = 0  # maximum cycle number
    SLT = 0 # solution lifetime (in cycles)

    NSN = 0 # number of solutions created in neighborhood
    NS = 0 # neighborhood size (radius)

    EBN = 0 # employed bees number
    OBN = 0 # onlooker bees number
    SBN = 0 # scout bees number

    # Solutions set
    solutions = []
    bestSolution = None

    # Images
    imgRef = []
    imgObj = []

    # Constraints
    xCon = 0  # number of ref image columns
    yCon = 0  # number of ref image rows

    xObj = 0  # number of searched image columns
    yObj = 0  # number of searched image rows

    # scale and rotation constraints in future phase

    showGUI = False
    visualize = None
    showLog = False
    showPlot = False
    plot = None


    # </editor-fold>

    # Initialization of ABC class
    # parameters setup etc.
    def __init__(self, _imgRef, _imgObj, _SN=100, _MCN=100, _SLT=20, _NSN=5, _NS=10):
        self.SN = _SN
        self.MCN = _MCN
        self.SLT = _SLT

        self.NSN = _NSN
        self.NS = _NS

        self.EBN = int(0.5*_SN)
        self.OBN = int(0.5*_SN)
        self.SBN = 0

        self.imgRef = _imgRef
        self.imgObj = _imgObj

        self.xCon = _imgRef.shape[1]
        self.yCon = _imgRef.shape[0]

        self.xObj = self.imgObj.shape[1]
        self.yObj = self.imgObj.shape[0]



    def settings(self, _showGUI=False, _showLog=False, _showPlot=False):
        self.showGUI = _showGUI
        self.showLog = _showLog
        self.showPlot = _showPlot

        if self.showPlot:
            self.plot = Plot(self.MCN)

        if self.showGUI:
            self.visualize = Visualize(self.imgRef)
            self.visualize.refresh()


    # Main algorithm loop
    def run(self):
        CCN = 0  # Current cycle number

        # initialization phase
        self.initColony()

        self.showBees(self.solutions)

        self.calculateFitness()
        self.findBestSolution()
        print("Init best pos({}, {}), fitness: {}".format(self.bestSolution.x,
                                                          self.bestSolution.y,
                                                          self.bestSolution.fitness))

        # main loop phase
        while CCN < self.MCN:
            self.calculateFitness()

            self.searchNeighborhood()

            self.showBees(self.solutions)

            self.calculateProbability()

            self.onlookersPhase()

            self.showBees(self.solutions)

            self.scoutPhase()

            self.showBees(self.solutions)

            self.calculateFitness()
            self.findBestSolution()

            self.abandonSolutions()

            CCN += 1
            print("Iteration {} best pos({}, {}, {}\u00b0), fitness: {}".format(CCN,
                                                                        self.bestSolution.x,
                                                                        self.bestSolution.y,
                                                                        self.bestSolution.angle,
                                                                        self.bestSolution.fitness))

            if self.showPlot:
                self.plot.drawPoint(-1 * self.bestSolution.fitness)

            if self.showGUI:
                self.visualize.refresh()

        if self.showGUI:
            self.visualize.wait()



    # Algorithm functions (phases)
    def createRandomSolution(self):
        return Solution(
            randint(self.xObj // 2, self.xCon - self.xObj // 2),
            randint(self.yObj // 2, self.yCon - self.yObj // 2),
            randint(0, 359))


    # Initialize population
    def initColony(self):
        # Create SN number of random solutions
        for i in range(self.EBN):
            self.solutions.append(self.createRandomSolution())


    # Evaluate fitness of each solution and allocate them to correct groups
    def calculateFitness(self):
        for sol in self.solutions:
            sol.calculateFitness(self.imgRef, self.imgObj)

    def createNeighbor(self, sol):
        x = 0
        y = 0
        # pick new coordinates in neighborhood of current ones
        # and check if they fit in ref image
        clamp = lambda n, minN, maxN: max(min(maxN, n), minN)

        x = randint(sol.x - self.NS, sol.x + self.NS)
        x = clamp(x, self.xObj // 2, self.xCon - self.xObj // 2)

        y = randint(sol.y - self.NS, sol.y + self.NS)
        y = clamp(y, self.yObj // 2, self.yCon - self.yObj // 2)

        angle = randint(sol.angle - 50, sol.angle + 50)
        angle = clamp(angle, 0, 359)

        return Solution(x, y, angle)

    # Create neighborhood of current positions
    def searchNeighborhood(self):
        # iterate through known solutions
        for idx, sol in enumerate(self.solutions):
            # create NSN number of neighborhood solutions
            for i in range(self.NSN):
                neighbor = self.createNeighbor(sol)

                # evaluate neighbor fitness
                neighbor.calculateFitness(self.imgRef, self.imgObj)

                # if neighbor is better, chose it as solution
                if neighbor.fitness > sol.fitness:
                    self.solutions[idx] = neighbor


    # Calculate probabilities for the solutions
    def calculateProbability(self):
        sumFitness = 0
        minFitness = 0
        for sol in self.solutions:
            sumFitness += sol.fitness
            if sol.fitness < minFitness:
                minFitness = sol.fitness

        bias = -minFitness*2
        sumFitness += bias * len(self.solutions)

        for sol in self.solutions:
            sol.probability = (sol.fitness + bias) / sumFitness


    # Create new solutions for onlookers based on probability
    def onlookersPhase(self):
        newSolutions = self.solutions.copy()
        abandonedSolutions = []


        probabilities = [sol.probability for sol in self.solutions]
        choices = []



        for i in range(self.OBN):
            # choice index of solution based on probabilities
            choice = np.random.choice(len(self.solutions), 1, p=probabilities)[0]


            # create neighbor of chosen solution
            neighbor = self.createNeighbor(self.solutions[choice])

            # evaluate neighbor fitness
            neighbor.calculateFitness(self.imgRef, self.imgObj)

            # if neighbor is better, chose it as solution
            # if not, abandon it and turn employed bee into scout
            if neighbor.fitness > self.solutions[choice].fitness:
                newSolutions.append(neighbor)
                choices.append(choice)
            # else:
            #     abandonedSolutions.append(choice)
            #     self.SBN += 1

        # self.solutions = []
        # for idx in range(self.EBN):
        #     if idx not in abandonedSolutions:
        #         self.solutions.append(newSolutions[idx])

        for idx, sol in enumerate(self.solutions):
            if idx in choices:
                newSolutions.append(sol)

        self.solutions = []
        self.EBN = 0

        for sol in newSolutions:
            self.solutions.append(sol)
            self.EBN += 1

        print("Solutions number: {}".format(len(self.solutions)))

        self.SBN = self.SN - self.EBN


    # Create new random solutions for unemployed bees
    def scoutPhase(self):
        for i in range(self.SBN):
            self.solutions.append(self.createRandomSolution())

    # Return best solution
    def findBestSolution(self):
        self.solutions.sort(key=lambda x: x.fitness)

        if self.bestSolution is None:
            self.bestSolution =  self.solutions[-1]
        elif self.bestSolution.fitness < self.solutions[-1].fitness:
            self.bestSolution = self.solutions[-1]


    def abandonSolutions(self):
        self.solutions = self.solutions[self.SN//2:]

    def showBees(self, beeList):
        if self.showGUI:
            self.visualize.clear()
            for sol in beeList:
                self.visualize.drawPoint(sol.x, sol.y, sol.angle)
            self.visualize.refresh()








