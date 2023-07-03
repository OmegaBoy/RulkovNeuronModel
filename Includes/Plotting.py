class Plotting:
    def __init__(self):
        import numpy as np
        import math
        import matplotlib.pyplot as plt
        from matplotlib.widgets import Slider
        from matplotlib.widgets import TextBox
        self.np = np
        self.math = math
        self.plt = plt
        self.slider = Slider
        self.TextBox = TextBox

    def PlotMultiple(self, datas, together=True, logx=False, logy=False):
        if together:
            fig, ax = self.plt.subplots()
            for i in range(len(datas)):
                color = (self.np.random.random(),
                         self.np.random.random(), self.np.random.random())
                self.plt.plot(datas[i][0], datas[i][1], c=color)
                if logx == True:
                    self.plt.xscale('log')
                if logy == True:
                    self.plt.yscale('log')
        else:
            fig, ax = self.plt.subplots(len(datas))
            for i in range(len(datas)):
                l, = ax[i].plot(datas[i][0], datas[i][1])
                if logx == True:
                    ax[i].set_xscale('log')
                if logy == True:
                    ax[i].set_yscale('log')

        ax.set_xlabel('Frecuencia')
        ax.set_ylabel('Intensidad')
        self.plt.show()

    def SliderPlot(self, datas, step, together=True, extraPars=[], zoom=0.7):
        if together:
            fig, ax = self.plt.subplots()
        else:
            fig, ax = self.plt.subplots(len(datas))
        bottom = 0.15
        if len(extraPars) > 0:
            bottom = 0.5
        self.plt.subplots_adjust(bottom=bottom)

        linePlots = []
        for n in range(len(datas)):
            color = (self.np.random.random(),
                     self.np.random.random(), self.np.random.random())
            marker = "" if len(datas[n]) == 2 else datas[n][2]
            if together:
                l, = self.plt.plot(
                    datas[n][0], datas[n][1], c=color, marker=marker)
            else:
                l, = ax[n].plot(datas[n][0], datas[n][1],
                                c=color, marker=marker)
            linePlots.append(l)

        self.plt.axis()

        bounds = self.CalculateBoundaries(datas, together, zoom)

        if together:
            self.plt.axis([0, step, bounds[0]["yMin"], bounds[0]["yMax"]])
        else:
            for n in range(len(datas)):
                ax[n].axis([0, step, bounds[n]["yMin"], bounds[n]["yMax"]])

        axpos = self.plt.axes([0.2, bottom - 0.1, 0.65, 0.03],
                              facecolor='lightgoldenrodyellow')

        spos = self.slider(
            axpos, 'Pos', 0, (bounds[0]["xMax"] - bounds[0]["xMin"])-step, orientation='horizontal')

        def update(val):
            pos = val
            if together:
                ax.axis([pos, pos+step, bounds[0]["yMin"], bounds[0]["yMax"]])
            else:
                for n in range(len(datas)):
                    ax[n].axis([pos, pos+step, bounds[n]
                               ["yMin"], bounds[n]["yMax"]])
            fig.canvas.draw_idle()

        spos.on_changed(lambda val: update(val))

        def updatePar(val, iPar):
            extraPar = extraPars[iPar]
            datas = extraPar.ChangeFunction(extraPar.ParName, val)
            bounds = self.CalculateBoundaries(datas, together)
            for n in range(len(datas)):
                if together:
                    ax.axis([0, step, bounds[0]["yMin"], bounds[0]["yMax"]])
                else:
                    ax[n].axis([0, step, bounds[n]["yMin"], bounds[n]["yMax"]])
                linePlots[n].set_data(datas[n][0], datas[n][1])

        for iPar in range(len(extraPars)):
            extraPar = extraPars[iPar]
            match extraPar.ParType:
                case 'Slider':
                    parsWidth = 0.65
                    parsHeight = 0.03
                    frac = 1000
                    eax = self.plt.axes([0.2, bottom - 0.1 - parsHeight - parsHeight *
                                        iPar, parsWidth, parsHeight], facecolor='lightgoldenrodyellow')
                    extraPar.Par = self.slider(eax, extraPar.ParName, extraPar.MinValue, extraPar.MaxValue, valinit=extraPar.InitialValue, valstep=(
                        extraPar.MaxValue - extraPar.MinValue)/frac, orientation='horizontal')
                    match iPar:
                        case 0:
                            extraPar.Par.on_changed(
                                lambda val: updatePar(val, 0))
                        case 1:
                            extraPar.Par.on_changed(
                                lambda val: updatePar(val, 1))
                        case 2:
                            extraPar.Par.on_changed(
                                lambda val: updatePar(val, 2))
                        case 3:
                            extraPar.Par.on_changed(
                                lambda val: updatePar(val, 3))
                        case 4:
                            extraPar.Par.on_changed(
                                lambda val: updatePar(val, 4))
                        case 5:
                            extraPar.Par.on_changed(
                                lambda val: updatePar(val, 5))
                        case 6:
                            extraPar.Par.on_changed(
                                lambda val: updatePar(val, 6))
                        case 7:
                            extraPar.Par.on_changed(
                                lambda val: updatePar(val, 7))
                        case 8:
                            extraPar.Par.on_changed(
                                lambda val: updatePar(val, 8))
                        case 9:
                            extraPar.Par.on_changed(
                                lambda val: updatePar(val, 9))

                case 'TextBox':
                    parsWidth = 0.1
                    parsHeight = 0.03
                    if iPar < 13:
                        eax = self.plt.axes([0.2, bottom - 0.1 - parsHeight - parsHeight *
                                            iPar, parsWidth, parsHeight], facecolor='lightgoldenrodyellow')
                    if iPar > 12 and iPar < 26:
                        eax = self.plt.axes([0.5, bottom - 0.1 - parsHeight - parsHeight * (
                            iPar - 13), parsWidth, parsHeight], facecolor='lightgoldenrodyellow')
                    if iPar > 25:
                        eax = self.plt.axes([0.8, bottom - 0.1 - parsHeight - parsHeight * (
                            iPar - 26), parsWidth, parsHeight], facecolor='lightgoldenrodyellow')
                    extraPar.Par = self.TextBox(
                        eax, extraPar.ParName, extraPar.InitialValue)
                    match iPar:
                        case 0:
                            extraPar.Par.on_submit(lambda val: updatePar(
                                float(val if val != '' else extraPar.InitialValue), 0))
                        case 1:
                            extraPar.Par.on_submit(lambda val: updatePar(
                                float(val if val != '' else extraPar.InitialValue), 1))
                        case 2:
                            extraPar.Par.on_submit(lambda val: updatePar(
                                float(val if val != '' else extraPar.InitialValue), 2))
                        case 3:
                            extraPar.Par.on_submit(lambda val: updatePar(
                                float(val if val != '' else extraPar.InitialValue), 3))
                        case 4:
                            extraPar.Par.on_submit(lambda val: updatePar(
                                float(val if val != '' else extraPar.InitialValue), 4))
                        case 5:
                            extraPar.Par.on_submit(lambda val: updatePar(
                                float(val if val != '' else extraPar.InitialValue), 5))
                        case 6:
                            extraPar.Par.on_submit(lambda val: updatePar(
                                float(val if val != '' else extraPar.InitialValue), 6))
                        case 7:
                            extraPar.Par.on_submit(lambda val: updatePar(
                                float(val if val != '' else extraPar.InitialValue), 7))
                        case 8:
                            extraPar.Par.on_submit(lambda val: updatePar(
                                float(val if val != '' else extraPar.InitialValue), 8))
                        case 9:
                            extraPar.Par.on_submit(lambda val: updatePar(
                                float(val if val != '' else extraPar.InitialValue), 9))
        self.plt.show()

    def CalculateBoundaries(self, datas, together=True, zoom=0.9):
        bounds = []
        xMin = 0
        yMin = 0
        xMax = 0
        yMax = 0
        for data in datas:
            if len(data[0]) > 0:
                xnMin = min(data[0])
                xnMax = max(data[0])
                if together:
                    if xnMin < xMin:
                        xMin = xnMin
                    if xnMax > xMax:
                        xMax = xnMax
                else:
                    xMin = xnMin
                    xMax = xnMax
                ynMin = min(data[1])
                ynMax = max(data[1])
                if together:
                    if ynMin < yMin:
                        yMin = ynMin
                    if ynMax > yMax:
                        yMax = ynMax
                else:
                    yMin = ynMin
                    yMax = ynMax
                bounds.append({"xMin": xMin,
                              "yMin": (yMin + yMin*(1-zoom)), "xMax": xMax, "yMax": (yMax + yMax*(1-zoom))})
        if together:
            return [bounds[len(bounds) - 1]]
        else:
            return bounds

    def PlotPhaseSpace(self, x, y, N, step):
        stepi = 0
        stepf = int(step)

        fig, ax = self.plt.subplots()
        bottom = 0.15
        self.plt.subplots_adjust(bottom=bottom)
        l, = self.plt.plot(x[stepi:stepf], y[stepi:stepf])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        self.plt.axis()
        self.plt.xlim(min([*x, *y]), max([*x, *y]))
        self.plt.ylim(min([*y]), max([*y]))

        posSlide = self.plt.axes(
            [0.2, bottom - 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')

        spos = self.slider(posSlide, 't', 0, N-step, orientation='horizontal')

        def updatePos(val):
            stepi = int(val)
            stepf = int(val + step)
            l.set_data(x[stepi:stepf], y[stepi:stepf])
            fig.canvas.draw_idle()

        spos.on_changed(updatePos)

        self.plt.show()

    def Histogram(self, data, bins=10, ylog=False, xlog=False, extraSliders=[]):
        _, ax = self.plt.subplots()
        bottom = 0.15
        if len(extraSliders) > 0:
            bottom = 0.5
        self.plt.subplots_adjust(bottom=bottom)

        if ylog != None and ylog:
            self.plt.yscale('log')

        if xlog != None and xlog:
            self.plt.xscale('log')

        # %% Media y Std Dev de Intervalos
        mean = self.np.mean(data)
        std = self.np.std(data)
        print('Mean: ' + str(mean))
        print('StdDev: ' + str(std))

        ax.set_xlabel('Número de pasos')
        ax.set_ylabel('Cantidad de intervalos en rango de pasos')

        # Add vertical lines for mean and standard deviation
        self.plt.axvline(mean, color='red', linestyle='dashed',
                         linewidth=2, label='Media')
        self.plt.axvline(mean + std, color='green', linestyle='dashed',
                         linewidth=2, label='Desviacion estandar sup.')
        self.plt.axvline(mean - std, color='green', linestyle='dashed',
                         linewidth=2, label='Desviacion estandar inf.')

        # Add legend
        self.plt.legend()

        hist, bins = self.np.histogram(data, bins=bins)
        b = self.plt.bar(bins[:-1], hist, width=1)

        self.plt.axis()

        parsWidth = 0.65
        parsHeight = 0.03
        frac = 1000

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
            eax = self.plt.axes([0.2, bottom - 0.1 - parsHeight - parsHeight *
                                iPar, parsWidth, parsHeight], facecolor='lightgoldenrodyellow')
            extraSlider.Slider = self.slider(eax, extraSlider.ParName, extraSlider.MinValue, extraSlider.MaxValue, valinit=extraSlider.InitialValue, valstep=(
                extraSlider.MaxValue - extraSlider.MinValue)/frac, orientation='horizontal')
            match iPar:
                case 0:
                    extraSlider.Slider.on_changed(
                        lambda val: updatePar(val, 0))
                case 1:
                    extraSlider.Slider.on_changed(
                        lambda val: updatePar(val, 1))
                case 2:
                    extraSlider.Slider.on_changed(
                        lambda val: updatePar(val, 2))
                case 3:
                    extraSlider.Slider.on_changed(
                        lambda val: updatePar(val, 3))
                case 4:
                    extraSlider.Slider.on_changed(
                        lambda val: updatePar(val, 4))
                case 5:
                    extraSlider.Slider.on_changed(
                        lambda val: updatePar(val, 5))
                case 6:
                    extraSlider.Slider.on_changed(
                        lambda val: updatePar(val, 6))
                case 7:
                    extraSlider.Slider.on_changed(
                        lambda val: updatePar(val, 7))
                case 8:
                    extraSlider.Slider.on_changed(
                        lambda val: updatePar(val, 8))
                case 9:
                    extraSlider.Slider.on_changed(
                        lambda val: updatePar(val, 9))
        self.plt.show()
        return hist

    def PowerSeries(self, data, logx=False, logy=False):
        data = data - self.np.mean(data)

        ps = self.np.abs(self.np.fft.fft(data))**2

        datas = []
        index = [i for i in range(len(ps[1:int((len(data)/2)-1)]))]
        data = ps[1:int((len(data)/2)-1)]
        datas.append([index, data])
        windowsSizes = [30, 90, 150]
        for ws in windowsSizes:
            data = self.moving_average(data, ws)
            datas.append([index, data])

        self.PlotMultiple(datas, together=True, logx=logx, logy=logy)

    def moving_average(self, data, window_size):
        window = self.np.ones(window_size) / window_size
        smoothed_data = self.np.convolve(data, window, mode='same')
        return smoothed_data

    def PlotHistogramSlopes(self, signal, ylog=False, xlog=False, bins=10, slopesData=[]):
        _, ax = self.plt.subplots()

        datas = []
        # Ponemos rectas en las pendientes
        for slope in slopesData["Slopes"]:
            datas.append([[lx for lx in slope["lx"]], [
                         vx*slope["Slope"].slope + slope["Slope"].intercept for vx in slope["lx"]]])

        if xlog and ylog:
            for d in datas:
                d[0] = self.np.power(10, d[0])
                d[1] = self.np.power(10, d[1])

        if ylog != None and ylog:
            self.plt.yscale('log')

        if xlog != None and xlog:
            self.plt.xscale('log')

        hist, bins = self.np.histogram(signal, bins=bins)
        b = self.plt.bar(bins[:-1], hist, width=1)

        ax.set_xlabel('Número de pasos')
        ax.set_ylabel('Cantidad de intervalos en rango de pasos')

        for n in range(len(datas)):
            self.plt.plot(datas[n][0], datas[n][1])
            self.plt.text(datas[n][0][int(self.np.round(len(datas[n][0])/2))], datas[n][1][int(self.np.round(len(datas[n][0])/2))], "y=" + str(
                self.np.round(slopesData["Slopes"][n]["Slope"].slope, 2)) + "*x+" + str(self.np.round(slopesData["Slopes"][n]["Slope"].intercept, 2)), fontsize=12)

        self.plt.show()

    def PlotRecurrence(self, signal):
        # Calculo de la matriz de distancias
        distance_matrix = self.np.abs(self.np.subtract.outer(signal, signal))

        # Elijo el mapa de color
        cmap = self.plt.get_cmap('coolwarm')

        # Creo el grafico de recurrencia
        self.plt.imshow(distance_matrix, cmap=cmap, origin='lower')
        self.plt.title('Grafico de Recurrencia')

        # Add colorbar with legend
        cbar = self.plt.colorbar(label='Recurrencia')
        self.plt.show()

    class DynamicPar:
        def __init__(self, parType='Slider', initialValue=None, minValue=None, maxValue=None, parName=None, changeFunction=None):
            self.InitialValue = initialValue
            self.MinValue = minValue
            self.MaxValue = maxValue
            self.ParName = parName
            self.ChangeFunction = changeFunction
            self.Par = None
            self.ParType = parType

# %%
