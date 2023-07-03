# %% Includes
import sys
sys.path.append('Includes')
from RulkovModel import RulkovModel
from SpikeAnalyzer import SpikeAnalyzer
from Plotting import Plotting
from Utilities import Utilities
from MathUtil import MathUtil
plotting = Plotting()
# %% Rulkov Simulation
# Inicializo los parametros para todas las celulas
cells = 1
alpha_ini = 4.3
sigma_ini = 0.001
beta_ini = 0.001
w_ini = 0.01
x_init = -2
y_init = -2.9
N_pasos = 100000

alpha = [alpha_ini for _ in range(cells)]
sigma = [sigma_ini for _ in range(cells)]
beta = [beta_ini for _ in range(cells)]
W = [[w_ini if not c == v else 0 for v in range(cells)] for c in range(cells)]

# %% Corro la simulación
rulkov = RulkovModel(alpha=alpha, sigma=sigma, beta=beta, cells=cells, W=W, x0=x_init, y0=y_init, N=N_pasos)

# %% Define Slider Parameters
def changePar(parName, parValue): #Change function
    splitName = parName.split('|')
    if len(splitName) == 1:
        setattr(rulkov, parName, parValue)
    else:
        if len(splitName) == 2:
            var = getattr(rulkov, splitName[0])
            var[int(splitName[1])] = parValue
            setattr(rulkov, splitName[0], var)
        else:
            if len(splitName) == 3:
                var = getattr(rulkov, splitName[0])
                var[int(splitName[1])][int(splitName[2])] = parValue
                setattr(rulkov, splitName[0], var)
    rulkov.Simulate()
    return getData()

def getData(var = 0):
    datas=[]
    for c in range(rulkov.cells):
        match var: # Selector de variable (Por default, la rapida)
            case 0:
                datas.append([[n for n in range(rulkov.N)], rulkov.x[c]])
            case 1:
                datas.append([[n for n in range(rulkov.N)], rulkov.y[c]])
    return datas

# Parámetros
pars = []
for c in range(cells):
    pars.append(Plotting.DynamicPar(parType='TextBox', initialValue=rulkov.alpha[c], parName="alpha|" + str(c), changeFunction=changePar))
for c in range(cells):
    pars.append(Plotting.DynamicPar(parType='TextBox', initialValue=rulkov.beta[c], parName="beta|" + str(c), changeFunction=changePar))
for c in range(cells):
    pars.append(Plotting.DynamicPar(parType='TextBox', initialValue=rulkov.sigma[c], parName="sigma|" + str(c), changeFunction=changePar))
for c in range(cells):
    for v in range(cells):
        if not c == v:
            pars.append(Plotting.DynamicPar(parType='TextBox', initialValue=rulkov.W[c][v], parName="W|" + str(c) + "|" + str(v), changeFunction=changePar))

# %% Burst vs N
plot_together = True
step = 1000
plotting.SliderPlot(datas=getData(), step=step, together=plot_together, extraPars=pars)

spikedData = True
noisedData = True
diffedData = True
timedData = True

class SliderFunctions:
    def __init__(self) -> None:
        pass

    def getData(self, noiseDev = None, threshold = None, refractoryTime = None, spikedData = True, noisedData = True, diffedData = True, timedData = True):
        Utilities.ChangeParameter(noiseDev, self, "noise")
        Utilities.ChangeParameter(threshold, self, "threshold")
        Utilities.ChangeParameter(refractoryTime, self, "refractoryTime")

        self.datas = []

        spiked = [[n for n in range(rulkov.N)], rulkov.x[0]]
        if (spikedData): self.datas.append(spiked)

        noised = SpikeAnalyzer.AddNoiseToSignal(spiked[0], spiked[1], self.noise)
        if (noisedData): self.datas.append(noised)

        diffed = SpikeAnalyzer.DifferenciateSignal(noised[0], noised[1])
        if (diffedData): self.datas.append(diffed)

        timed = SpikeAnalyzer.DetectSpikes(noised[0], noised[1], self.threshold, self.refractoryTime)
        timed.append('o')
        if (timedData): self.datas.append(timed)

        return self.datas
    
    def changePar(self, parName, parValue):
        match parName:
            case "noiseDev":
                return self.getData(noiseDev=parValue, spikedData=spikedData, noisedData=noisedData, diffedData=diffedData, timedData=timedData)
            case "threshold":
                return self.getData(threshold=parValue, spikedData=spikedData, noisedData=noisedData, diffedData=diffedData, timedData=timedData)
            case "refractoryTime":
                return self.getData(refractoryTime=parValue, spikedData=spikedData, noisedData=noisedData, diffedData=diffedData, timedData=timedData)
            
    def changeParHist(self, parName, parValue):
        match parName:
            case "test":
                self.changePar("noiseDev", parValue)
                return SpikeAnalyzer.SpikesIntervals(self.datas[3][0])
    
noiseDevVal = 0
thresholdVal = 0.5
refractoryTimeVal = 0

sliderFunc = SliderFunctions()

noiseDev = Plotting.DynamicPar('TextBox', noiseDevVal, 0, 2, "noiseDev", sliderFunc.changePar)
threshold = Plotting.DynamicPar('TextBox', thresholdVal, 0, 5, "threshold", sliderFunc.changePar)
refractoryTime = Plotting.DynamicPar('TextBox', refractoryTimeVal, 0, 10, "refractoryTime", sliderFunc.changePar)

pars = [noiseDev, threshold, refractoryTime]
   
sliderFunc.getData(noiseDevVal, thresholdVal, refractoryTimeVal, spikedData=spikedData, noisedData=noisedData, diffedData=diffedData, timedData=timedData)
# %% Calculo de intervalos
scale = 300
bins = 80
plotting.SliderPlot(datas=sliderFunc.datas, step=rulkov.N/scale, extraPars=pars, zoom=0.5)
intervals = SpikeAnalyzer.SpikesIntervals(sliderFunc.datas[3][0]) # Obtengo los intervalos

# %% Visor de intervalos
intervalsSub = 500 # Sublength of intervals
plotting.PlotMultiple([[[i for i in range(intervalsSub)],intervals[0:intervalsSub], 'o']]) # Plot de los intervalos
# plotting.PlotMultiple([[sliderFunc.datas[1][0][0:intervalsSub], sliderFunc.datas[1][1][0:intervalsSub]], [[i for i in range(intervalsSub)] ,intervals[0:intervalsSub]]], together=False)

# %% Histogram
doubleLog = True
plotting.Histogram(intervals, bins, ylog=doubleLog, xlog=doubleLog)

# %% Calculo de Historgrama y sus pendientes
slopesData = SpikeAnalyzer.CalculateHistogramSlopes(intervals, bins, threshold=1, minSequenceSize=2) #Calculamos las pendientes de los histogramas
plotting.PlotHistogramSlopes(signal=intervals, bins=bins, slopesData=slopesData, ylog=doubleLog, xlog=doubleLog) # Graficamos el histograma con sus pendientes

# %% Power series
plotting.PowerSeries(intervals, doubleLog, doubleLog)