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

    def SliderPlot(self, datas, step, zoom, together=False, extraSliders=[]):
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
            for n in range(len(datas)):
                if together:
                    ax.axis([pos, pos+step, yMin/zoom, yMax/zoom])
                else:
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

    def Histogram(self, data, bins=10, log=False):
        self.plt.hist(data, bins=bins, log=log)
        self.plt.show()

    class SliderPar:
        def __init__(self, initialValue = None, minValue = None, maxValue = None, parName = None, changeFunction = None):
            self.InitialValue = initialValue
            self.MinValue = minValue
            self.MaxValue = maxValue
            self.ParName = parName
            self.ChangeFunction = changeFunction
            self.Slider = None