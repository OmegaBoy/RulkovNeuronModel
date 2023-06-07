class RulkovCoupled:
    def __init__(self, alpha=None, sigma=None, cells=None, W=None, x0=None, y0=None, N=None):
        from Utilities import Utilities

        self.alpha = Utilities.ChangeParameter(alpha, self.alpha, "alpha")
        self.sigma = Utilities.ChangeParameter(sigma, self.sigma, "sigma") # 
        self.cells = Utilities.ChangeParameter(cells, self.cells, "cells") # Nro de celulas
        self.W = Utilities.ChangeParameter(W, self.W, "W") # Pesos neuronales
        self.x0 = Utilities.ChangeParameter(x0, self.x0, "x0")
        self.y0 = Utilities.ChangeParameter(y0, self.y0, "y0")
        self.N = Utilities.ChangeParameter(N, self.N, "N") # Cantidad de iteraciones 

        self.Simulate()

    def Simulate(self):
        self.x = []
        self.y = []
        
        self.NCO = int(self.N*1.1)
        self.x = [[0 for _ in range(self.NCO)] for _ in range(self.cells)]
        for X in self.x: X[0] = self.x0
        self.y = [[0 for _ in range(self.NCO)] for _ in range(self.cells)]
        for Y in self.y: Y[0] = self.y0
        self.C = range(0, self.cells)
        self.I = range(0, self.cells)
        self.N = range(1, self.NCO-1)
        self.W = [[0 for _ in range(self.cells)] for _ in range(self.cells)]

        for i in range(0, self.cells):
            self.W[i][self.cells - 1 - i] = self.W
        for n in self.N:
            for c in self.C:
                for i in self.I:
                    #sigma_n = self.sigma * self.W[i][c] * self.x[i][n-1]


                    self.x[c][n] = (self.alpha/(1+(self.x[c][n-1])**2))+self.y[c][n-1]
                    self.y[c][n] = self.y[c][n-1]-sigma_n*self.x[c][n-1]-self.beta

                    # cambian sigma y beta
                    #sigma(c)  = (x(c)(n) - x(c+1)(n)) * sigma(c)(n-1) * w(c)(c+1)//peso entre las dos c beta es igual


        for i in range(self.cells):
            self.x[i] = self.x[i][0:self.N]
            self.y[i] = self.y[i][0:self.N]