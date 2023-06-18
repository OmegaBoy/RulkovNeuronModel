# %% Includes
import sys
sys.path.append('Includes')
from Plotting import Plotting
from RulkovCoupled import RulkovCoupled
# %% RULKOV
rulkov = RulkovCoupled(alpha=4.3, sigma=[0.001, 0.00112], beta=0.001, cells=2, W=0.01, x0=-2, y0=-2.9, N=800)
# %% Slider Parameters
def changePar(parName, parValue):
    splitName = parName.split('|')
    if len(splitName) == 1:
        setattr(rulkov, parName, parValue)
    else:
        var = getattr(rulkov, splitName[0])
        var[int(splitName[1])] = parValue
        setattr(rulkov, splitName[0], var)
    rulkov.Simulate()
    return getData()

pars = []
pars.append(Plotting.DynamicPar(parType='TextBox', initialValue=rulkov.alpha, parName="alpha", changeFunction=changePar))
pars.append(Plotting.DynamicPar(parType='TextBox', initialValue=rulkov.beta, parName="beta", changeFunction=changePar))
pars.append(Plotting.DynamicPar(parType='TextBox', initialValue=rulkov.sigma[0], parName="sigma|0", changeFunction=changePar))
pars.append(Plotting.DynamicPar(parType='TextBox', initialValue=rulkov.sigma[1], parName="sigma|1", changeFunction=changePar))
pars.append(Plotting.DynamicPar(parType='TextBox', initialValue=rulkov.W, parName="W", changeFunction=changePar))

# %% PLOTTING
plotting = Plotting()
# %% Burst vs N
def getData():
    datas=[]
    for c in range(rulkov.cells):
        datas.append([[n for n in range(rulkov.N)], rulkov.x[c]])
        # datas.append([[n for n in range(rulkov.N)], rulkov.y[c]])
    return datas

datas = getData()
scale=1
plotting.SliderPlot(datas=datas, step=rulkov.N/scale, zoom=0.8, together=True, extraPars=pars)
# %% Phase Space
# plotting.PlotPhaseSpace(x=datas[0][1], y=datas[1][1], N=rulkov.N, step=rulkov.N/scale)
# %% Map
# plotting.PlotPhaseSpace(rulkov.x[0:rulkov.N-1], rulkov.x[1:rulkov.N], rulkov.N - 1, step=4000)