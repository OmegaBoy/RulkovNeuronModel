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

    def AddNoiseToSignal(index, signal, noiseDev):
        import numpy as np
        N = len(signal)
        noise = np.random.normal(0, noiseDev, N)
        iNoisedSignal = index
        noisedSignal = [signal[n] + noise[n] for n in range(N)]
        return [iNoisedSignal, noisedSignal]
    
    def CalculateHistogramSlopes(signal, bins = 10, slopeIndexes=[], length = 4):
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

        slopes = []
        from scipy.stats import linregress
        # for si in slopeIndexes:
        #     lxv = lx[si[0]:si[1]]
        #     lyv = ly[si[0]:si[1]]
        #     r = linregress(lxv, lyv)
        #     slopes.append(r)

        for d in range(len(lx) - length):
            lxv = lx[d:d+length]
            lyv = ly[d:d+length]
            r = linregress(lxv, lyv)
            slopes.append({
                "Slope": r,
                "x": lxv,
                "y": lyv
            })

        import matplotlib.pyplot as plt
        
        plt.plot(lx, ly)
        plt.plot()

        ds = SpikeAnalyzer.DifferenciateSignal(lx, ly)

        plt.plot(ds[0], ds[1])

        plt.show()

        return {
            "Slopes": slopes,
            "Data": {
                "x": lx,
                "y": ly
            }
        }