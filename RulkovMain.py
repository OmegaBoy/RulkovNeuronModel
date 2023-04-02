# %% Includes
import sys
sys.path.append('Includes')
from Plotting import Plotting
from Rulkov import Rulkov
# %% RULKOV
rulkov = Rulkov()
# %% Initial Simulation
rulkov.RulkovModel(alpha=4, beta=0.001, sigma=0.001, x0=-2, y0=-3, N=100000)
# %% Slider Parameters
alphaPar = (rulkov.alpha, 0, 8, "alpha", rulkov.ChangeParameter)
betaPar = (rulkov.beta, 0, 0.002, "beta", rulkov.ChangeParameter)
sigmaPar = (rulkov.sigma, 0, 0.002, "sigma", rulkov.ChangeParameter)
x0Par = (rulkov.x0, -2, 2, "x0", rulkov.ChangeParameter)
y0Par = (rulkov.y0, -3, 3, "y0", rulkov.ChangeParameter)
pars = (alphaPar, betaPar, sigmaPar, x0Par, y0Par)
# %% PLOTTING
plotting = Plotting()
# %% Burst vs N
plotting.SliderPlot(y=(rulkov.x, rulkov.y), N=rulkov.N, step=rulkov.N/10, zoom=0.8, extraSliders=pars)
# %% Phase Space
rulkov.ChangeParameter('N', 10000)
plotting.PlotPhaseSpace(rulkov.x, rulkov.y, rulkov.N, step=rulkov.N/100)
