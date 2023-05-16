# %% Includes
import sys
sys.path.append('Includes')
from Plotting import Plotting
from RulkovCoupled import RulkovCoupled
# %% RULKOV
rulkov = RulkovCoupled(alpha=4, sigma=0.001, cells=2, W=0, x0=1, y0=1, N=8000)
# %% Slider Parameters
def changePar(parName, parValue):
    setattr(rulkov, parName, parValue)
    rulkov.Simulate()
    return getData()

alphaPar = (rulkov.alpha, 0, 8, "alpha", changePar)
sigmaPar = (rulkov.sigma, 0, 0.001, "sigma", changePar)
WPar = (rulkov.W, 0, 1, "W", changePar)
x0Par = (rulkov.x0, -8, 8, "x0", changePar)
y0Par = (rulkov.y0, -6, 6, "y0", changePar)

pars = [alphaPar, sigmaPar, WPar, x0Par, y0Par]
# %% PLOTTING
plotting = Plotting()
# %% Burst vs N
def getData():
    datas=[]
    for c in rulkov.cells:
        datas.append([[n for n in range(rulkov.N)], rulkov.x[c]])
        datas.append([[n for n in range(rulkov.N)], rulkov.y[c]])
    return datas

datas = getData()
scale=1
plotting.SliderPlot(datas=datas, step=rulkov.N/scale, zoom=0.8, together=True, extraSliders=pars)
# %% Phase Space
# plotting.PlotPhaseSpace(rulkov.x[0], rulkov.y[0], rulkov.N, step=100)
# %% Map
# plotting.PlotPhaseSpace(rulkov.x[0][0:rulkov.N-1], rulkov.x[0][1:rulkov.N], rulkov.N - 1, step=100)