# %% Includes y Initializations
import sys
sys.path.append('Includes')
from Plotting import Plotting
from RulkovCoupled import RulkovCoupled
plotting = Plotting()

# %% Rulkov Simulation
# Inicializo los parametros para todas las celulas
cells = 2
alpha = []
sigma = []
beta = []
W = [[0 for _ in range(cells)] for _ in range(cells)]
for c in range(cells):
    alpha.append(4.3)
    sigma.append(0.001)
    beta.append(0.001)
    for v in range(cells):
        if not c == v:
            W[c][v] = 0.01

rulkov = RulkovCoupled(alpha=alpha, sigma=sigma, beta=beta, cells=cells, W=W, x0=-2, y0=-2.9, N=2000)

# %% Define Slider Parameters
def changePar(parName, parValue): #Change function
    splitName = parName.split('|')
    if len(splitName) == 1:
        setattr(rulkov, parName, parValue)
    else:
        if len(splitName) == 2:
            var = getattr(rulkov, splitName[0])
            var[int(splitName[1])] = parValue
            setattr(rulkov, splitName[0], var)
        else:
            if len(splitName) == 3:
                var = getattr(rulkov, splitName[0])
                var[int(splitName[1])][int(splitName[2])] = parValue
                setattr(rulkov, splitName[0], var)
    rulkov.Simulate()
    return getData()

def getData(var = 0):
    datas=[]
    for c in range(rulkov.cells):
        match var: # Selector de variable (Por default, la rapida)
            case 0:
                datas.append([[n for n in range(rulkov.N)], rulkov.x[c]])
            case 1:
                datas.append([[n for n in range(rulkov.N)], rulkov.y[c]])
    return datas

# Parámetros
pars = []
for c in range(cells):
    pars.append(Plotting.DynamicPar(parType='TextBox', initialValue=rulkov.alpha[c], parName="alpha|" + str(c), changeFunction=changePar))
for c in range(cells):
    pars.append(Plotting.DynamicPar(parType='TextBox', initialValue=rulkov.beta[c], parName="beta|" + str(c), changeFunction=changePar))
for c in range(cells):
    pars.append(Plotting.DynamicPar(parType='TextBox', initialValue=rulkov.sigma[c], parName="sigma|" + str(c), changeFunction=changePar))
for c in range(cells):
    for v in range(cells):
        if not c == v:
            pars.append(Plotting.DynamicPar(parType='TextBox', initialValue=rulkov.W[c][v], parName="W|" + str(c) + "|" + str(v), changeFunction=changePar))

# %% Burst vs N
plotting.SliderPlot(datas=getData(), step=1000, zoom=0.8, together=True, extraPars=pars)

# %% Phase Space
# plotting.PlotPhaseSpace(x=datas[0][1], y=datas[1][1], N=rulkov.N, step=rulkov.N/scale)

# %% Map
# plotting.PlotPhaseSpace(rulkov.x[0:rulkov.N-1], rulkov.x[1:rulkov.N], rulkov.N - 1, step=4000)