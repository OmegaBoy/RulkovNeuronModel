# %% Includes
import sys
sys.path.append('Includes')
from Plotting import Plotting
from MathUtil import MathUtil
from RulkovSimple import RulkovSimple
# Inicializo
plotting = Plotting()
mathUtil = MathUtil()
# %% SIN WAVE
signal = mathUtil.np.sin(mathUtil.np.linspace(0, 100, 10000)) # Un seno de 1000 puntos con t [0, 100]
plotting.PlotRecurrence(signal)
# %% RAND DATA
random_array = mathUtil.np.random.rand(1000)
plotting.PlotRecurrence(random_array)
#  %% RULKOV SIMPLE SIGNAL
rulkov = RulkovSimple(alpha=4, beta=0.001, sigma=0.001, x0=-2, y0=-2.9, N=10000)
plotting.PlotRecurrence(rulkov.x)