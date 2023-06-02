class Plotting:
    def __init__(self):
        import numpy as np
        import math
        import matplotlib.pyplot as plt
        from matplotlib.widgets import Slider
        self.np = np
        self.math = math
        self.plt = plt
        self.slider = Slider

    def PlotMultiple(self, datas):
        for i in range(len(datas)):
            color = (self.np.random.random(),
                     self.np.random.random(), self.np.random.random())
            self.plt.plot(datas[i][0], datas[i][1], c=color)
        self.plt.show()

    def SliderPlot(self, datas, step, zoom, together=True, extraSliders=[]):
        if together:
            fig, ax = self.plt.subplots()
        else:
            fig, ax = self.plt.subplots(len(datas))
        bottom = 0.15
        if len(extraSliders) > 0:
            bottom = 0.5
        self.plt.subplots_adjust(bottom=bottom)

        linePlots = []
        for n in range(len(datas)):
            color = (self.np.random.random(), self.np.random.random(), self.np.random.random())
            marker = "" if len(datas[n]) == 2 else datas[n][2]
            if together:
                l, = self.plt.plot(datas[n][0], datas[n][1], c=color, marker=marker)
            else:
                l, = ax[n].plot(datas[n][0], datas[n][1], c=color, marker=marker)
            linePlots.append(l)

        self.plt.axis()

        xMin, yMin, xMax, yMax = self.CalculateBoundaries(datas)
        self.plt.xlim(xMin/zoom, step)
        self.plt.ylim(yMin/zoom, yMax/zoom)

        axpos = self.plt.axes([0.2, bottom - 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')

        spos = self.slider(axpos, 'Pos', 0, (xMax - xMin)-step, orientation='horizontal')

        def update(val):
            pos = val
            if together:
                ax.axis([pos, pos+step, yMin/zoom, yMax/zoom])
            else:
                for n in range(len(datas)):
                    ax[n].axis([pos, pos+step, yMin/zoom, yMax/zoom])
            fig.canvas.draw_idle()

        spos.on_changed(lambda val: update(val))

        parsWidth = 0.65
        parsHeight = 0.03
        frac=1000

        def updatePar(val, iPar):
            extraSlider = extraSliders[iPar]
            datas = extraSlider.ChangeFunction(extraSlider.ParName, val)
            _, yMin, _, yMax = self.CalculateBoundaries(datas)
            ax.set_ylim(yMin/zoom, yMax/zoom)
            for d in range(len(datas)):
                linePlots[d].set_data(datas[d][0], datas[d][1])

        for iPar in range(len(extraSliders)):
            extraSlider = extraSliders[iPar]
            eax = self.plt.axes([0.2, bottom - 0.1 - parsHeight - parsHeight * iPar, parsWidth, parsHeight], facecolor='lightgoldenrodyellow')
            extraSlider.Slider = self.slider(eax, extraSlider.ParName, extraSlider.MinValue, extraSlider.MaxValue, valinit=extraSlider.InitialValue, valstep=(extraSlider.MaxValue - extraSlider.MinValue)/frac, orientation='horizontal')
            match iPar:
                case 0:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 0))
                case 1:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 1))
                case 2:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 2))
                case 3:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 3))
                case 4:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 4))
                case 5:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 5))
                case 6:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 6))
                case 7:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 7))
                case 8:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 8))
                case 9:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 9))
        self.plt.show()

    def CalculateBoundaries(self, datas):
        xMin = 0
        yMin = 0
        xMax = 0
        yMax = 0
        for data in datas:
            if len(data[0])>0:
                xnMin = min(data[0])
                xnMax = max(data[0])
                if xnMin < xMin:
                    xMin = xnMin
                if xnMax > xMax:
                    xMax = xnMax
                ynMin = min(data[1])
                ynMax = max(data[1])
                if ynMin < yMin:
                    yMin = ynMin
                if ynMax > yMax:
                    yMax = ynMax
        return xMin,yMin,xMax,yMax

    def PlotPhaseSpace(self, x, y, N, step):
        stepi = 0
        stepf = int(step)

        fig, ax = self.plt.subplots()
        bottom = 0.15
        self.plt.subplots_adjust(bottom=bottom)
        l, = self.plt.plot(x[stepi:stepf], y[stepi:stepf])
        self.plt.axis()
        self.plt.xlim(min([*x, *y]), max([*x, *y]))
        self.plt.ylim(min([*y]), max([*y]))

        posSlide = self.plt.axes(
            [0.2, bottom - 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')

        spos = self.slider(posSlide, 't', 0, N-step,
                           orientation='horizontal')

        def updatePos(val):
            stepi = int(val)
            stepf = int(val + step)
            l.set_data(x[stepi:stepf], y[stepi:stepf])
            fig.canvas.draw_idle()

        spos.on_changed(updatePos)

        self.plt.show()

    def Histogram(self, data, bins=10, ylog=False, xlog=False, extraSliders = []):
        _, ax = self.plt.subplots()
        bottom = 0.15
        if len(extraSliders) > 0:
            bottom = 0.5
        self.plt.subplots_adjust(bottom=bottom)

        if ylog != None:
            self.plt.yscale('log')
        
        if xlog != None:
            self.plt.xscale('log')

        hist, bins = self.np.histogram(data, bins=bins)
        b = self.plt.bar(bins[:-1], hist, width=.3)

        self.plt.axis()

        parsWidth = 0.65
        parsHeight = 0.03
        frac=1000

        def updatePar(val, iPar):
            extraSlider = extraSliders[iPar]
            data = extraSlider.ChangeFunction(extraSlider.ParName, val)
            self.np.histogram(data, bins=bins)
            [bar.set_height(hist[i]) for i, bar in enumerate(b)]
            [bar.set_x(bins[i]) for i, bar in enumerate(b)]
            ax.relim()
            ax.autoscale_view()
            self.plt.draw()

        for iPar in range(len(extraSliders)):
            extraSlider = extraSliders[iPar]
            eax = self.plt.axes([0.2, bottom - 0.1 - parsHeight - parsHeight * iPar, parsWidth, parsHeight], facecolor='lightgoldenrodyellow')
            extraSlider.Slider = self.slider(eax, extraSlider.ParName, extraSlider.MinValue, extraSlider.MaxValue, valinit=extraSlider.InitialValue, valstep=(extraSlider.MaxValue - extraSlider.MinValue)/frac, orientation='horizontal')
            match iPar:
                case 0:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 0))
                case 1:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 1))
                case 2:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 2))
                case 3:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 3))
                case 4:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 4))
                case 5:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 5))
                case 6:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 6))
                case 7:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 7))
                case 8:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 8))
                case 9:
                    extraSlider.Slider.on_changed(lambda val: updatePar(val, 9))
        self.plt.show()
        return hist

    def PowerSeries(self, data):
        data = data - self.np.mean(data)
        sp = self.np.fft.fft(data)
        
        self.plt.plot(self.np.abs(sp))
        self.plt.show()

    def PlotHistogramSlopes(self, signal, bins = 10, slopeIndexes=[]):
        hist, bins_edges = self.np.histogram(signal, bins)

        y = []
        x = []
        for n in range(bins):
            if hist[n] != 0:
                x.append((bins_edges[n + 1] + bins_edges[n])/2)
                y.append(hist[n])

        lx = self.np.log(x)
        ly = self.np.log(y)
        self.plt.plot(lx,ly)

        from scipy.stats import linregress
        for si in slopeIndexes:
            lxv = lx[si[0]:si[1]]
            lyv = ly[si[0]:si[1]]
            r = linregress(lxv, lyv)
            self.plt.plot(lxv, [vx*r.slope + r.intercept for vx in lxv], marker="o", markersize=5)
            self.plt.text(lxv[0], lyv[0], f'y={r.slope:.2f}*x+{r.intercept:.2f}')

        self.plt.show()

    class SliderPar:
        def __init__(self, initialValue = None, minValue = None, maxValue = None, parName = None, changeFunction = None):
            self.InitialValue = initialValue
            self.MinValue = minValue
            self.MaxValue = maxValue
            self.ParName = parName
            self.ChangeFunction = changeFunction
            self.Slider = None