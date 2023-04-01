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

    def SliderPlot(self, y, N, step, yZoom, extraSliders=[]):
        fig, ax = self.plt.subplots()
        bottom = 0.15
        if len(extraSliders) > 0:
            bottom = 0.5
        self.plt.subplots_adjust(bottom=bottom)

        l, = self.plt.plot(range(0, N), y)
        self.plt.axis()
        self.plt.ylim(min(y)/yZoom, max(y)/yZoom)
        self.plt.xlim(0, step)

        axcolor = 'lightgoldenrodyellow'
        axpos = self.plt.axes(
            [0.2, bottom - 0.1, 0.65, 0.03], facecolor=axcolor)

        spos = self.slider(axpos, 'Pos', 0, N-step, orientation='horizontal')

        parLeft = 0.1
        parRight = 0.5
        parsWidth = 0.3
        parsHeight = 0.03
        parsSeparation = 0.1

        iPar = 0
        if len(extraSliders) > iPar:
            extraSlider0 = extraSliders[iPar]
            ax0 = self.plt.axes([parLeft, bottom - parsSeparation * (iPar + 2),
                                parsWidth, parsHeight], facecolor='lightgoldenrodyellow')
            s0 = self.slider(ax0, extraSlider0[3], extraSlider0[1], extraSlider0[2], valinit=extraSlider0[0], valstep=(
                extraSlider0[2] - extraSlider0[1])/100, orientation='horizontal')

            def updatePar0(val):
                (y, N) = extraSlider0[4](extraSlider0[3], val, extraSlider0[5])
                l.set_data(range(0, N), y)
                ax.set_ylim(min(y)/yZoom, max(y)/yZoom)

            s0.on_changed(updatePar0)

        iPar = 1
        if len(extraSliders) > iPar:
            extraSlider1 = extraSliders[iPar]
            ax1 = self.plt.axes([parLeft, bottom - parsSeparation * (iPar + 2),
                                parsWidth, parsHeight], facecolor='lightgoldenrodyellow')
            s1 = self.slider(ax1, extraSlider1[3], extraSlider1[1], extraSlider1[2], valinit=extraSlider1[0], valstep=(
                extraSlider1[2] - extraSlider1[1])/100, orientation='horizontal')

            def updatePar1(val):
                (y, N) = extraSlider1[4](extraSlider1[3], val, extraSlider1[5])
                l.set_data(range(0, N), y)
                ax.set_ylim(min(y)/yZoom, max(y)/yZoom)

            s1.on_changed(updatePar1)

        iPar = 2
        if len(extraSliders) > iPar:
            extraSlider2 = extraSliders[iPar]
            ax2 = self.plt.axes([parLeft, bottom - parsSeparation * (iPar + 2),
                                parsWidth, parsHeight], facecolor='lightgoldenrodyellow')
            s2 = self.slider(ax2, extraSlider2[3], extraSlider2[1], extraSlider2[2], valinit=extraSlider2[0], valstep=(
                extraSlider2[2] - extraSlider2[1])/100, orientation='horizontal')

            def updatePar2(val):
                (y, N) = extraSlider2[4](extraSlider2[3], val, extraSlider2[5])
                l.set_data(range(0, N), y)
                ax.set_ylim(min(y)/yZoom, max(y)/yZoom)

            s2.on_changed(updatePar2)

        iPar = 3
        if len(extraSliders) > iPar:
            extraSlider3 = extraSliders[iPar]
            ax3 = self.plt.axes([parRight, bottom - parsSeparation * (iPar - 3 + 2),
                                parsWidth, parsHeight], facecolor='lightgoldenrodyellow')
            s3 = self.slider(ax3, extraSlider3[3], extraSlider3[1], extraSlider3[2], valinit=extraSlider3[0], valstep=(
                extraSlider3[2] - extraSlider3[1])/100, orientation='horizontal')

            def updatePar3(val):
                (y, N) = extraSlider3[4](extraSlider3[3], val, extraSlider3[5])
                l.set_data(range(0, N), y)
                ax.set_ylim(min(y)/yZoom, max(y)/yZoom)

            s3.on_changed(updatePar3)

        iPar = 4
        if len(extraSliders) > iPar:
            extraSlider4 = extraSliders[iPar]
            ax4 = self.plt.axes([parRight, bottom - parsSeparation * (iPar - 3 + 2),
                                parsWidth, parsHeight], facecolor='lightgoldenrodyellow')
            s4 = self.slider(ax4, extraSlider4[3], extraSlider4[1], extraSlider4[2], valinit=extraSlider4[0], valstep=(
                extraSlider4[2] - extraSlider4[1])/100, orientation='horizontal')

            def updatePar4(val):
                (y, N) = extraSlider4[4](extraSlider4[3], val, extraSlider4[5])
                l.set_data(range(0, N), y)
                ax.set_ylim(min(y)/yZoom, max(y)/yZoom)

            s4.on_changed(updatePar4)

        iPar = 5
        if len(extraSliders) > iPar:
            extraSlider5 = extraSliders[iPar]
            ax5 = self.plt.axes([parRight, bottom - parsSeparation * (iPar - 3 + 2),
                                parsWidth, parsHeight], facecolor='lightgoldenrodyellow')
            s5 = self.slider(ax5, extraSlider5[3], extraSlider5[1], extraSlider5[2], valinit=extraSlider5[0], valstep=(
                extraSlider5[2] - extraSlider5[1])/100, orientation='horizontal')

            def updatePar5(val):
                (y, N) = extraSlider5[4](extraSlider5[3], val, extraSlider5[5])
                l.set_data(range(0, N), y)
                ax.set_ylim(min(y)/yZoom, max(y)/yZoom)
                
            s5.on_changed(updatePar5)

        def update(val):
            pos = val
            ax.axis([pos, pos+step, min(y)/yZoom, max(y)/yZoom])
            fig.canvas.draw_idle()

        spos.on_changed(update)

        self.plt.show()

    def PlotPhaseSpace(self, x, y, N, cutoff):
        self.plt.plot(x[0:self.math.floor(N*cutoff)],
                      y[0:self.math.floor(N*cutoff)])
        self.plt.show()
