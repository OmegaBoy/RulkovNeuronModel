class Rulkov:
    def __init__(self):
        self.x = []
        self.y = []
        self.alpha = 0
        self.beta = 0
        self.sigma = 0
        self.x0 = 0
        self.y0 = 0
        self.N = 0

    def RulkovModel(self, alpha=None, beta=None, sigma=None, x0=None, y0=None, N=None):
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
        self.x = [0]*self.N
        self.x[0] = self.x0
        self.y = [0]*self.N
        self.y[0] = self.y0
        NI = range(1, self.N-1)
        for n in NI:
            self.x[n] = (self.alpha/(1+(self.x[n-1])**2))+self.y[n-1]
            self.y[n] = self.y[n-1]-self.sigma*self.x[n-1]-self.beta
        return (self.x, self.y)

    def ChangeParameter(self, par, value):
        match par:
            case "alpha":
                self.RulkovModel(alpha=value)
            case "beta":
                self.RulkovModel(beta=value)
            case "sigma":
                self.RulkovModel(sigma=value)
            case "x0":
                self.RulkovModel(x0=value)
            case "y0":
                self.RulkovModel(y0=value)
            case "N":
                self.RulkovModel(N=value)
        return ((self.x, self.y), self.N)
