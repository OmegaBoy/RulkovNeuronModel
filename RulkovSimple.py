# %% Includes
import sys
sys.path.append('Includes')
from Plotting import Plotting
from Rulkov import Rulkov
# %% RULKOV
rulkov = Rulkov()
# %% Initial Simulation
rulkov.RulkovSimple(alpha=4, beta=0.001, sigma=0.001, x0=-2, y0=-2.9, N=600)
# %% Slider Parameters
alphaPar = (rulkov.alpha, 0, 8, "alpha", rulkov.ChangeParameterRulkovSimple)
betaPar = (rulkov.beta, 0, 0.002, "beta", rulkov.ChangeParameterRulkovSimple)
sigmaPar = (rulkov.sigma, 0, 0.001, "sigma", rulkov.ChangeParameterRulkovSimple)
x0Par = (rulkov.x0, -8, 8, "x0", rulkov.ChangeParameterRulkovSimple)
y0Par = (rulkov.y0, -6, 6, "y0", rulkov.ChangeParameterRulkovSimple)
pars = (alphaPar, betaPar, sigmaPar, x0Par, y0Par)
# %% PLOTTING
plotting = Plotting()
# %% Burst vs N
datas=rulkov.SpikePlots()
scale=1
plotting.SliderPlot(datas=datas, step=rulkov.N/scale, zoom=0.8, together=True, extraSliders=pars)
# %% Phase Space
# plotting.PlotPhaseSpace(x=datas[0][1], y=datas[1][1], N=rulkov.N, step=rulkov.N/scale)
# %% Map
# plotting.PlotPhaseSpace(rulkov.x[0:rulkov.N-1], rulkov.x[1:rulkov.N], rulkov.N - 1, step=4000)