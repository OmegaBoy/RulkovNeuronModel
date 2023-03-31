#%%
import sys
import matplotlib.pyplot as plt
sys.path.append('Includes')
from Functions import Functions
#%% Initialization
alpha=4
sigma=0.001
beta=sigma
x0=1
y0=-3
N=10000
x=[0]*N
x[0]=x0
y=[0]*N
y[0]=y0
#%%
NI=range(1,N-1)
for n in NI:
    x[n]=(alpha/(1+(x[n-1])**2))+y[n-1]
    y[n]=y[n-1]-sigma*x[n-1]-beta
plt.plot(x[0:round(N*0.9)])
plt.show()
plt.plot(y[0:round(N*0.9)])
plt.show()
plt.plot(x[0:round(N*0.9)],y[0:round(N*0.9)])
plt.show()