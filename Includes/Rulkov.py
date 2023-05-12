class Rulkov:
    def __init__(self):
        self.x = []
        self.y = []
        self.alpha = 0
        self.beta = 0
        self.sigma = 0
        self.cells = 1
        self.W = 0
        self.x0 = 0
        self.y0 = 0
        self.N = 0
        self.noiseDev = 0
        self.threshold = 0.5

    def RulkovSimple(self, alpha=None, beta=None, sigma=None, x0=None, y0=None, N=None):
        if alpha != None:
            self.alpha = alpha
        if beta != None:
            self.beta = beta
        if sigma != None:
            self.sigma = sigma
        if x0 != None:
            self.x0 = x0
        if y0 != None:
            self.y0 = y0
        if N != None:
            self.N = int(N)
        NCO = int(self.N*1.1)
        self.x = [0]*NCO
        self.x[0] = self.x0
        self.y = [0]*NCO
        self.y[0] = self.y0
        NI = range(1, NCO-1)
        for n in NI:
            self.x[n] = (self.alpha/(1+(self.x[n-1])**2))+self.y[n-1]
            self.y[n] = self.y[n-1]-self.sigma*self.x[n-1]-self.beta
        tempx = self.x[0:self.N]
        tempy = self.y[0:self.N]
        self.x = [0 for _ in range(1)]
        self.y = [0 for _ in range(1)]
        self.x[0] = tempx
        self.y[0] = tempy
        return (self.x, self.y)

    def ChangeParameterRulkovSimple(self, par, value):
        match par:
            case "alpha":
                self.RulkovSimple(alpha=value)
            case "beta":
                self.RulkovSimple(beta=value)
            case "sigma":
                self.RulkovSimple(sigma=value)
            case "x0":
                self.RulkovSimple(x0=value)
            case "y0":
                self.RulkovSimple(y0=value)
            case "N":
                self.RulkovSimple(N=value)
        return self.SpikePlots()

    def RulkovCoupled(self, alpha=None, sigma=None, cells=None, W=None, x0=None, y0=None, N=None):
        if alpha != None:
            self.alpha = alpha
        if sigma != None:
            self.sigma = sigma
        if cells != None:
            self.cells = cells
        if W != None:
            self.W = W
        if x0 != None:
            self.x0 = x0
        if y0 != None:
            self.y0 = y0
        if N != None:
            self.N = int(N)
        NCO = int(self.N*1.1)
        self.x = [[0 for _ in range(NCO)] for _ in range(self.cells)]
        for X in self.x: X[0] = self.x0
        self.y = [[0 for _ in range(NCO)] for _ in range(self.cells)]
        for Y in self.y: Y[0] = self.y0
        C = range(0, self.cells)
        I = range(0, self.cells)
        N = range(1, NCO-1)
        W = [[0 for _ in range(self.cells)] for _ in range(self.cells)]
        for i in range(0, self.cells):
            W[i][self.cells - 1 - i] = self.W
        for n in N:
            for c in C:
                for i in I:
                    sigma_n = self.sigma * W[i][c] * self.x[i][n-1]

                    self.x[c][n] = (self.alpha/(1+(self.x[c][n-1])**2))+self.y[c][n-1]
                    self.y[c][n] = self.y[c][n-1]-sigma_n*self.x[c][n-1]-self.beta

        for i in range(self.cells):
            self.x[i] = self.x[i][0:self.N]
            self.y[i] = self.y[i][0:self.N]
        return (self.x, self.y)

    def ChangeParameterRulkovCoupled(self, par, value):
        match par:
            case "alpha":
                self.RulkovCoupled(alpha=value)
            case "sigma":
                self.RulkovCoupled(sigma=value)
            case "cells":
                self.RulkovCoupled(cells=value)
            case "W":
                self.RulkovCoupled(W=value)
            case "x0":
                self.RulkovCoupled(x0=value)
            case "y0":
                self.RulkovCoupled(y0=value)
            case "N":
                self.RulkovCoupled(N=value)
        return self.SpikePlots()
    
    def SpikePlots(self):       
        plots = []
        for cell in range(self.cells):
            plots.append([[i for i in range(self.N)], self.x[cell]])
            plots.append([[i for i in range(self.N)], self.y[cell]])
        return plots
    
    def CountSpikes(self, noiseDev=None, threshold=None):
        if noiseDev != None:
            self.noiseDev = noiseDev
        if threshold != None:
            self.threshold = threshold

        self.RulkovSimple()

        (iSignal, signal) = self.SpikePlots()[0]

        (iNoisedSignal, noisedSignal) = self.AddNoiseToSignal(iSignal, signal, self.noiseDev)

        self.x[0] = noisedSignal

        return self.DetectSpikes(iNoisedSignal, noisedSignal, self.threshold)
    
    def SpikesIntervals(self):
        (timedData, _) = self.CountSpikes()
        intervals = [timedData[n + 1] - timedData[n] for n in range(len(timedData) - 1)]
        return intervals
    
    def DetectSpikes(self, index, signal, threshold):
        (iDiffSignal, diffSignal) = self.DifferenciateSignal(index, signal)
        iTimedSignal=[]
        for n in range(len(iDiffSignal) - 1):
            if diffSignal[n]>0 and diffSignal[n+1]<0:
                if signal[n+1]>threshold:
                    iTimedSignal.append(iDiffSignal[n] + iDiffSignal[0])
        maxSignalVal = max(signal)
        timedData = [iTimedSignal, [maxSignalVal for _ in range(len(iTimedSignal))]]
        return timedData
    
    def DifferenciateSignal(self, index, signal):
        iDiffSignal = [index[n] + (index[n + 1] - index[n])/2 for n in range(len(index) - 1)]
        diffSignal = [signal[n + 1] - signal[n] for n in range(len(iDiffSignal))]
        return [iDiffSignal, diffSignal]

    def AddNoiseToSignal(self, index, signal, noiseDev):
        import numpy as np
        N = len(signal)
        noise = np.random.normal(0, noiseDev, N)
        iNoisedSignal = index
        noisedSignal = [signal[n] + noise[n] for n in range(N)]
        return [iNoisedSignal, noisedSignal]

    def ChangeParameterCountSpikes(self, par, value):
        ret = []
        match par:
            case "noiseDev":
                ret = self.CountSpikes(noiseDev=value)
            case "threshold":
                ret = self.CountSpikes(threshold=value)
        return [self.SpikePlots()[0], ret]