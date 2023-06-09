# %% Includes
import sys
sys.path.append('Includes')
from Plotting import Plotting
from RulkovCoupled import RulkovCoupled
# %% RULKOV
rulkov = RulkovCoupled(alpha=4.3, sigma=0.001, beta=0.001, cells=2, W=0, x0=-2, y0=-2.9, N=800)
# %% Slider Parameters
def changePar(parName, parValue):
    setattr(rulkov, parName, parValue)
    rulkov.Simulate()
    return getData()

alphaPar = Plotting.SliderPar(rulkov.alpha, 0, 8 , "alpha", changePar)
betaPar = Plotting.SliderPar(rulkov.beta, 0, 0.002, "beta", changePar)
sigmaPar = Plotting.SliderPar(rulkov.sigma, 0, 1, "sigma", changePar)
WPar = Plotting.SliderPar(rulkov.W, 0, 1, "W", changePar)
x0Par = Plotting.SliderPar(rulkov.x0, -8, 8, "x0", changePar)
y0Par = Plotting.SliderPar(rulkov.y0, -6, 6, "y0", changePar)

pars = [alphaPar, betaPar, sigmaPar, WPar, x0Par, y0Par]
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
plotting.SliderPlot(datas=datas, step=rulkov.N/scale, zoom=0.8, together=True, extraSliders=pars)
# %% Phase Space
# plotting.PlotPhaseSpace(x=datas[0][1], y=datas[1][1], N=rulkov.N, step=rulkov.N/scale)
# %% Map
# plotting.PlotPhaseSpace(rulkov.x[0:rulkov.N-1], rulkov.x[1:rulkov.N], rulkov.N - 1, step=4000)