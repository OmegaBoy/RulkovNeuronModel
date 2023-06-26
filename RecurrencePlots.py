# %% Includes
import sys
sys.path.append('Includes')
from Plotting import Plotting
from MathUtil import MathUtil
from RulkovModel import RulkovModel
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
# Inicializo los parametros para todas las celulas
cells = 1
alpha_ini = 4.3
sigma_ini = 0.001
beta_ini = 0.001
w_ini = 0.01
x_init = -2
y_init = -2.9
N_pasos = 2000

alpha = [alpha_ini for _ in range(cells)]
sigma = [sigma_ini for _ in range(cells)]
beta = [beta_ini for _ in range(cells)]
W = [[w_ini if not c == v else 0 for v in range(cells)] for c in range(cells)]

# %% Corro la simulación
rulkov = RulkovModel(alpha=alpha, sigma=sigma, beta=beta, cells=cells, W=W, x0=x_init, y0=y_init, N=N_pasos)
plotting.PlotRecurrence(rulkov.x[0])