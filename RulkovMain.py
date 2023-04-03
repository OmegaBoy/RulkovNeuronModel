# %% Includes
import sys
sys.path.append('Includes')
from Plotting import Plotting
from Rulkov import Rulkov
# %% RULKOV
rulkov = Rulkov()
# %% Initial Simulation
rulkov.RulkovModel(alpha=4, beta=0.001, sigma=0.001, x0=-2, y0=-3, N=50000)
# %% Slider Parameters
alphaPar = (rulkov.alpha, 0, 8, "alpha", rulkov.ChangeParameter)
betaPar = (rulkov.beta, 0, 0.002, "beta", rulkov.ChangeParameter)
sigmaPar = (rulkov.sigma, 0, 0.001, "sigma", rulkov.ChangeParameter)
x0Par = (rulkov.x0, -8, 8, "x0", rulkov.ChangeParameter)
y0Par = (rulkov.y0, -6, 6, "y0", rulkov.ChangeParameter)
pars = (alphaPar, betaPar, sigmaPar, x0Par, y0Par)
# %% PLOTTING
plotting = Plotting()
# %% Burst vs N
plotting.SliderPlot(y=(rulkov.x, rulkov.y), N=rulkov.N, step=10000, zoom=0.8, extraSliders=pars)
# %% Phase Space
plotting.PlotPhaseSpace(rulkov.x, rulkov.y, rulkov.N, step=50)
# %% Map
plotting.PlotPhaseSpace(rulkov.x[0:rulkov.N-1], rulkov.x[1:rulkov.N], rulkov.N - 1, step=50)