class SpikeAnalyzer:
    def SpikesIntervals(iTimedData):
        intervals = [iTimedData[n + 1] - iTimedData[n]
                     for n in range(len(iTimedData) - 1)]
        return intervals

    def DetectSpikes(index, signal, threshold, refractoryTime=0):
        iTimedSignal = []
        [iDiffSigal, diffSignal] = SpikeAnalyzer.DifferenciateSignal(
            index, signal)
        indexDet = None
        for n in range(len(iDiffSigal) - 1):
            if diffSignal[n] > 0 and diffSignal[n+1] < 0:
                if signal[n+1] > threshold and (indexDet == None or n+1 > (indexDet+refractoryTime)):
                    indexDet = n+1
                    iTimedSignal.append(iDiffSigal[n] + iDiffSigal[0])
        maxSignalVal = max(signal)
        timedData = [iTimedSignal, [
            maxSignalVal for _ in range(len(iTimedSignal))]]
        return timedData

    def DifferenciateSignal(index, signal):
        iDiffSignal = [
            index[n] + (index[n + 1] - index[n])/2 for n in range(len(index) - 1)]
        diffSignal = [signal[n + 1] - signal[n]
                      for n in range(len(iDiffSignal))]
        return [iDiffSignal, diffSignal]
    
    def CalculateSlopeSignal(index, signal):
        iSlopeSignal = [
            index[n] + (index[n + 1] - index[n])/2 for n in range(len(index) - 1)]
        slopeSignal = [(signal[n + 1] - signal[n])/(index[n + 1] - index[n])
                      for n in range(len(iSlopeSignal))]
        return [iSlopeSignal, slopeSignal]

    def AddNoiseToSignal(index, signal, noiseDev):
        import numpy as np
        N = len(signal)
        noise = np.random.normal(0, noiseDev, N)
        iNoisedSignal = index
        noisedSignal = [signal[n] + noise[n] for n in range(N)]
        return [iNoisedSignal, noisedSignal]
    
    def CalculateHistogramSlopes(signal, bins = 10, threshold = 1, minSequenceSize = 2):
        import numpy as np
        hist, bins_edges = np.histogram(signal, bins)

        y = []
        x = []
        for n in range(bins):
            if hist[n] != 0:
                x.append((bins_edges[n + 1] + bins_edges[n])/2)
                y.append(hist[n])

        lx = np.log(x)
        ly = np.log(y)

        import matplotlib.pyplot as plt
        ds = SpikeAnalyzer.CalculateSlopeSignal(lx, ly)

        slopeIndexes=[]
        currentIndexes = []
        for n in range(len(ds[0])):
            if ds[1][n] < threshold:
                if len(currentIndexes) == 0:
                    currentIndexes.append(n)
            else:
                currentIndexes.append(n)
                if len(currentIndexes)==2:
                    if currentIndexes[1] - currentIndexes[0] > minSequenceSize:
                        slopeIndexes.append(currentIndexes)
                    currentIndexes=[]
            if len(slopeIndexes)==2:
                break
        
        from scipy.stats import linregress
        slopes = []
        for si in slopeIndexes:
            xv = [np.exp(x) for x in lx]
            yv = [np.exp(y) for y in ly]
            lxv = lx[si[0]:si[1]]
            lyv = ly[si[0]:si[1]]
            r = linregress(lxv, lyv)
            slopes.append({
                "Slope": r,
                "x": xv,
                "y": yv,
                "lx": lxv,
                "ly": lyv
            })

        return {
            "Slopes": slopes,
            "Data": {
                "x": lx,
                "y": ly
            }
        }