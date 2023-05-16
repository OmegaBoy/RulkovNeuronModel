# %% Includes
import sys
sys.path.append('Includes')
from RulkovSimple import RulkovSimple
from SpikeAnalyzer import SpikeAnalyzer
from Plotting import Plotting
from Utilities import Utilities
# %% RULKOV
rulkov = RulkovSimple(alpha=4.8, beta=0.001, sigma=0.001, x0=-2, y0=-2.9, N=10000)
plotting = Plotting()
class SliderFunctions:
    def __init__(self) -> None:
        pass

    def getData(self, noiseDev = None, threshold = None, refractoryTime = None):
        Utilities.ChangeParameter(noiseDev, self, "noise")
        Utilities.ChangeParameter(threshold, self, "threshold")
        Utilities.ChangeParameter(refractoryTime, self, "refractoryTime")

        datas = []

        spiked = [rulkov.i, rulkov.x]
        # datas.append(spiked)

        noised = SpikeAnalyzer.AddNoiseToSignal(spiked[0], spiked[1], self.noise)
        datas.append(noised)

        diffed = SpikeAnalyzer.DifferenciateSignal(noised[0], noised[1])
        # datas.append(diffed)

        timed = SpikeAnalyzer.DetectSpikes(noised[0], noised[1], self.threshold, self.refractoryTime)
        timed.append('o')
        datas.append(timed)

        return datas
    
    def changePar(self, parName, parValue):
        match parName:
            case "noiseDev":
                return self.getData(noiseDev=parValue)
            case "threshold":
                return self.getData(threshold=parValue)
            case "refractoryTime":
                return self.getData(refractoryTime=parValue)

noiseDevVal = 0
thresholdVal = 0.5
refractoryTimeVal = 0

sliderFunc = SliderFunctions()

noiseDev = Plotting.SliderPar(noiseDevVal, 0, 2, "noiseDev", sliderFunc.changePar)
threshold = Plotting.SliderPar(thresholdVal, 0, 5, "threshold", sliderFunc.changePar)
refractoryTime = Plotting.SliderPar(refractoryTimeVal, 0, 10, "refractoryTime", sliderFunc.changePar)

pars = [noiseDev, threshold, refractoryTime]
   
datas = sliderFunc.getData(noiseDevVal, thresholdVal, refractoryTimeVal)
# %% Plotting
scale = 100
plotting.SliderPlot(datas=datas, step=rulkov.N/scale, zoom=0.8, together=True, extraSliders=pars)
# %% Statistics
intervals = SpikeAnalyzer.SpikesIntervals()