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

# %% Slider Parameters
def changePar(parName, parValue):
    setattr(rulkov, parName, parValue)
    rulkov.Simulate()
    return getData()

alphaPar = Plotting.SliderPar(rulkov.alpha, 0, 8 , "alpha", changePar)
betaPar = Plotting.SliderPar(rulkov.beta, 0, 0.002, "beta", changePar)
sigmaPar = Plotting.SliderPar(rulkov.sigma, 0, 0.001, "sigma", changePar)
x0Par = Plotting.SliderPar(rulkov.x0, -8, 8, "x0", changePar)
y0Par = Plotting.SliderPar(rulkov.y0, -6, 6, "y0", changePar)

pars = [alphaPar, betaPar, sigmaPar, x0Par, y0Par]
# %% PLOTTING
plotting = Plotting()
# %% Burst vs N
def getData():
    datas=[]
    datas.append([[n for n in range(rulkov.N)], rulkov.x])
    datas.append([[n for n in range(rulkov.N)], rulkov.y])
    return datas

datas = getData()
scale=100
# plotting.SliderPlot(datas=datas, step=rulkov.N/scale, zoom=0.8, together=True, extraSliders=pars)

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
# plotting.SliderPlot(datas=sliderFunc.datas, step=rulkov.N/scale, zoom=0.8, extraSliders=pars)
# %% Histogram
intervals = SpikeAnalyzer.SpikesIntervals(sliderFunc.datas[3][0])
plotting.PlotMultiple([[[i for i in range(len(intervals))],intervals, 'o']])
# plotting.PlotMultiple([[sliderFunc.datas[1][0], sliderFunc.datas[1][1]], [[i for i in range(len(intervals))] ,intervals]], together=False)

# plotting.Histogram(intervals, bins,ylog=False, xlog=False)
# %%
# slopeIndexes = []
# slopeIndexes = [[0, 8],[15, 32]]
# slopesData = SpikeAnalyzer.CalculateHistogramSlopes(intervals, bins, slopeIndexes=slopeIndexes, threshold=1, minSequenceSize=2)
# datas=[[slopesData["Data"]["x"], slopesData["Data"]["y"]]]
# for slope in slopesData["Slopes"]:
#     datas.append([slope["x"], [vx*slope["Slope"].slope + slope["Slope"].intercept for vx in slope["x"]]])
# plotting.PlotMultiple(datas)
# plotting.PlotHistogramSlopes(intervals, bins, slopeIndexes)

# %% Power series
# plotting.PowerSeries(intervals, False, False)