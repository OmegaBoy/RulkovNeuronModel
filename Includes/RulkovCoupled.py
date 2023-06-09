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
        self.sigmaI = [[0 for _ in range(self.NCO)] for _ in range(self.cells)] # Matriz inicial de Sigma

        for bi in self.betaI: bi[0] = self.beta # Seteo alpha en el primero de los Beta
        for si in self.sigmaI: si[0] = self.sigma # Seteo sigma inicial en el primero de los Sigma

        # SETEO TEMPORALMENTE PARAMETROS DIFERENTES
        self.sigmaI[1][0] = self.sigmaI[1][0] * 1.2# aleatorio 0 y 1
        self.betaI[1][0] = self.betaI[1][0] * 1.2

        # Seteo los pesos en todo menos la diagonal (Con si misma) en 0
        for i in range(0, self.cells):
            self.WI[i][self.cells - 1 - i] = self.W

        for n in self.NI:
            # Calculamos el estado actual de cada neurona
            for i in self.I:
                self.x[i][n] = (self.alpha/(1+(self.x[i][n-1])**2))+self.y[i][n-1]
                self.y[i][n] = self.y[i][n-1]-self.sigmaI[i][n-1]*self.x[i][n-1]-self.betaI[i][n-1]

            # Calculamos los nuevos parametros a partir de la diferencia entre las neuronas
            for i in self.I:
                for j in self.J:
                    if i != j:
                        # Calculo la diferencia normalizada de los estados de las neuronas
                        normDiff = (self.x[j][n-1] - self.x[i][n-1])
                        # Calculo el factor de cambio de coupling entre las neuronas como el peso entre estas por la diferencia normalizada
                        fact = self.WI[i][j] * normDiff

                        self.betaI[i][n] = self.betaI[1][0] + fact * self.betaI[i][n-1]
                        self.sigmaI[i][n] = self.sigmaI[1][0] + fact * self.sigmaI[i][n-1]

                        # print('NormDiff: ' + str(normDiff) + ', Fact: ' + str(fact) + ', Beta: ' + str(self.betaI[i][n]) + ', Sigma: ' + str(self.sigmaI[i][n]))

        # Remuevo final
        for i in range(self.cells):
            self.x[i] = self.x[i][0:self.N]
            self.y[i] = self.y[i][0:self.N]