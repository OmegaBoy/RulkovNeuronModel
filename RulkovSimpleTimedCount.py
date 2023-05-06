# %% Includes
import sys
sys.path.append('Includes')
import numpy as np
from Plotting import Plotting
from Rulkov import Rulkov
# %% RULKOV
rulkov = Rulkov()
# %% Initial Simulation
rulkov.RulkovSimple(alpha=4.8, beta=0.001, sigma=0.001, x0=-2, y0=-2.9, N=100)
# %% PLOTTING
plotting = Plotting()
noiseDevPar = (rulkov.noiseDev, 0, 1, "noiseDev", rulkov.ChangeParameterCountSpikes)
tresholdPar = (rulkov.threshold, 0, 3, "threshold", rulkov.ChangeParameterCountSpikes)
pars = (noiseDevPar, tresholdPar)
scale=1
plotting.SliderPlot(datas=[rulkov.SpikePlots()[0], rulkov.CountSpikes(noiseDev=0, threshold=0.5)], step=rulkov.N/scale, zoom=0.8, together=True, extraSliders=pars)