# %% Includes
import sys
sys.path.append('Includes')
from Plotting import Plotting
from Rulkov import Rulkov
# %% RULKOV
rulkov = Rulkov()
# %% Initial Simulation
rulkov.RulkovCoupled(alpha=4, sigma=0.001, cells=1, W=0, x0=1, y0=1, N=8000)
# %% Slider Parameters
alphaPar = (rulkov.alpha, 0, 8, "alpha", rulkov.ChangeParameterRulkovCoupled)
sigmaPar = (rulkov.sigma, 0, 0.001, "sigma", rulkov.ChangeParameterRulkovCoupled)
WPar = (rulkov.W, 0, 1, "W", rulkov.ChangeParameterRulkovCoupled)
x0Par = (rulkov.x0, -8, 8, "x0", rulkov.ChangeParameterRulkovCoupled)
y0Par = (rulkov.y0, -6, 6, "y0", rulkov.ChangeParameterRulkovCoupled)
pars = (alphaPar, sigmaPar, WPar, x0Par, y0Par)
# %% PLOTTING
plotting = Plotting()
# %% Burst vs N
plotting.SliderPlot(rulkov.SpikePlots(), step=2000, zoom=0.8, extraSliders=pars)
# %% Phase Space
# plotting.PlotPhaseSpace(rulkov.x[0], rulkov.y[0], rulkov.N, step=100)
# %% Map
# plotting.PlotPhaseSpace(rulkov.x[0][0:rulkov.N-1], rulkov.x[0][1:rulkov.N], rulkov.N - 1, step=100)