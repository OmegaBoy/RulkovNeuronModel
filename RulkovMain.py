# %%
import sys
sys.path.append('Includes')
from Plotting import Plotting
from Rulkov import Rulkov
# %%
alpha = 4
beta = 0.001
sigma = beta
x0 = -2
y0 = -3
N = 1000000
div = 3
cutoff = 0.9
step = N/100
yZoom = 0.8
# %%
(x, y) = Rulkov.RulkovModel(alpha, beta, sigma, x0, y0, N)
plotting = Plotting()
plotting.SliderPlot(x, N, step, yZoom)
# plotting.PlotPhaseSpace(x, y, N, cutoff)