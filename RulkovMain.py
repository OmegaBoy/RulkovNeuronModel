# %%
import sys
sys.path.append('Includes')
from Plotting import Plotting
from Rulkov import Rulkov
# %% RULKOV
alpha = 4
beta = 0.001
sigma = beta
x0 = -2
y0 = -3
N = 10000
rulkov = Rulkov()
(x, y) = rulkov.RulkovModel(alpha, beta, sigma, x0, y0, N)
# %% SLIDER ARAMETERS
alphaPar = (alpha, 0, 8, "alpha", rulkov.ChangeParameter)
betaPar = (beta, 0, 0.002, "beta", rulkov.ChangeParameter)
sigmaPar = (sigma, 0, 0.002, "sigma", rulkov.ChangeParameter)
x0Par = (x0, -2, 2, "x0", rulkov.ChangeParameter)
y0Par = (y0, -3, 3, "y0", rulkov.ChangeParameter)
# NPar = (N, 1000, 100000, "N", rulkov.ChangeParameter)
pars = (alphaPar, betaPar, sigmaPar, x0Par, y0Par)
# %% PLOTTING
plotting = Plotting()
step = N/10
zoom = 0.8
plotting.SliderPlot((rulkov.x, rulkov.y), rulkov.N, step, zoom, pars)
step = N/100
plotting.PlotPhaseSpace(x, y, N, step)