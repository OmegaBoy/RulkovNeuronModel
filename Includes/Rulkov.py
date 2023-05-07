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
            plots.append(([i for i in range(self.N)], self.x[cell]))
            plots.append(([i for i in range(self.N)], self.y[cell]))
        return plots
    
    def CountSpikes(self, noiseDev=None, threshold=None):
        if noiseDev != None:
            self.noiseDev = noiseDev
        if threshold != None:
            self.threshold = threshold
        import numpy as np
        noise = np.random.normal(0,self.noiseDev,self.N)
        self.RulkovSimple()
        data = self.SpikePlots()
        iSignal = data[0][0]
        signal = data[0][1]
        iNoisedSignal = iSignal
        noisedSignal = [signal[n] + noise[n] for n in range(self.N)]
        self.x[0] = noisedSignal
        iDiffSignal = [iNoisedSignal[n] + (iNoisedSignal[n + 1] - iNoisedSignal[n])/2 for n in range(len(iNoisedSignal) - 1)]
        diffSignal = [noisedSignal[n + 1] - noisedSignal[n] for n in range(len(iDiffSignal))]
        iDiffDiffSignal = [iDiffSignal[n] + (iDiffSignal[n + 1] - iDiffSignal[n])/2 for n in range(len(iDiffSignal) - 1)]
        diffDiffSignal = [diffSignal[n + 1] - diffSignal[n] for n in range(len(iDiffDiffSignal))]
        iTimedSignal=[]
        direction=0
        for n in range(len(iDiffDiffSignal)):
            if direction==0 and abs(diffDiffSignal[n]) > self.threshold:
                direction=diffDiffSignal[n]/abs(diffDiffSignal[n])
            else:
                if direction!=0 and diffDiffSignal[n] > self.threshold*direction:
                    iTimedSignal.append(iDiffDiffSignal[n] - iDiffDiffSignal[0])
                    direction=0

        return [iTimedSignal, [max(signal) for n in range(len(iTimedSignal))], "o"]
    
    def ChangeParameterCountSpikes(self, par, value):
        ret = []
        match par:
            case "noiseDev":
                ret = self.CountSpikes(noiseDev=value)
            case "threshold":
                ret = self.CountSpikes(threshold=value)
        return [self.SpikePlots()[0], ret]