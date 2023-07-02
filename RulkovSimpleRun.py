# %% Includes y Initializations
import sys
sys.path.append('Includes')
from Plotting import Plotting
from RulkovModel import RulkovModel
plotting = Plotting()

# %% Rulkov Simulation
# Inicializo los parametros para todas las celulas
cells = 1
alpha_ini = 4
sigma_ini = 0.001
beta_ini = 0.001
w_ini = 0.01
x_init = -2
y_init = -2.9
N_pasos = 100000

alpha = [alpha_ini for _ in range(cells)]
sigma = [sigma_ini for _ in range(cells)]
beta = [beta_ini for _ in range(cells)]
W = [[w_ini if not c == v else 0 for v in range(cells)] for c in range(cells)]

# %% Corro la simulación
rulkov = RulkovModel(alpha=alpha, sigma=sigma, beta=beta, cells=cells, W=W, x0=x_init, y0=y_init, N=N_pasos)

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
    return getData(2)

def getData(var = 0):
    datas=[]
    for c in range(rulkov.cells):
        match var: # Selector de variable (Por default, la rapida)
            case 0:
                datas.append([[n for n in range(rulkov.N)], rulkov.x[c]])
            case 1:
                datas.append([[n for n in range(rulkov.N)], rulkov.y[c]])
            case 2:
                datas.append([[n for n in range(rulkov.N)], rulkov.x[c]])
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
plot_together = False
step = 15000
datas = getData(2)
plotting.SliderPlot(datas=datas, step=step, together=plot_together, extraPars=pars)

# %% Phase Space
plotting.PlotPhaseSpace(x=datas[0][1], y=datas[1][1], N=rulkov.N, step=rulkov.N/32)
# %% Map
# plotting.PlotPhaseSpace(rulkov.x[0][0:rulkov.N-1], rulkov.x[0][1:rulkov.N], rulkov.N - 1, step=4000)