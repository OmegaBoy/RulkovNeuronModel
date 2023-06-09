class RulkovCoupled:
    def __init__(self, alpha=None, sigma=None, beta=None, cells=None, W=None, x0=None, y0=None, N=None):
        from Utilities import Utilities

        Utilities.ChangeParameter(alpha, self, "alpha") # Parametro Alpha
        Utilities.ChangeParameter(sigma, self, "sigma") # Parametro Sigma
        Utilities.ChangeParameter(beta, self, "beta") # Parametro Beta
        Utilities.ChangeParameter(cells, self, "cells") # Nro de celulas
        Utilities.ChangeParameter(W, self, "W") # Pesos neuronales
        Utilities.ChangeParameter(x0, self, "x0") # Punto de inicio en X
        Utilities.ChangeParameter(y0, self, "y0") # Punto de inicio en Y
        Utilities.ChangeParameter(N, self, "N") # Cantidad de iteraciones 

        self.Simulate()

    def Simulate(self):
        self.x = []
        self.y = []
        
        self.NCO = int(self.N*1.1) # Numero de pasos con un 10% mas para descartar el borde
        self.x = [[0 for _ in range(self.NCO)] for _ in range(self.cells)] # Matriz inicial de X
        for X in self.x: X[0] = self.x0 # Seteo X0 en el primero de los X
        self.y = [[0 for _ in range(self.NCO)] for _ in range(self.cells)]  # Matriz inicial de Y
        for Y in self.y: Y[0] = self.y0 # Seteo Y0 en el primero de los X
        self.I = range(0, self.cells) # Indice de Celula
        self.J = range(0, self.cells) # Indice de Celula Vecina
        self.NI = range(1, self.NCO-1) # Numero de Pasos
        self.WI = [[0 for _ in range(self.cells)] for _ in range(self.cells)] # Matriz inicial de pesos
        self.betaI = [[0 for _ in range(self.NCO)] for _ in range(self.cells)] # Matriz inicial de Beta
        for bi in self.betaI: bi[0] = self.beta # Seteo alpha en el primero de los Beta
        self.sigmaI = [[0 for _ in range(self.NCO)] for _ in range(self.cells)] # Matriz inicial de Sigma
        for si in self.sigmaI: si[0] = self.sigma # Seteo alpha en el primero de los Alpha

        # Seteo los pesos en todo menos la diagonal (Con si misma) en 0
        for i in range(0, self.cells):
            self.WI[i][self.cells - 1 - i] = self.W

        for n in self.NI:
            for i in self.I:
                for j in self.J:
                    self.x[i][n] = (self.alpha/(1+(self.x[i][n-1])**2))+self.y[i][n-1]
                    self.y[i][n] = self.y[i][n-1]-self.sigmaI[i][n-1]*self.x[i][n-1]-self.betaI[i][n-1]

                    # cambian sigma y beta
                    #sigma(c)  = (x(c)(n) - x(c+1)(n)) * sigma(c)(n-1) * w(c)(c+1)//peso entre las dos c beta es igual

                    self.betaI[i][n] = self.WI[i][j] * self.betaI[i][n-1] * (self.x[i][n] - self.x[j][n])
                    self.sigmaI[i][n] = self.WI[i][j] * self.sigmaI[i][n-1] * (self.x[i][n] - self.x[j][n])
                    print('Step: ' + str(n) + ',  Cell: '+ str(i) + ', Neig: ' + str(j))


        # Remuevo final
        for i in range(self.cells):
            self.x[i] = self.x[i][0:self.N]
            self.y[i] = self.y[i][0:self.N]