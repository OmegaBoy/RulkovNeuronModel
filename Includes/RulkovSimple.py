class RulkovSimple:
    def __init__(self, alpha=None, beta=None, sigma=None, x0=None, y0=None, N=None):
        from Utilities import Utilities

        Utilities.ChangeParameter(alpha, self, "alpha")
        Utilities.ChangeParameter(beta, self, "beta")
        Utilities.ChangeParameter(sigma, self, "sigma")
        Utilities.ChangeParameter(x0, self, "x0")
        Utilities.ChangeParameter(y0, self, "y0")
        Utilities.ChangeParameter(N, self, "N")

        self.Simulate()

    def Simulate(self):
        self.x = []
        self.y = []

        self.NCO = int(self.N*1.1)
        self.x = [0]*self.NCO
        self.x[0] = self.x0
        self.y = [0]*self.NCO
        self.y[0] = self.y0
        self.NI = range(1, self.NCO-1)
        self.i = [n for n in range(self.N)]

        for n in self.NI:
            self.x[n] = (self.alpha/(1+(self.x[n-1])**2))+self.y[n-1]
            self.y[n] = self.y[n-1]-self.sigma*self.x[n-1]-self.beta
        self.x = self.x[0:self.N]
        self.y = self.y[0:self.N]