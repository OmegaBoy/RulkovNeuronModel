# %% Includes
import sys
sys.path.append('Includes')
from RulkovSimple import RulkovSimple
from SpikeAnalyzer import SpikeAnalyzer
from Plotting import Plotting
from Utilities import Utilities
# %% RULKOV
rulkov = RulkovSimple(alpha=4.8, beta=0.001, sigma=0.001, x0=-2, y0=-2.9, N=100000)
plotting = Plotting()
class SliderFunctions:
    def __init__(self) -> None:
        pass

    def getData(self, noiseDev = None, threshold = None, refractoryTime = None):
        Utilities.ChangeParameter(noiseDev, self, "noise")
        Utilities.ChangeParameter(threshold, self, "threshold")
        Utilities.ChangeParameter(refractoryTime, self, "refractoryTime")

        self.datas = []

        spiked = [rulkov.i, rulkov.x]
        self.datas.append(spiked)

        noised = SpikeAnalyzer.AddNoiseToSignal(spiked[0], spiked[1], self.noise)
        self.datas.append(noised)

        diffed = SpikeAnalyzer.DifferenciateSignal(noised[0], noised[1])
        self.datas.append(diffed)

        timed = SpikeAnalyzer.DetectSpikes(noised[0], noised[1], self.threshold, self.refractoryTime)
        timed.append('o')
        self.datas.append(timed)

        return self.datas
    
    def changePar(self, parName, parValue):
        match parName:
            case "noiseDev":
                return self.getData(noiseDev=parValue)
            case "threshold":
                return self.getData(threshold=parValue)
            case "refractoryTime":
                return self.getData(refractoryTime=parValue)
            
    def changeParHist(self, parName, parValue):
        match parName:
            case "test":
                self.changePar("noiseDev", parValue)
                return SpikeAnalyzer.SpikesIntervals(self.datas[3][0])
    
noiseDevVal = 0
thresholdVal = 0.5
refractoryTimeVal = 0

sliderFunc = SliderFunctions()

noiseDev = Plotting.SliderPar(noiseDevVal, 0, 2, "noiseDev", sliderFunc.changePar)
threshold = Plotting.SliderPar(thresholdVal, 0, 5, "threshold", sliderFunc.changePar)
refractoryTime = Plotting.SliderPar(refractoryTimeVal, 0, 10, "refractoryTime", sliderFunc.changePar)

pars = [noiseDev, threshold, refractoryTime]
   
sliderFunc.getData(noiseDevVal, thresholdVal, refractoryTimeVal)
# %% Plotting
scale = 400
bins = 80
plotting.SliderPlot(datas=sliderFunc.datas, step=rulkov.N/scale, zoom=0.8, extraSliders=pars)
# %% Histogram
intervals = SpikeAnalyzer.SpikesIntervals(sliderFunc.datas[3][0])

slopeIndexes = [[0, 8],[15, 32]]
# slopeIndexes = []
plotting.PlotHistogramSlopes(intervals, bins, slopeIndexes)
# %% Power series
# plotting.PowerSeries(sliderFunc.datas[0][1])