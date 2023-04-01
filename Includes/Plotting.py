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

    def SliderPlot(self, y, N, step, yZoom):
        fig, ax = self.plt.subplots()
        self.plt.subplots_adjust(bottom=0.25)
        x = range(0, N)
        l, = self.plt.plot(x, y)
        yAxisMin = min(y)/yZoom
        yAxisMax = max(y)/yZoom
        self.plt.axis([0, step, yAxisMin, yAxisMax])

        axcolor = 'lightgoldenrodyellow'
        axpos = self.plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)

        spos = self.slider(axpos, 'Pos', 0, N-step)

        def update(val):
            pos = spos.val
            ax.axis([pos, pos+step, yAxisMin, yAxisMax])
            fig.canvas.draw_idle()

        spos.on_changed(update)

        self.plt.show()

    def PlotPhaseSpace(self, x, y, N, cutoff):
        self.plt.plot(x[0:self.math.floor(N*cutoff)],
                      y[0:self.math.floor(N*cutoff)])
        self.plt.show()
