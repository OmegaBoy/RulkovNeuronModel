class Rulkov:
    def RulkovModel(alpha, beta, sigma, x0, y0, N):
        x = [0]*N
        x[0] = x0
        y = [0]*N
        y[0] = y0
        NI = range(1, N-1)
        for n in NI:
            x[n] = (alpha/(1+(x[n-1])**2))+y[n-1]
            y[n] = y[n-1]-sigma*x[n-1]-beta
        return (x, y)
