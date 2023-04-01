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
mode = "slow"
rulkov = Rulkov()
(x, y) = rulkov.RulkovModel(alpha, beta, sigma, x0, y0, N)
# %% SLIDER ARAMETERS
alphaPar = (alpha, 0, 8, "alpha", rulkov.ChangeParameter, mode)
betaPar = (beta, 0, 0.002, "beta", rulkov.ChangeParameter, mode)
sigmaPar = (sigma, 0, 0.002, "sigma", rulkov.ChangeParameter, mode)
# x0Par = (x0, -2, 2, "x0", rulkov.ChangeParameter, mode)
# y0Par = (y0, -3, 3, "y0", rulkov.ChangeParameter, mode)
# NPar = (N, 1000, 100000, "N", rulkov.ChangeParameter, mode)
pars = (alphaPar, betaPar, sigmaPar)
# %% PLOTTING
plotting = Plotting()
step = N/2
yZoom = 0.8
if mode == "fast": plotting.SliderPlot(rulkov.x, rulkov.N, step, yZoom, pars)
if mode == "slow": plotting.SliderPlot(rulkov.y, rulkov.N, step, yZoom, pars)
cutoff = 0.9
# plotting.PlotPhaseSpace(x, y, N, cutoff)
# %%
# a[3](a[2], 2)