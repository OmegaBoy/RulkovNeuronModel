# %% Includes
import sys
sys.path.append('Includes')
from Plotting import Plotting
from Rulkov import Rulkov
# %% RULKOV
rulkov = Rulkov()
# %% Initial Simulation
rulkov.RulkovSimple(alpha=4.8, beta=0.001, sigma=0.001, x0=-2, y0=-2.9, N=50000)
# %% PLOTTING
plotting = Plotting()
# %% Burst vs N
data = rulkov.SpikePlots()[0]
threshold=0.2
window=10
timedData=[]
for n in range(len(data[0])):
    if data[1][n] > threshold and tempd < threshold:
       tempd=data[1][n]
       timedData.append((data[0][n], data[1][n]))
print(timedData)