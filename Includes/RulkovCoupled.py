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
        self.sigmaI = [self.sigma for _ in range(self.cells)] # Matriz inicial de Sigma

        # TODO: Hacer que el factor que se achica sigma sea una variable y que vaya de 10 a 1000 veces mas chico
        # TODO: poder cambiar los parametros de una neurona a la vez

        # Seteo los pesos en todo menos la diagonal (Con si misma) en 0
        for i in range(0, self.cells):
            self.WI[i][self.cells - 1 - i] = self.W

        for n in self.NI:
            # Calculamos el estado actual de cada neurona
            for i in self.I:
                self.x[i][n] = (self.alpha/(1+(self.x[i][n-1])**2))+self.y[i][n-1]
                self.y[i][n] = self.y[i][n-1]-self.sigmaI[i]*self.x[i][n-1]-self.beta

            # Calculamos los nuevos parametros a partir de la diferencia entre las neuronas
            for i in self.I:
                for j in self.J:
                    if i != j:
                        # Calculo la diferencia de los estados de las neuronas
                        diff = (self.x[j][n-1] - self.x[i][n-1])
                        # Calculo el factor de cambio de coupling entre las neuronas como el peso entre estas por la diferencia normalizada
                        fact = self.WI[i][j] * diff

                        self.sigmaI[i] = self.sigma + fact * self.sigmaI[i]

        # Remuevo final
        for i in range(self.cells):
            self.x[i] = self.x[i][0:self.N]
            self.y[i] = self.y[i][0:self.N]